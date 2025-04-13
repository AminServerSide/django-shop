from django.shortcuts import render, redirect ,get_object_or_404
from django.views import View
from product.models import Product
from .cart_modules import Cart

def cart_detail_view(request):
    if request.method == 'GET':
        cart = Cart(request)
        return render(request, "cart/cart_detail.html" , {'cart':cart})



def cart_add_view(request , pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=pk)
        size , color , quantity = request.POST.get('size'), request.POST.get('color') , request.POST.get('quantity')
        cart = Cart(request)
        cart.add(product , size , color , quantity)
        return redirect("cart:cart_detail")
