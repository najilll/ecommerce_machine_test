from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Cart, Order, OrderItem, Product

# Create your views here.
class HomeView(View):
    def get(self, request):
        context={
            "products":Product.objects.all()
        }
        
        return render(request, "web/index.html",context)
    
class CartView(LoginRequiredMixin, View):
    template_name = "web/cart.html"

    def get(self, request):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)
        cart_total = float(sum(item.get_total_price() for item in Cart.objects.filter(user=user)))

        context = {
            "cart_items": cart_items,
            "cart_total": cart_total,
        }
        return render(request, self.template_name, context)


class AddToCartView(View,LoginRequiredMixin):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'User not authenticated'}, status=401)
        user = self.request.user
        quantity = request.GET.get('quantity', 1)
        is_cart=request.GET.get("update",'')
        print(is_cart,"==========")
        product_id = request.GET.get("product_id",'')
        product = get_object_or_404(Product, pk=product_id)

        cart_item, created = Cart.objects.get_or_create(
            user=user,
            product=product,
            defaults=({"quantity": quantity})
        )

        if not created:
            if is_cart:
                cart_item.quantity = int(quantity)
            else:
                cart_item.quantity += int(quantity)
            cart_item.save()
        return JsonResponse({
            'message': 'Product Quantity Added from cart successfully',
            'quantity':cart_item.quantity,
            'total_price':cart_item.get_total_price(),
            'cart_total':cart_item.cart_total(),
            'cart_count':Cart.objects.filter(user=request.user).count(),
            'image_url': product.image.url,
            'product_name': product.name,
        })


class RemoveCartItemView(LoginRequiredMixin, View):
    def get(self, request, cart_item_id, *args, **kwargs):
        user = self.request.user
        cart_item = get_object_or_404(Cart, id=cart_item_id, user=user)
        cart_item.delete()
        return redirect("web:cart")


class MinusCartView(LoginRequiredMixin,View):
   def get(self, request):
        try:
            cart_id = request.GET.get("cart_id")
            cart_item = Cart.objects.get(id=cart_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
            return JsonResponse({'message': 'Product Quantity decreased from cart successfully','quantity':cart_item.quantity,'total_price':cart_item.get_total_price(),'cart_total':cart_item.cart_total()})
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Product not found in cart'}, status=404)

class ClearCartView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        user = request.user
        Cart.objects.filter(user=user).delete()
        return redirect('web:cart')
    
class CheckoutView(View):
    def get(self, request):
        return render(request, "web/checkout.html")
    
class CheckoutView(LoginRequiredMixin,View):
    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        cart_total = sum(item.get_total_price() for item in cart_items)
        order_form = OrderForm()
        context = {
            "cart_items": cart_items,
            "cart_total": cart_total,
            "order_form": order_form,
        }
        return render(request, "web/checkout.html", context)

    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = user
            order.save()  # Save the order

            # Calculate payable amount after ensuring there are items in the cart
            cart_total = sum(item.get_total_price() for item in cart_items)
            order.payable = cart_total
            order.save() 

            # Create order items
            for item in cart_items:
                order_item = OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.sale_price,
                    quantity=item.quantity
                )
            cart_items.delete()  # Clear the cart
            
            return redirect('web:index')
              # Redirect to a success page
        else:
            print(order_form.errors)
            context = {
                "order_form": order_form,
                "cart_items": cart_items,
                "cart_total": sum(item.get_total_price() for item in cart_items),
            }
            return render(request, "web/checkout.html", context)
        

class OrderStatusView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        order_items = OrderItem.objects.filter()
        context = {
            'orders': orders,
            'order_items': order_items
        }
        return render(request, 'web/order_status.html', context)
    
class OrderItemsView(LoginRequiredMixin,View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        context = {
            'order': order,
        }
        return render(request, 'web/update_order_status.html', context)

    # def post(self, request, order_id):
    #     order = get_object_or_404(Order, id=order_id, user=request.user)
    #     form = OrderForm(request.POST, instance=order)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('web:order_status')  # Redirect to order status page
    #     context = {
    #         'form': form,
    #         'order': order
    #     }
    #     return render(request, 'web/index.html', context)