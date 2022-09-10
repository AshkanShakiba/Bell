from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Seller


class SellerCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Seller
        fields = ("account_number", "name", "username")


class SellerChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = Seller
        fields = ("account_number", "name", "username")
