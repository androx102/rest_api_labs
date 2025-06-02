from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404

import json
from .serializers import *
from .permissions import IsAdminOrReadOnly




class MenuItems(APIView):
    permission_classes = [IsAdminOrReadOnly]

    #DONE
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
        

    #DONE
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
    def delete(self, request, uuid_=None):
        if not uuid_:
            return Response({'error': 'UUID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        item = get_object_or_404(MenuItem, menu_item_uuid=uuid_)
        item.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)





class Orders(APIView):
    #permission_classes = [IsAdminOrReadOnly]

    #DONE 
    def get(self, request, pk=None):
        email = request.data.get('email')
        print(email)

        if pk:
            if not request.user.is_staff and not email:
                return Response({'error': 'Only staff can see this order'}, status=status.HTTP_403_FORBIDDEN)

            if email:
                #uuid_ + email -> return details of single order 
                order = get_object_or_404(Order, pk=pk, customer_email=email)
        
            else:
                #uuid_ -> return details of single order 
                order = get_object_or_404(Order, pk=pk)

            serializer = FullOrderSerializer(order)  # Changed to FullOrderSerializer
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        else:
            if not request.user.is_staff:
                return Response({'error': 'Only staff can view all orders'}, status=status.HTTP_403_FORBIDDEN)
            
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)  # Changed to FullOrderSerializer
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
            return Response(FullOrderSerializer(order).data, status=status.HTTP_201_CREATED)  # Changed to FullOrderSerializer
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