from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.http import JsonResponse


from account.models import Address
from product.models import Product
from .cart_modules import Cart
from .forms import DiscountForm
from .models import Order, OrderItem, DiscountCode


def cart_detail_view(request):
    if request.method == 'GET':
        cart = Cart(request)
        return render(request, "cart/cart_detail.html", {'cart': cart})

# def cart_item_count(request):
#     count = 0
#     if request.user.is_authenticated:
#         try:
#             order = Order.objects.get(user=request.user, is_paid=False)
#             count = order.item.count()
#         except Order.DoesNotExist:
#             pass
#     return {'cart_item_count': count}

def cart_add_view(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=pk)
        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = request.POST.get('quantity')
        cart = Cart(request)
        cart.add(product, quantity, color, size)
        return redirect("cart:cart_detail")


def cart_remove_view(request, pk):
    if request.method == 'GET':
        cart = Cart(request)
        cart.remove(pk)
        return redirect("cart:cart_detail")


@login_required
def order_detail(request, id):
    if request.method == "GET":
        order = get_object_or_404(Order, id=id, user=request.user)
        return render(request, 'cart/order_detail.html', {'order': order})


@login_required
def order_creation(request):
    if request.method == "GET":
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=cart.total())
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], color=item['color'],
                                     size=item['size'], quantity=item['quantity'], price=item['price'])

        cart.remove_cart()
        return redirect("cart:order_detail", id=order.id)


class ApplyDiscountView(View):
    def post(self, request, pk):
        form = DiscountForm(request.POST)
        order = get_object_or_404(Order, id=pk)

        if form.is_valid():
            code = form.cleaned_data['discount_code']

            try:
                discount = DiscountCode.objects.get(name=code)

                if not discount.is_active or discount.quantity == 0:
                    messages.error(request, "This discount code is inactive or out of stock.")
                    return redirect("cart:order_detail", id=order.id)

                if discount.expires_at and timezone.now() > discount.expires_at:
                    messages.error(request, "This discount code has expired.")
                    return redirect("cart:order_detail", id=order.id)

                if discount.discount <= 0 or discount.discount > 100:
                    messages.error(request, "Invalid discount percentage.")
                    return redirect("cart:order_detail", id=order.id)

                discount_rate = Decimal(discount.discount) / 100
                discount_amount = order.total_price * discount_rate
                order.total_price = max(order.total_price - discount_amount, 0)
                order.save()

                discount.quantity -= 1
                discount.save()

                messages.success(request, f"Discount code '{discount.name}' applied successfully!")

            except DiscountCode.DoesNotExist:
                messages.error(request, "Discount code not found.")
        else:
            messages.error(request, "Invalid input.")

        return redirect("cart:order_detail", id=order.id)


@login_required
def fake_payment_view(request, pk):
    order = get_object_or_404(Order, id=pk, user=request.user)
    order.is_paid = True
    order.save()
    return redirect('cart:order_detail', id=order.id)


@login_required
def fake_verify_view(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return render(request, 'cart/payment_failed.html', {'message': 'Order not found'})

    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.is_paid = True
    order.save()
    return render(request, 'cart/payment_success.html', {'order': order})


@login_required
def payment_view(request, pk):
    order = get_object_or_404(Order, id=pk, user=request.user)
    if order.is_paid:
        return redirect('cart:order_detail', id=order.id)

    request.session['order_id'] = order.id
    return render(request, 'cart/payment.html', {'order': order})
