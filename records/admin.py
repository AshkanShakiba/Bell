from django.contrib import admin

from .models import IncreaseRecord, SaleRecord


class IncreaseRecordAdmin(admin.ModelAdmin):
    list_display = (
        "seller",
        "amount",
        "date",
        "completed",
    )


class SaleRecordAdmin(admin.ModelAdmin):
    list_display = (
        "seller",
        "amount",
        "phone_number",
        "date",
        "completed",
    )


admin.site.register(IncreaseRecord, IncreaseRecordAdmin)
admin.site.register(SaleRecord, SaleRecordAdmin)
