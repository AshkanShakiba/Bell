from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SellerCreationForm, SellerChangeForm
from .models import Seller


class SellerAdmin(UserAdmin):
    add_form = SellerCreationForm
    form = SellerChangeForm
    model = Seller
    list_display = [
        "username",
        "name",
        "credit",
        "is_confirmed",
    ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("name", "credit", "is_confirmed", "account_number")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("name", "credit", "is_confirmed", "account_number")}),)


admin.site.register(Seller, SellerAdmin)
