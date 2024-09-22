from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import UserCustom
from .service import UserCustomService


class UserCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        fields = ["id", "username", "dni", "rol", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """
        Llamar al servicio para crear un usuario basado en los datos validados.
        """
        try:
            return UserCustomService.create_user(validated_data)
        except ValidationError as e:
            raise serializers.ValidationError({"error": str(e)})


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
