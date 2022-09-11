from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.views import View

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
