import hashlib
from admin import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from payments import PaymentStatus
from payments import get_payment_model


def isset(data, columns):
    for column in columns:
        if data.get(column, None):
            return False
    return True


def order_load(payment_id):
    if payment_id is None or not str(payment_id).isdigit():
        return None
    
    if int(payment_id) > 1000000000:
        return None
    
    payment = get_object_or_404(get_payment_model(), id=int(payment_id))
    print(payment, "///////////////////////   payment   ///////////////////////")
    return payment

def click_secret_key():
    PAYMENT_VARIANTS = settings.PAYMENT_VARIANTS
    _click = PAYMENT_VARIANTS['click']
    secret_key = _click[1]['secret_key']
    print(secret_key, "^^^^^^^^^^^^^^^^^ secret_key ^^^^^^^^^^^^^^^")
    return secret_key


def click_webhook_errors(request):
    click_trans_id = request.POST.get('click_trans_id')
    service_id = request.POST.get('service_id')
    click_paydoc_id = request.POST.get('click_paydoc_id')
    order_id = request.POST.get('merchant_trans_id')
    amount = request.POST.get('amount')
    action = request.POST.get('action')
    error = request.POST.get('error')
    error_note = request.POST.get('error_note')
    sign_time = request.POST.get('sign_time')
    sign_string = request.POST.get('sign_string')
    merchant_prepare_id = request.POST.get('merchant_prepare_id') if action == '1' else ''
    
    # So'rov   dagi kerakli ma'lumotlar mavjudligini tekshiramiz
    if isset(request.POST, ['click_trans_id', 'service_id', 'click_paydoc_id', 'amount', 'action', 'error', 'error_note', 'sign_time', 'sign_string']):
        return {
            'error': '-8',
            'error_note': _('Error in request from click')
        }

    # Signaturani tekshirish
    signString = '{}{}{}{}{}{}{}{}'.format(
        click_trans_id, service_id, click_secret_key(), order_id, merchant_prepare_id, amount, action, sign_time
    )
    encoder = hashlib.md5(signString.encode('utf-8'))
    signString = encoder.hexdigest()

    if signString != sign_string:
        return {
            'error': '-1',
            'error_note': _('SIGN CHECK FAILED!')
        }

    # Action tekshiruvi
    if action not in ['0', '1']:
        return {
            'error': '-3',
            'error_note': _('Action not found')
        }

    # Orderni yuklab olish
    transaction = order_load(order_id)
    if not transaction:
        return {
            'error': '-5',
            'error_note': _('Transaction not found')
        }

    # Bu yerda foydalanuvchi kiritgan summa bilan TransactionsModeldagi summa tekshiriladi
    if abs(float(amount) - float(transaction.amount)) > 0.01:
        return {
            'error': '-2',
            'error_note': _('Incorrect parameter amount')
        }

    # Agar to'lov allaqachon tasdiqlangan bo'lsa
    if transaction.status == PaymentStatus.CONFIRMED:
        return {
            'error': '-4',
            'error_note': _('Already paid')
        }

    # Xato holatlarini qaytarish
    if transaction.status == PaymentStatus.REJECTED or int(error) < 0:
        return {
            'error': '-9',
            'error_note': _('Transaction cancelled')
        }

    return {
        'error': '0',
        'error_note': 'Success'
    }


def prepare(request):
    order_id = request.POST.get('merchant_trans_id', None)
    result = click_webhook_errors(request)
    order = order_load(order_id)

    if result['error'] == '0':
        order.status = PaymentStatus.WAITING
        order.save()
    result['click_trans_id'] = request.POST.get('click_trans_id', None)
    result['merchant_trans_id'] = request.POST.get('merchant_trans_id', None)
    result['merchant_prepare_id'] = request.POST.get('merchant_trans_id', None)
    result['merchant_confirm_id'] = request.POST.get('merchant_trans_id', None)

    return JsonResponse(result)


def complete(request):
    order_id = request.POST.get('merchant_trans_id', None)
    order = order_load(order_id)
    result = click_webhook_errors(request)
    if request.POST.get('error', None) != None and int(request.POST.get('error', None)) < 0:
        order.status = PaymentStatus.REJECTED
        order.save()
    if result['error'] == '0':
        order.status = PaymentStatus.CONFIRMED
        order.save()
    result['click_trans_id'] = request.POST.get('click_trans_id', None)
    result['merchant_trans_id'] = request.POST.get('merchant_trans_id', None)
    result['merchant_prepare_id'] = request.POST.get('merchant_prepare_id', None)
    result['merchant_confirm_id'] = request.POST.get('merchant_prepare_id', None)
    return JsonResponse(result)
