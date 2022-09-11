from django import forms

from .models import IncreaseRecord, SaleRecord


class IncreaseRecordForm(forms.ModelForm):
    class Meta:
        model = IncreaseRecord
        fields = ("amount",)


class SaleRecordForm(forms.ModelForm):
    class Meta:
        model = SaleRecord
        fields = ("phone_number", "amount",)
