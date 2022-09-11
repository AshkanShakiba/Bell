from django.urls import path

from .views import IncreaseView, SaleView

urlpatterns = [
    path("increase/", IncreaseView.as_view(), name="increase"),
    path("sale/", SaleView.as_view(), name="sale"),
]
