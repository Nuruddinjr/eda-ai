from django.urls import path, include
from .views import PaymeCallBackAPIView, confirm_product
from .auth import UserRegister, VerifyOtp,  UserTries

urlpatterns = [
    path('payme/callback', PaymeCallBackAPIView.as_view()),
    path('click/', include('click_api.urls')),
    path("confirm-product/", confirm_product),

    path("auth-one/", UserRegister.as_view()),
    path("auth-two/", VerifyOtp.as_view()),

    path("user-tries/", UserTries.as_view()),


]
