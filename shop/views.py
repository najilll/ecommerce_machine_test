from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User
from web.models import Order, Product
from mixins import CustomLoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView


# Create your views here.
class HomeView(CustomLoginRequiredMixin,View):
    permissions = ['staff']
    def get(self, request):
        user = User.objects.all()
        context={
            'users':user
        }
        return render(request, "dashboard/shop_index.html",context)
    

# products  
class ProductCreate(CustomLoginRequiredMixin, CreateView):
    model = Product
    template_name = "dashboard/products/product_form.html"
    fields="__all__"
    permissions = ['staff']
    success_url = reverse_lazy('shop:product_list',)


class ProductList(CustomLoginRequiredMixin, ListView):
    model = Product
    template_name = "dashboard/products/product_list.html"
    permissions = ['staff']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Products"
        return context


class ProductDetail(CustomLoginRequiredMixin, DetailView):
    model = Product
    template_name = "dashboard/products/product_detail.html"
    permissions = ['staff']


class ProductUpdate(CustomLoginRequiredMixin, UpdateView):
    model = Product
    template_name = "dashboard/products/product_form.html"
    permissions = ['staff']
    fields = "__all__"
    success_url = reverse_lazy('shop:product_list',)


class ProductDelete(CustomLoginRequiredMixin, DeleteView):
    model = Product
    template_name = "dashboard/products/product_delete.html"
    permissions = ['staff']
    # success_url = "shop/product_list/"
    success_url = reverse_lazy('shop:product_list',)


#orders
class OrderList(CustomLoginRequiredMixin, ListView):
    model = Order
    template_name = "dashboard/orders/order_list.html"
    permissions = ['staff']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Orders"
        return context
    

class OrderDetail(CustomLoginRequiredMixin, DetailView):
    model = Order
    template_name = "dashboard/orders/order_detail.html"
    permissions = ['staff']


class OrderUpdate(CustomLoginRequiredMixin, UpdateView):
    model = Order
    template_name = "dashboard/orders/order_form.html"
    fields = "__all__"
    permissions = ['staff']
    success_url = reverse_lazy('shop:order_list')


class OrderDelete(CustomLoginRequiredMixin, DeleteView):
    model = Order
    template_name = "dashboard/orders/order_delete.html"
    permissions = ['staff']
    success_url = reverse_lazy('shop:order_list')
    
