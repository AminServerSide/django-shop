from django.shortcuts import render, redirect ,get_object_or_404
from django.views import View
from product.models import Product


def cart_detail_view(request):
    if request.method == 'GET':
        return render(request, "cart/cart_detail.html" , {})



def cart_add_view(request , pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=pk)
        size , color , quantity = request.POST.get('size'), request.POST.get('color') , request.POST.get('quantity')
        print(size , color , quantity)
        return redirect("cart:cart_detail")
