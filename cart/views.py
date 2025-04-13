from django.shortcuts import render
from django.views import View


def cart_detail_view(request):
    if request.method == 'GET':
        return render(request, "cart/cart_detail.html")