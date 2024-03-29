from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.views import View
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response

from sellers.models import Seller
from pages import views as home_view
from .models import IncreaseRecord, SaleRecord
from .forms import IncreaseRecordForm, SaleRecordForm


class IncreaseGet(LoginRequiredMixin, TemplateView):
    template_name = "increase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = IncreaseRecordForm()
        return context


class IncreasePost(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = IncreaseRecord
    form_class = IncreaseRecordForm
    template_name = "increase.html"

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        record = form.save(commit=False)
        record.seller = self.request.user
        record.save()
        if record.completed:
            home_view.set_message("increase credit done successfully")
        else:
            home_view.set_message("increase credit failed, server-side error")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("home")


class IncreaseView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = IncreaseGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = IncreasePost.as_view()
        return view(request, *args, **kwargs)


class SaleGet(LoginRequiredMixin, TemplateView):
    template_name = "sale.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SaleRecordForm()
        return context


class SalePost(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = SaleRecord
    form_class = SaleRecordForm
    template_name = "sale.html"

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        record = form.save(commit=False)
        record.seller = self.request.user
        record.save()
        if record.completed:
            home_view.set_message("sale credit done successfully")
        else:
            if record.amount > record.seller.credit:
                home_view.set_message("sale credit failed, not enough credit")
            else:
                home_view.set_message("sale credit failed, server-side error")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("home")


class SaleView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = SaleGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = SalePost.as_view()
        return view(request, *args, **kwargs)


@api_view(["GET"])
def credit_api_view(request):
    if request.user.is_confirmed:
        seller = request.user
        return Response({"credit": seller.credit}, status=200)
    else:
        return Response({"detail": "please wait until bell's administrator confirm your account."}, status=403)


@transaction.atomic
@api_view(["POST"])
def increase_api_view(request):
    data = request.data

    response = check_increase_validations(request.user, data)

    if response is not None:
        return response

    amount = data["amount"]

    with transaction.atomic():
        record = IncreaseRecord.objects.create(
            amount=amount,
            seller=Seller.objects.select_for_update().get(id=request.user.id),
        )

    if record.completed:
        response = Response({"credit": request.user.credit, "detail": "increase credit done successfully"}, status=200)
    else:
        response = Response({"detail": "increase credit failed", "error": "server-side error"}, status=500)

    return response


def check_increase_validations(seller, data):
    if seller.is_confirmed:
        amount = data["amount"]
        if isinstance(amount, int) and amount > 0:
            return None
        else:
            return Response({"detail": "increase credit failed", "error": "amount must be a positive integer"},
                            status=400)
    else:
        return Response({"detail": "please wait until bell's administrator confirm your account."}, status=403)


@transaction.atomic
@api_view(["POST"])
def sale_api_view(request):
    data = request.data

    response = check_increase_validations(request.user, data)

    if response is not None:
        return response

    amount = data["amount"]
    phone_number = data["phone_number"]

    with transaction.atomic():
        record = SaleRecord.objects.create(
            amount=amount,
            seller=Seller.objects.select_for_update().get(id=request.user.id),
            phone_number=phone_number,
        )

    if record.completed:
        return Response({"credit": request.user.credit, "detail": "sale credit done successfully"}, status=200)
    else:
        if amount > request.user.credit:
            return Response({"detail": "sale credit failed", "error": "not enough credit"}, status=400)
        else:
            return Response({"detail": "sale credit failed", "error": "server-side error"}, status=500)


def check_sale_validations(seller, data):
    if seller.is_confirmed:
        amount = data["amount"]
        phone_number = data["phone_number"]
        if isinstance(amount, int) and amount > 0:
            if isinstance(phone_number, str):
                return None
            else:
                return Response({"detail": "sale credit failed", "error": "phone_number must be a string"}, status=400)
        else:
            return Response({"detail": "sale credit failed", "error": "amount must be a positive integer"}, status=400)
    else:
        return Response({"detail": "please wait until bell's administrator confirm your account."}, status=403)
