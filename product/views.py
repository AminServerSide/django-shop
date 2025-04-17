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
    return render(request, 'includes/categories.html', context)

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)
    return render(request, 'product/category_detail.html', {
        'category': category,
        'products': products
    })



def product_list(request):
    colors = request.GET.getlist('color')
    sizes = request.GET.getlist('size')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    queryset = Product.objects.all()

    if colors:
        queryset = queryset.filter(color__title__in=colors).distinct()

    if sizes:
        queryset = queryset.filter(size__title__in=sizes).distinct()

    if min_price and max_price:
        queryset = queryset.filter(price__lte=max_price, price__gte=min_price)

    context = {
        'object_list': queryset
    }

    return render(request, 'product/products_list.html', context)
