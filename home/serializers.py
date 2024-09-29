from rest_framework import serializers

from home.models import OrderTransactionsModel, Users


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTransactionsModel
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["username", "name"]

