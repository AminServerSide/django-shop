from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm

from account.models import User, Address, Wallet  # ✅ Imported Wallet

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["email", "is_admin", "is_seller"]
    list_filter = ["is_admin", "is_seller"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["fullname", "phone"]}),
        ("Permissions", {"fields": ["is_admin", "is_seller"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "fullname", "phone", "password1", "password2", "is_seller"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

# ✅ Register models
admin.site.register(User, UserAdmin)
admin.site.register(Address)

# ✅ Wallet admin
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "updated_at")
    search_fields = ("user__email",)

# ✅ Unregister Group
admin.site.unregister(Group)
