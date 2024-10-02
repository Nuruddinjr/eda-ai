import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from uuid import uuid4
from payments.models import BasePayment


class Users(AbstractBaseUser, PermissionsMixin):
    class UserType(models.IntegerChoices):
        ADMIN = 1, "ADMIN"
        USER = 2, "USER"

    username = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    tries = models.IntegerField(default=0)
    user_type = models.IntegerField(choices=UserType.choices, default=2)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['user_type']
    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.user_type == self.UserType.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False

        super().save(*args, **kwargs)

        if not self.pk:
            self.generate_access_token()

    def generate_access_token(self):
        token = AccessToken.objects.create(
            user=self
        )
        return token.token


class AccessToken(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Token: {self.token} for User: {self.user.username}'


class SmsModel(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class OrderTransactionsModel(models.Model):
    # Status turi tanlovlari
    class StatusTypeChoices(models.IntegerChoices):
        created = 0, "Created"  # Yaratilgan
        confirm = 1, "Confirm"  # Tasdiqlangan
        cancel = 2, "Cancel"  # Bekor qilingan
        error = 3, "Error"  # Xatolik yuz berdi
        in_progress = 4, "InProgress"  # Jarayonda
        processing = 5, "Processing"  # Qayta ishlash

    # To'lov turi tanlovlari
    class TransferTypeChoices(models.IntegerChoices):
        payme = 0, "PAYME"  # Payme orqali to'lov
        click = 1, "CLICK"  # Click orqali to'lov

    order_id = models.CharField(max_length=255, unique=True, default=uuid4)  # Noyob buyurtma ID
    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # Foydalanuvchi
    amount = models.IntegerField(default=0)  # Umumiy summa
    status = models.BooleanField(default=False)  # To'lov holati
    is_finished = models.BooleanField(default=False)  # Yakunlanganlik holati
    is_canceled = models.BooleanField(default=False)  # Bekor qilinganlik holati
    status_type = models.IntegerField(choices=StatusTypeChoices.choices, default=0)  # Holat turi
    type = models.IntegerField(choices=TransferTypeChoices.choices, null=True, blank=True, default=0)  # To'lov turi
    message = models.TextField(blank=True, default="")  # Xabar maydoni

    def __str__(self):
        return self.tr_id

    def change_status(self, status: str, message=""):  # to'lovning holatini yangilash uchun
        """
        Обновляет статус платежа
        """
        self.status = status
        self.message = message
        self.save(update_fields=["status", "message"])

    def __str__(self) -> str:
        return f"{self.id} - {self.amount}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


# payme
class MerchantTransactionsModel(models.Model):
    """
    MerchantTransactionsModel class \
        That's used for managing transactions in database.
    """
    _id = models.CharField(max_length=255, null=True, blank=False)
    transaction_id = models.CharField(max_length=255, null=True, blank=False,
                                      verbose_name=("Transaction ID"))
    order_id = models.BigIntegerField(null=True, blank=True, verbose_name=("Order ID"))
    amount = models.FloatField(null=True, blank=True, verbose_name=("Amount"))
    time = models.BigIntegerField(null=True, blank=True, verbose_name=("Time"))
    perform_time = models.BigIntegerField(null=True, default=0, verbose_name=("Perform Time"))
    cancel_time = models.BigIntegerField(null=True, default=0, verbose_name=("Cancel Time"))
    state = models.IntegerField(null=True, default=1, verbose_name=("State"))
    reason = models.CharField(max_length=255, null=True, blank=True, verbose_name=("Reason"))
    created_at_ms = models.CharField(max_length=255, null=True, blank=True,
                                     verbose_name=("Created At MS"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=("Updated At"))

    def __str__(self):
        return str(self._id)

    class Meta:
        verbose_name = ("Merchant Transaction")
        verbose_name_plural = ("Merchant Transactions")


Order = OrderTransactionsModel


# click
class Payment(BasePayment):
    """
    click model
    """
    delivery = models.DecimalField(max_digits=9, decimal_places=2, default="0.0", null=True)
    tax = models.DecimalField(max_digits=9, decimal_places=2, default="0.0", null=True)
    description = models.TextField(blank=True, default="", null=True)
    billing_first_name = models.CharField(max_length=256, blank=True, null=True)
    billing_last_name = models.CharField(max_length=256, blank=True, null=True)
    billing_address_1 = models.CharField(max_length=256, blank=True, null=True)
    billing_address_2 = models.CharField(max_length=256, blank=True, null=True)
    billing_city = models.CharField(max_length=256, blank=True, null=True)
    billing_postcode = models.CharField(max_length=256, blank=True, null=True)
    billing_country_code = models.CharField(max_length=2, blank=True, null=True)
    billing_country_area = models.CharField(max_length=256, blank=True, null=True)
    billing_email = models.EmailField(blank=True, null=True)
