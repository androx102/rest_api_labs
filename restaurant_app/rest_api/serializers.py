from rest_framework import serializers
from .models import MenuItem, Order, OrderItem, UserObject


class MenuItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = MenuItem
    fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = OrderItem
    fields = '__all__'

class OrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['delivery_address']
        read_only_fields = [
            'order_number_uuid', 
            'customer_name', 
            'customer_email',
            'customer_phone', 
            'status', 
            'created_at',
            'total_amount'
        ]

class OrderItemDetailSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_price = serializers.DecimalField(source='menu_item.price', max_digits=6, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'menu_item_name', 'menu_item_price', 'quantity', 'subtotal']

class FullOrderSerializer(serializers.ModelSerializer):
    items = OrderItemDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['order_number_uuid', 'customer_name', 'customer_email', 
                 'customer_phone', 'delivery_address', 'status', 'created_at', 
                 'total_amount', 'items']
        


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserObject
        fields = [
            "id",
            "username",
            "email",
            "password",
            "is_verified",
            "is_active",
            "delivery_address",
            "name",
            "phone_number"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            "is_verified": {"read_only": True},
            "is_active": {"read_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance