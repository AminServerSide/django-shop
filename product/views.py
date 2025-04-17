from django.shortcuts import render

from django.shortcuts import render, get_object_or_404 , redirect
from django.views.generic import ListView

from .models import Product, Category , Comment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q


from django.core.paginator import Paginator




def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    top_level_comments = product.comments.filter(parent__isnull=True).select_related('user').prefetch_related('replies__user')
    return render(request, 'product/product_detail.html', {
        'product': product,
        'comments': top_level_comments,
    })

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




class ProductListView(ListView):
    template_name = 'product/products_list.html'
    context_object_name = 'object_list'
    paginate_by = 2  # Number of products per page

    def get_queryset(self):
        request = self.request
        colors = request.GET.getlist('color')
        sizes = request.GET.getlist('size')
        min_price = request.GET.get('min-price')
        max_price = request.GET.get('max-price')
        queryset = Product.objects.all()

        if colors:
            queryset = queryset.filter(color__title__in=colors).distinct()

        if sizes:
            queryset = queryset.filter(size__title__in=sizes).distinct()

        if min_price and max_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.copy()
        if 'page' in query:
            del query['page']
        context['query_params'] = query.urlencode()
        return context


def search_products(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(title__icontains=query)
    else:
        products = Product.objects.all()  # Show all products when no query is entered.

    return render(request, 'product/products_list.html', {
        'object_list': products,  # Make sure this matches with the template variable
        'query': query,
    })


@login_required()
def create_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    body = request.POST.get("body")
    parent_id = request.POST.get("parent_id")

    if body:
        parent_comment = (
            Comment.objects.filter(id=parent_id, product=product).first()
            if parent_id else None
        )
        Comment.objects.create(
            product=product,
            user=request.user,
            body=body,
            parent=parent_comment
        )

    # Redirect back to the product detail page
    return redirect('product:product-detail', pk=product.id)



