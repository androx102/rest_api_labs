from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404


from .serializers import *
from .permissions import IsAdminOrReadOnly




class MenuItems(APIView):
    permission_classes = [IsAdminOrReadOnly]

    #DONE
    def get(self, request, uuid_=None):
        category = request.query_params.get('category')

        if uuid_:
            item = get_object_or_404(MenuItem,menu_item_uuid=uuid_)
            serializer = MenuItemSerializer(item)
        else:
            if category:
                items = get_list_or_404(MenuItem, category__iexact=category)
            else:
                items = get_list_or_404(MenuItem)
            serializer = MenuItemSerializer(items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
        

    #DONE - only for admin
    def post(self, request, uuid_=None):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #DONE - only for admin
    def put(self, request, uuid_=None):
        if not uuid_:
            return Response({'error': 'UUID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        item = get_object_or_404(MenuItem, menu_item_uuid=uuid_)
        serializer = MenuItemSerializer(item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #DONE - only for admin
    def delete(self, request, uuid_=None):
        if not uuid_:
            return Response({'error': 'UUID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        item = get_object_or_404(MenuItem, menu_item_uuid=uuid_)
        item.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



class Orders(APIView):
    permission_classes = [IsAdminOrReadOnly]

    # get order details for user / get list of all orders for admin
    def get(self, request, uuid_=None):

        #TODO:
        # - for uuid_ + email -> return details of single order 
        # - for all -> check if staff_user
        # - for uuid_ without email -> return details of single order
        if uuid_:
            order = get_object_or_404(Order, order_number_uuid=uuid_)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    #TODO:
    # - handle change of adress, status, customer's data, items in order??
    def put(self, request, uuid_=None):
        if not uuid_:
            return Response({'error': 'UUID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        order = get_object_or_404(Order, order_number_uuid=uuid_)
        serializer = OrderSerializer(order, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #TODO:
    # - add serialization of items, based on UUID's of menu items (fornt sends menuItem_uuids in body)
    def post(self, request, uuid_=None):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    #DONE - only for admin ?? or delete based on user's email ??
    def delete(self, request, uuid_=None):
        if not uuid_:
            return Response({'error': 'UUID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        order = get_object_or_404(Order, order_number_uuid=uuid_)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)