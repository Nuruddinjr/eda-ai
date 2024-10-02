from django.contrib import admin
from .models import Order, Payment, AccessToken, Users, SmsModel


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "amount", "is_finished", "is_canceled", "status_type", "type", "message"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.fields]


admin.site.register(AccessToken)
admin.site.register(Users)
admin.site.register(SmsModel)
