from django.contrib import admin

from home.models import Order as CUSTOM_ORDER
from home.models import Order as DefaultOrderModel

from home.models import MerchantTransactionsModel

if not CUSTOM_ORDER:
    admin.site.register(DefaultOrderModel)

admin.site.register(MerchantTransactionsModel)
