from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from click_api.views import PyClickMerchantAPIView
from home.models import Order, Payment
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from uuid import uuid4
from rest_framework.response import Response
from .services import generate_link
from home.serializers import OrderSerializer

from payme.views import MerchantAPIView
from home.models import OrderTransactionsModel


# from home.modules.avia import ticketed_user_notify
# from home.services.avia import methods as avia_methods
# from home.utils.notify import notify

class PaymeCallBackAPIView(MerchantAPIView):
    def create_transaction(self, order_id, action, *args, **kwargs) -> None:
        # Tranzaktsiya yaratish
        print(f"Tranzaktsiya yaratish uchun order_id: {order_id}, action: {action}")

    def perform_transaction(self, order_id, action, *args, **kwargs) -> None:
        # Tranzaktsiyani tasdiqlash
        print(f"Tranzaktsiya tasdiqlanmoqda: order_id: {order_id}, action: {action}")
        if action == 2:  # Payme tomonidan tasdiqlangan to'lov
            try:
                tr = OrderTransactionsModel.objects.get(order_id=order_id)
                tr.status = True
                tr.is_finished = True
                tr.status_type = OrderTransactionsModel.StatusTypeChoices.confirm
                tr.save(update_fields=["status", "is_finished", "status_type"])

                # Bu yerda to'lov muvaffaqiyati haqida log yoziladi
                print(f"To'lov muvaffaqiyatli yakunlandi: {order_id}")
            except OrderTransactionsModel.DoesNotExist:
                # Agar tranzaktsiya topilmasa, xato chiqariladi
                print(f"Tranzaktsiya topilmadi: {order_id}")

    def cancel_transaction(self, order_id, action, *args, **kwargs) -> None:
        # Tranzaktsiyani bekor qilish
        print(f"Tranzaktsiya bekor qilindi: order_id: {order_id}, action: {action}")
        try:
            tr = OrderTransactionsModel.objects.get(order_id=order_id)
            tr.is_canceled = True
            tr.status_type = OrderTransactionsModel.StatusTypeChoices.cancel
            tr.save(update_fields=["is_canceled", "status_type"])
        except OrderTransactionsModel.DoesNotExist:
            print(f"Bekor qilinadigan tranzaktsiya topilmadi: {order_id}")


# confirm
@swagger_auto_schema(method="post", tags=["booking"], request_body=OrderSerializer,
                     operation_description="")
@api_view(['POST', ])
def confirm_product(request):
    data = request.data
    tr: OrderTransactionsModel = get_object_or_404(Order, order_id=data["order_id"], )
    match data["type"]:
        case "CLICK":
            click_payment = Payment.objects.create(variant="click", transaction_id=str(uuid4()),
                                                   currency="sum", amount=tr.amount)
            return_url = 'https://mysafar.uz/'  # Foydalanuvchini qaytarish kerak bo'lgan URL
            url = PyClickMerchantAPIView.generate_url(order_id=click_payment.id, amount=tr.amount,
                                                      return_url=return_url)
            print(url, "^^^^^^^^^^^^^   url  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            return Response({"payment_url": url})

        case "PAYME":
            tr.type = OrderTransactionsModel.TransferTypeChoices.payme
            tr.save(update_fields=["type"])
            return Response({"url": generate_link(tr.id, tr.amount * 100)})
