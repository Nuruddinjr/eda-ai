from admin import settings
import base64


def generate_link(order_id, amount) -> str:
    """
    GeneratePayLink for each order.
    """
    generated_pay_link: str = "{payme_url}/{encode_params}"
    params: str = 'm={payme_id};ac.{payme_account}={order_id};a={amount};c={call_back_url}'

    params = params.format(
        payme_id=settings.PAYME_ID,
        payme_account=settings.PAYME_ACCOUNT,
        order_id=order_id,
        amount=amount,
        call_back_url=settings.PAYME_CALL_BACK_URL
    )
    encode_params = base64.b64encode(params.encode("utf-8"))
    return generated_pay_link.format(
        payme_url=settings.PAYME_URL,
        encode_params=str(encode_params, 'utf-8')
    )
