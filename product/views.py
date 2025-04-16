from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product/product_detail.html', {'product': product})

def navbar_partial(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'includes/navbar.html', context)

def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'includes/category.html', context)