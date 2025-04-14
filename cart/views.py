from django.shortcuts import render, redirect ,get_object_or_404
from django.views import View
from product.models import Product
from .cart_modules import Cart
from .models import Order, OrderItem


def cart_detail_view(request):
    if request.method == 'GET':
        cart = Cart(request)
        return render(request, "cart/cart_detail.html" , {'cart':cart})



def cart_add_view(request , pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=pk)
        size , color , quantity = request.POST.get('size'), request.POST.get('color') , request.POST.get('quantity')
        cart = Cart(request)
        cart.add(product , quantity, color, size)
        return redirect("cart:cart_detail")

def cart_remove_view(request , pk):
    if request.method == 'GET':
        cart = Cart(request)
        cart.remove(pk)
        return redirect("cart:cart_detail")

def Order_detail(request , id):
    if request.method == "GET":
        order = get_object_or_404(Order, id=id)
        return render(request , 'cart/order_detail.html' , {'order':order})


def OrderCreation(request):
    if request.method == "GET":
        cart = Cart(request)
        order = Order.objects.create(user=request.user , total_price=cart.total())
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], color=item['color'],
                                     size=item['size'], quantity=item['quantity'] ,  price=item['price'])

        cart.remove_cart()
        return redirect("cart:order_detail" , order.id)








