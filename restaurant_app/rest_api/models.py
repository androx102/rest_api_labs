from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)





class UserObject(AbstractUser):
    username = None
    user_uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, null=False)
    is_verified = models.BooleanField(default=True)
    email = models.EmailField(max_length=254, verbose_name="email address", unique=True)
    name = models.TextField(null=True,blank=True)
    delivery_address = models.TextField(null=True,blank=True)
    phone_number = models.CharField(null=True,blank=True,max_length=20)    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
   
    objects = UserManager()
   
   #def save(self, *args, **kwargs):
   #    self.username = self.email
   #    super().save(*args, **kwargs)
   
    def __str__(self):
        return self.email


class MenuItem(models.Model):
    """Model representing items on the restaurant menu (pizzas, drinks, etc.)"""
    CATEGORY_CHOICES = [
        ('pizza', 'Pizza'),
        ('pasta', 'Pasta'),
        ('salad', 'Salad'),
        ('drink', 'Drink')
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} (${self.price})"


class Order(models.Model):
    """Model representing a customer order"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    
    order_number_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    delivery_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    payu_order_id = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} ({self.status})"
    
    def calculate_total(self):
        """Calculate total amount from order items"""
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save()
        return total


class OrderItem(models.Model):
    """Model representing individual items within an order"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    subtotal = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.menu_item.price * self.quantity
        super().save(*args, **kwargs)
