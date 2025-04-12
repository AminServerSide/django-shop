from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product/product_detail.html', {'product': product})