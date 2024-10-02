from django.urls import path, include
from .views import PaymeCallBackAPIView, confirm_product
from .auth import UserRegister, VerifyOtp, Login, VerifyLoginOtp

urlpatterns = [
    path('payme/callback', PaymeCallBackAPIView.as_view()),
    path('click/', include('click_api.urls')),
    path("confirm-product/", confirm_product),

    path("register-one/", UserRegister.as_view()),
    path("register-two/", VerifyOtp.as_view()),
    path("login-one/", Login.as_view()),
    path("login-two/", VerifyLoginOtp.as_view()),
]
