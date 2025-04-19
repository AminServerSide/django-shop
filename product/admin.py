from django.contrib import admin
from .models import Size, Color, Category, Product, Information, Comment, ProductLike

class SizeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('parent',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount', 'seller', 'category_list')
    search_fields = ('title', 'description', 'seller__fullname')
    list_filter = ('category', 'size', 'color', 'seller')
    filter_horizontal = ('category', 'size', 'color')
    ordering = ('-created',)

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'description',
                'price',
                'discount',
                'image',
                'category',
                'size',
                'color',
                'seller',  # 👈 Added seller field here
            )
        }),
    )

    actions = ['apply_discount']

    def category_list(self, obj):
        return ", ".join([category.title for category in obj.category.all()])
    category_list.short_description = 'Categories'

    def apply_discount(self, request, queryset):
        discount_percentage = request.POST.get('discount_percentage', 0)
        queryset.update(discount=discount_percentage)
        self.message_user(request, f'Discount of {discount_percentage}% applied to selected products.')
    apply_discount.short_description = 'Apply Discount'

class InformationAdmin(admin.ModelAdmin):
    list_display = ('product', 'text')
    search_fields = ('text',)

# Register models
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Information, InformationAdmin)
admin.site.register(Comment)
admin.site.register(ProductLike)
