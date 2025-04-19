from django.shortcuts import render

from django.shortcuts import render, get_object_or_404 , redirect
from django.views.generic import ListView

from .models import Product, Category , Comment , ProductLike
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductForm




def all_products(request):
    products = Product.objects.all()  # Get all products
    return render(request, 'product/products_list.html', {'products': products})

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    top_level_comments = product.comments.filter(parent__isnull=True).select_related('user').prefetch_related('replies__user')

    # Count the number of likes for the product
    like_count = ProductLike.objects.filter(product=product, liked=True).count()

    # Check if the current user has liked the product
    user_liked = ProductLike.objects.filter(product=product, user=request.user).exists() if request.user.is_authenticated else False

    return render(request, 'product/product_detail.html', {
        'product': product,
        'comments': top_level_comments,
        'like_count': like_count,  # Add like count (integer) to the context
        'user_liked': user_liked,  # Add whether the user has liked the product
    })

def navbar_partial(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'includes/navbar.html', context)

def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'includes/categories.html', context)

def all_categories(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 9)  # 9 categories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/category_list.html', {'page_obj': page_obj})

# Category Detail View with Pagination for Products
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)
    paginator = Paginator(products, 9)  # 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/category_detail.html', {
        'category': category,
        'page_obj': page_obj
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
        sort = request.GET.get('sort')  # Get sort query param

        queryset = Product.objects.all()

        if colors:
            queryset = queryset.filter(color__title__in=colors).distinct()

        if sizes:
            queryset = queryset.filter(size__title__in=sizes).distinct()

        if min_price and max_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        # ✅ Apply sorting if specified
        if sort == 'latest':
            queryset = queryset.order_by('-created_at')  # Replace with your actual datetime field
        elif sort == 'most_expensive':
            queryset = queryset.order_by('-price')
        elif sort == 'most_cheap':
            queryset = queryset.order_by('price')

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



@login_required
def like_product(request, pk):
    try:
        # Try to get an existing like, if exists
        like = ProductLike.objects.get(product_id=pk, user_id=request.user.id)
        # If it exists, delete the like (unlike action)
        ProductLike.liked = False
        like.delete()
    except ProductLike.DoesNotExist:
        # If the like doesn't exist, create a new like (like action)
        ProductLike.objects.create(product_id=pk, user_id=request.user.id)
        ProductLike.liked = True

    # Redirect to product detail page using pk
    return redirect('product:product-detail', pk=pk)


@login_required
@user_passes_test(lambda u: u.is_seller)
def manage_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'product/manage_products.html', {'products': products})



def is_seller(user):
    return hasattr(user, 'is_seller') and user.is_seller

@login_required
@user_passes_test(is_seller)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Assign logged-in user as seller
            product.save()
            form.save_m2m()  # Save many-to-many data
            return redirect('product:products_list')  # Change this to your desired redirect
    else:
        form = ProductForm()
    return render(request, 'product/add_product.html', {'form': form})

