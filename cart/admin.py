from django.contrib import admin
from . import models

class OrderItemAdmin(admin.TabularInline):
    model = models.OrderItem




@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user' , "is_paid"]
    inlines = [OrderItemAdmin]
    list_filter = ('is_paid',)


@admin.register(models.DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount', 'quantity', 'is_active', 'expires_at']
    list_filter = ['is_active', 'expires_at']
    search_fields = ['name']
    ordering = ['-expires_at', 'name']
