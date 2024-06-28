from django.db import models
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="product")
    description = models.TextField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    @staticmethod
    def get_list_url():
        return reverse_lazy("main:product_list")

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_product_name(self):
        return self.product

    def get_total_price(self):
        res = float(self.quantity) * float(self.product.sale_price)
        return round(res,2)

    def cart_total(self):
        return float(sum(item.get_total_price() for item in Cart.objects.filter(user=self.user)))

    def __str__(self):
        return f"{self.product} - {self.quantity}"
    
class Order(models.Model):
    PAYMENT_CHOICES=(
        ('cash_on_delivery','cash on delivery'),
        ('online_payment','online payment'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    phone_number=models.IntegerField()
    email=models.EmailField()
    address = models.CharField("Complete Address", max_length=100)
    land_mark=models.CharField(max_length=200, null=True)
    town_city=models.CharField(max_length=200, null=True)
    state=models.CharField(max_length=200, null=True)
    postcode_zip=models.IntegerField()
    country_name=models.CharField(max_length=200, null=True)
    payable = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_methode=models.CharField(max_length=50,choices=PAYMENT_CHOICES)

    payment_status = models.CharField(
        max_length=50,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Failed", "Failed"),
            ("Success", "Success"),
            ("Cancelled", "Cancelled"),
        ),
    )
    order_status = models.CharField(
        max_length=50,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Placed", "Order Placed"),
            ("Shipped", "Order Shipped"),
            ("InTransit", "In Transit"),
            ("Delivered", "Order Delivered"),
            ("Cancelled", "Order Cancelled"),
        ),
    )

    def get_items(self):
        return OrderItem.objects.filter(order=self)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity=models.PositiveIntegerField()


    def get_total(self):
        return self.product.sale_price * self.quantity