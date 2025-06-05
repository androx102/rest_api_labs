from django.contrib import admin
from .models import OrderItem, Order, MenuItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('menu_item', 'quantity', 'subtotal')
    can_delete = False
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number_uuid', 'customer_name', 'customer_email', 
                   'status', 'created_at', 'total_amount')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number_uuid', 'customer_name', 'customer_email')
    readonly_fields = ('order_number_uuid', 'created_at', 'total_amount')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number_uuid', 'status', 'created_at', 'total_amount')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'delivery_address')
        }),
    )

admin.site.register(MenuItem)