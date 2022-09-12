from django.urls import path

from .views import IncreaseView, SaleView, increase_api_view, sale_api_view

urlpatterns = [
    path("increase/", IncreaseView.as_view(), name="increase"),
    path("sale/", SaleView.as_view(), name="sale"),
    path("api/v1/increase/", increase_api_view, name="increase_api"),
    path("api/v1/sale/", sale_api_view, name="sale_api"),
]
