from rest_framework import serializers

from .models import UserCustom

class UserCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        fields = ["id", "username", "dni", "rol","email"]
        extra_kwargs = {
            "password": {"required": {"write_only": True}},
        } 