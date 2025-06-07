from django.shortcuts import render
from django.conf import settings
import hashlib
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Order
from .serializers import *
from .permissions import IsAdminOrReadOnly
from .utils import get_oauth_token, get_payu_order_status




class MenuItems(APIView):
    permission_classes = [IsAdminOrReadOnly]
    """
    API endpoint for managing menu items
    """
    
    @swagger_auto_schema(
        operation_description="Get list of menu items",
        manual_parameters=[
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Filter by category",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={200: MenuItemSerializer(many=True)}
    )
    def get(self, request, pk=None):
        category = request.query_params.get('category')

        if pk:        
            item = get_object_or_404(MenuItem,pk=pk)
            serializer = MenuItemSerializer(item)
        else:
            if category:
                items = get_list_or_404(MenuItem, category__iexact=category)
            else:
                items = get_list_or_404(MenuItem)
            serializer = MenuItemSerializer(items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
        

    @swagger_auto_schema(
        operation_description="Create a new menu item",
        request_body=MenuItemSerializer,
        responses={201: MenuItemSerializer()}
    )
    def post(self, request, pk=None):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #DONE
    def put(self, request, pk=None):
        if not pk:
            return Response({'error': 'UUID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemSerializer(item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #DONE
    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'UUID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        item = get_object_or_404(MenuItem, pk=pk)
        item.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)






class Orders(APIView):
    """
    API endpoint for managing orders
    """
    
    @swagger_auto_schema(
        operation_description="Get order details",
        manual_parameters=[
            openapi.Parameter(
                'email',
                openapi.IN_QUERY,
                description="Customer email for order verification",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'check_payment',
                openapi.IN_QUERY,
                description="Check payment status",
                type=openapi.TYPE_BOOLEAN,
                required=False
            )
        ],
        responses={
            200: FullOrderSerializer(),
            400: 'Bad Request',
            404: 'Not Found'
        }
        )
    def get(self, request, pk=None):
        check_payment = request.query_params.get('check_payment', False)
        
        if check_payment and pk:
            email = request.query_params.get('email')
            
            order = get_object_or_404(Order, order_number_uuid=pk, customer_email=email)
                
            if not order.payu_order_id:
                    return Response(
                        {'error': 'No payment information for this order'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
            if order.payment_status != None:
                    return Response({
                        'status': order.status,
                        'payuStatus': order.payment_status,
                        'orderNumber': order.order_number_uuid
                    }, status=status.HTTP_200_OK)
                
            access_token = get_oauth_token()
            payu_status = get_payu_order_status(order.payu_order_id, access_token)
                
            if payu_status:
                status_mapping = {
                        'COMPLETED': 'confirmed',
                        'PENDING': 'pending',
                        'CANCELED': 'canceled',
                        'REJECTED': 'canceled'
                    }
                    
                payu_order_status = payu_status.get('orders', [{}])[0].get('status')
                new_status = status_mapping.get(payu_order_status)
                    
                if new_status != order.payment_status:
                        order.payment_status = new_status
                        order.save()
                    
                return Response({
                        'status': order.status,
                        'payuStatus': order.payment_status,
                        'orderNumber': order.order_number_uuid
                    }, status=status.HTTP_200_OK)
                
            return Response(
                    {'error': 'Could not fetch payment status'}, 
                    status=status.HTTP_502_BAD_GATEWAY
                )


        # Case 1: Unauthenticated user with order lookup
        if not request.user.is_authenticated:
            email = request.query_params.get('email')
            if pk and email:
                try:
                    order = get_object_or_404(Order, order_number_uuid=pk, customer_email=email)
                    serializer = FullOrderSerializer(order)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Order.DoesNotExist:
                    return Response(
                        {'error': 'Order not found with provided email'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
            return Response(
                {'error': 'Please provide both order number and email'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Case 2: Authenticated admin user
        if request.user.is_staff:
            if pk:
                order = get_object_or_404(Order, order_number_uuid=pk)
                serializer = FullOrderSerializer(order)
            else:
                orders = Order.objects.all()
                serializer = FullOrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Case 3: Authenticated regular user
        if pk:
            order = get_object_or_404(
                Order, 
                order_number_uuid=pk, 
                customer_email=request.user.email
            )
            serializer = FullOrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Return all orders for the logged-in user
            orders = Order.objects.filter(customer_email=request.user.email)
            serializer = FullOrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    #TODO:
    # - change serializer for user
    def put(self, request, pk=None):
        email = request.data.get('email')

        if not pk:
            return Response({'error': 'UUID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.is_staff and not email:
            return Response({'error': 'Only staff can change this order'}, status=status.HTTP_403_FORBIDDEN)

        if email:
            #TODO: add serializer with only adress changable
            order = get_object_or_404(Order, pk=pk, customer_email=email)
            serializer = OrderUserSerializer(order, data=request.data, partial=True)

        else:
            #uuid_ without email -> del order by id / admin
            order = get_object_or_404(Order, pk=pk)
            serializer = OrderSerializer(order, data=request.data, partial=True)
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #TODO:
    # - add serialization of items, based on UUID's of menu items (fornt sends menuItem_uuids in body)
    def post(self, request, pk=None):
        order_data = request.data.copy()
        items_buffor = order_data.pop('items', [])

        try:
            if isinstance(items_buffor[0], str):
                items_buffor = items_buffor[0].replace('\t', '').replace('\n', '')
                order_items = json.loads(items_buffor)
                
            else:
                order_items = items_buffor
        except json.JSONDecodeError:
            return Response(
                {'error': 'Invalid items format'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(order_items)==0:
            return Response(
                {'error': 'Invalid items format'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            
            # Process order items
            for item_data in order_items:
                order_item = {
                    'order': order.id,
                    'menu_item': item_data.get('menu_item'),  
                    'quantity': item_data.get('quantity', 1)  
                }
                item_serializer = OrderItemSerializer(data=order_item)
                if item_serializer.is_valid():
                    item_serializer.save()
                else:
                    order.delete()
                    return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
            order.calculate_total()

            
            
            try:

                # Get OAuth token
                access_token = get_oauth_token()

                # Prepare PayU request data
                payu_data = {
                    "extOrderId": str(order.order_number_uuid),
                    "merchantPosId": settings.PAYU_POS_ID,
                    "description": f"Order {order.order_number_uuid}",
                    "currencyCode": request.data.get('currency', 'PLN'),
                    "totalAmount": str(int(float(order.total_amount) * 100)),
                    "buyer": {
                        "email": order.customer_email,
                        "phone": order.customer_phone,
                        "firstName": order.customer_name,
                        "language": "pl"
                    },
                    "products": [
                        {
                            "name": item.menu_item.name,
                            "unitPrice": str(int(float(item.menu_item.price) * 100)),
                            "quantity": item.quantity
                        } for item in order.items.all()
                    ],
               
                    "continueUrl": f"{settings.FRONT_BASE_URL}/payment-redirect/{order.order_number_uuid}?email={order.customer_email}",
                    "customerIp": request.META.get('REMOTE_ADDR'),
                }

                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json',
                }

                response = requests.post(
                    settings.PAYU_ORDER_URL,
                    json=payu_data,
                    headers=headers,
                    allow_redirects=False 
                )

                response_data = response.json()
            
                if response_data.get('status', {}).get('statusCode') == 'SUCCESS':
                    redirect_uri = response_data.get('redirectUri')
                    order_id = response_data.get('orderId')

                    if not redirect_uri:
                        return Response(
                            {'error': 'No redirect URL in PayU response'},
                            status=status.HTTP_502_BAD_GATEWAY
                        )

                    # Save PayU order ID
                    order.payu_order_id = order_id
                    order.save()

                    return Response({
                        'redirectUri': redirect_uri,
                        'orderId': order_id,
                        'status': 'success'
                    }, status=status.HTTP_200_OK)
            
                else:
                    error_message = response_data.get('status', {}).get('statusDesc', 'Unknown error')
                    return Response(
                        {'error': f'PayU error: {error_message}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


            #return Response(FullOrderSerializer(order).data, status=status.HTTP_201_CREATED)  # Changed to FullOrderSerializer
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    #DONE
    def delete(self, request, pk=None):
        email = request.data.get('email')
        
        if not pk:
            return Response({'error': 'UUID is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_staff and not email:
            return Response({'error': 'Only staff can del this order'}, status=status.HTTP_403_FORBIDDEN)
        
        if email:
            #uuid_ + email -> del order by id  and email/ user
            order = get_object_or_404(Order, pk=pk, customer_email=email)
        
        else:
            #uuid_ without email -> del order by id / admin
            order = get_object_or_404(Order, pk=pk)
            
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UserEndpoint(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_ = get_object_or_404(UserObject, id=request.user.id)
        serializer = UserSerializer(user_)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        user_ = get_object_or_404(UserObject, id=request.user.id)
        user_.is_active = False
        user_.save()
        return Response({"message": "User deactivated"}, status=status.HTTP_200_OK)

    def put(self, request):
        print(request)
        user_instance = get_object_or_404(UserObject, id=request.user.id)
        serializer = UserSerializer(user_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RegisterEndpoint(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer_ = UserSerializer(data=request.data)
        if serializer_.is_valid():
            serializer_.save()
            return Response(
                {"OK": "User created sucesfully"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer_.errors, status=status.HTTP_400_BAD_REQUEST)
