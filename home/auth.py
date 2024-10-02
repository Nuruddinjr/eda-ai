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

        # Check if the user already exists
        user = Users.objects.filter(username=data['username']).first()
        if user:
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate OTP
        otp_code = str(random.randint(100000, 999999))

        # Create OTP entry without user
        otp_entry = SmsModel.objects.create(code=otp_code)

        # Send OTP to the user's phone number
        sms_send(data['username'], otp_code)

        return Response({'message': 'OTP sent to your phone number'}, status=status.HTTP_200_OK)


class VerifyOtp(GenericAPIView):
    def post(self, request):
        data = request.data

        # Check if the OTP is valid for the username
        otp_entry = SmsModel.objects.filter(code=data['otp']).first()
        if not otp_entry:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the OTP has expired
        if timezone.now() - otp_entry.created_at > timedelta(minutes=3):
            otp_entry.delete()  # Clean up expired OTP
            return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user now that OTP is confirmed
        user = Users.objects.create(username=data['username'])
        otp_entry.delete()  # Clean up OTP entry after use

        # Create a token for the user (optional)
        token = AccessToken.objects.create(user=user)

        return Response({"access_token": token.token}, status=status.HTTP_201_CREATED)


class Login(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data
        phone_number = data.get('username')

        user = Users.objects.filter(username=phone_number).first()
        if not user:
            otp_code = str(random.randint(100000, 999999))

            otp_entry = SmsModel.objects.create(user=user, code=otp_code)

            sms_send(data['username'], otp_code)

            return Response({'message': 'OTP sent to your phone number'}, status=status.HTTP_200_OK)

        return Response({'error': 'Username exists please log in'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyLoginOtp(GenericAPIView):
    def post(self, request):
        data = request.data
        phone_number = data.get('username')
        otp_code = data.get('otp')

        otp_entry = SmsModel.objects.filter(user__username=phone_number, code=otp_code).first()

        if not otp_entry:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() - otp_entry.created_at > timedelta(minutes=3):
            otp_entry.delete()
            return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

        otp_entry.delete()

        user = Users.objects.get(username=phone_number)

        token = AccessToken.objects.get_or_create(user=user)[0]

        return Response({"access_token": token.token}, status=status.HTTP_200_OK)


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
