from django.urls import path
from django.views.generic import TemplateView
from django.urls import path, include  

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.HomeView.as_view(), name="shop_index"),
    
    path("product_create/", views.ProductCreate.as_view(), name="product_create"),
    path("product_list/", views.ProductList.as_view(), name="product_list"),
    path("product_detail/<str:pk>/", views.ProductDetail.as_view(), name="product_detail"),
    path("product_update/<str:pk>/", views.ProductUpdate.as_view(), name="product_update"),
    path("product_delete/<str:pk>/", views.ProductDelete.as_view(), name="product_delete"),
    #orders
    path("order_list/",views.OrderList.as_view(),name="order_list"),
    path("order_detail/<str:pk>/", views.OrderDetail.as_view(), name="order_detail"),
    path("order_update/<str:pk>/", views.OrderUpdate.as_view(), name="order_update"),
    path("order_delete/<str:pk>/", views.OrderDelete.as_view(), name="order_delete"),
    #login
]