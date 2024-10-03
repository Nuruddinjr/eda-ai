import random
from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from home.helper import sms_send
from home.models import Users, AccessToken, SmsModel
from home.serializers import UserSerializer


class UserRegister(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data

        otp_code = str(random.randint(100000, 999999))
        SmsModel.objects.create(user=data['username'], code=otp_code)
        sms_send(data['username'], otp_code)
        return Response({'message': 'OTP sent to your phone number'}, status=status.HTTP_200_OK)


class VerifyOtp(GenericAPIView):
    def post(self, request):
        data = request.data

        otp_entry = SmsModel.objects.filter(code=data['otp']).first()
        if not otp_entry:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() - otp_entry.created_at > timedelta(minutes=3):
            otp_entry.delete()
            return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

        user_status = Users.objects.filter(username=data['username']).first()

        if user_status:
            token = AccessToken.objects.get_or_create(user=user_status)[0]
            return Response({"access_token": token.token, "login": "success"}, status=status.HTTP_200_OK)

        user = Users.objects.create(username=data['username'])
        token = AccessToken.objects.create(user=user)

        return Response({"access_token": token.token, "register": "success"}, status=status.HTTP_201_CREATED)


class UserTries(GenericAPIView):
    def get(self, request):
        user = Users.objects.get(username=request.user.username)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'user_tries': user.tries}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        user = Users.objects.get(username=data['username'])
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user.tries += 1

        return Response(data={'user_tries': user.tries}, status=status.HTTP_200_OK)
