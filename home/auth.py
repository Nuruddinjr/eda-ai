from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from home.models import Users, AccessToken
from home.serializers import UserSerializer


class UserRegister(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data

        user = Users.objects.filter(username=data['username']).first()
        if user:
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = AccessToken.objects.create(user=user)
            return Response({"access_token": token.token}, status=status.HTTP_201_CREATED)


class Login(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data
        user = Users.objects.filter(username=data['username']).first()
        if user:
            token = AccessToken.objects.get_or_create(user=user)[0]
            return Response({"access_token": token.token}, status=status.HTTP_201_CREATED)

        return Response({'error': 'Username or password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
