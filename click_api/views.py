from . import Services
from . import utils
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def prepare(request):
    print("*************CLICK***************")
    print(request.POST)
    print("*************CLICK***************")
    return utils.prepare(request)


@csrf_exempt
def complete(request):
    print("*************CLICK***************")
    print(request.POST)
    print("*************CLICK***************")
    return utils.complete(request)


@csrf_exempt
def service(request, service_type):
    print("*************CLICK***************")
    print(request.POST)
    print(service_type)
    print("*************CLICK***************")
    service = Services(request.POST, service_type)
    return JsonResponse(service.api())



from rest_framework.permissions import BasePermission
from rest_framework.views import APIView

from admin import settings


#
class PyClickMerchantAPIView(APIView):
    authentication_classes = []
    permission_classes = [BasePermission, ]
    VALIDATE_CLASS = None

    @staticmethod
    def generate_url(order_id, amount, return_url=None):
        service_id = settings.PAYMENT_VARIANTS["click"][1]['merchant_service_id']
        merchant_id = settings.PAYMENT_VARIANTS["click"][1]['merchant_id']
        url = f"https://my.click.uz/services/pay?service_id={service_id}&merchant_id={merchant_id}&amount={amount}&transaction_param={order_id}"
        if return_url:
            url += f"&return_url=http://159.89.107.246"
        return url
