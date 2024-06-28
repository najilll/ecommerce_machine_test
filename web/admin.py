from django.contrib import admin

from .models import OrderItem, Product,Order

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("full_name",)
    search_fields = ("full_name",)
    inlines = [OrderItemInline]