from django.contrib import admin
from payment.models import Payment


@admin.register(Payment)
class payment(admin.ModelAdmin):
    list_display = ["order", "payment_id", "payment_status", "payment_method", "amount"]
    list_filter = ["payment_status"]
    search_fields = ["amount"]
