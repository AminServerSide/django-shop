# product/admin.py
from django.contrib import admin
from .models import Size, Color, Category, Product, Information

class SizeAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Columns to display in the list view
    search_fields = ('title',)  # Enable search functionality

class ColorAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Columns to display in the list view
    search_fields = ('title',)  # Enable search functionality

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')  # Display category title and parent
    search_fields = ('title',)  # Enable search functionality
    prepopulated_fields = {'slug': ('title',)}  # Automatically fill slug from the title
    list_filter = ('parent',)  # Allow filtering by parent category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount', 'category_list')  # Display product info
    search_fields = ('title', 'description')  # Enable search functionality
    list_filter = ('category', 'size', 'color')  # Allow filtering by category, size, and color
    filter_horizontal = ('category', 'size', 'color')  # Display many-to-many fields more easily
    readonly_fields = ('image',)  # Make the image field read-only in the admin
    actions = ['apply_discount']  # Custom admin actions

    # Custom method to display the categories associated with the product
    def category_list(self, obj):
        return ", ".join([category.title for category in obj.category.all()])
    category_list.short_description = 'Categories'

    # Custom action to apply a discount to selected products
    def apply_discount(self, request, queryset):
        discount_percentage = request.POST.get('discount_percentage', 0)
        queryset.update(discount=discount_percentage)
        self.message_user(request, f'Discount of {discount_percentage}% applied to selected products.')

    apply_discount.short_description = 'Apply Discount'

class InformationAdmin(admin.ModelAdmin):
    list_display = ('product', 'text')  # Display product and text in the list view
    search_fields = ('text',)  # Enable search functionality

# Register the models with the custom admin classes
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Information, InformationAdmin)
