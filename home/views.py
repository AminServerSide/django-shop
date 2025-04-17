from django.shortcuts import render
from django.views.generic import TemplateView
from product.models import Product, Category

class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Store something in the session (optional)
        self.request.session['my_name'] = 'name'

        # Last 9 products
        context['object_list'] = Product.objects.order_by('-id')[:9]


        context['categories'] = Category.objects.order_by('-id')[:9]

        return context
