from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm

from account.models import User, Address

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "is_admin", "is_seller"]  # Added `is_seller` to list_display
    list_filter = ["is_admin", "is_seller"]  # Added `is_seller` to list_filter
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["fullname", "phone"]}),
        ("Permissions", {"fields": ["is_admin", "is_seller"]}),  # Added `is_seller` to Permissions section
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "fullname", "phone", "password1", "password2", "is_seller"],  # Added `is_seller`
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

# Register the Address model
admin.site.register(Address)

# Register the User model with the custom UserAdmin
admin.site.register(User, UserAdmin)

# Unregister the Group model, since we aren't using it for permissions
admin.site.unregister(Group)
