from django.urls import path, include
from .views import PaymeCallBackAPIView, confirm_product
from .auth import UserRegister, Login

urlpatterns = [
    path('payme/callback', PaymeCallBackAPIView.as_view()),
    path('click/', include('click_api.urls')),
    path("confirm-product/", confirm_product),

    path("register/", UserRegister.as_view()),
    path("login/", Login.as_view())
]
