from django.urls import path
from django.views.generic import TemplateView
from django.urls import path, include  

from . import views

app_name = "web"

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/add/", views.AddToCartView.as_view(), name="add_to_cart"),
    path("cart/remove/<int:cart_item_id>/",views.RemoveCartItemView.as_view(),name="remove_cart_item"),
    path('cart/minus/', views.MinusCartView.as_view(), name='minus_to_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order-status/', views.OrderStatusView.as_view(), name='order_status'),
    path('order-product/<int:order_id>/', views.OrderItemsView.as_view(), name='order_product'),
]
