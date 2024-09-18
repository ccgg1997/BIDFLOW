from rest_framework import serializers

from api.user_custom.factory.user_factory import UserCustomFactory
from api.user_custom.repository.user_custom_repository import (
    UserCustomRepository,
)

from .models import UserCustom


class UserCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        fields = ["id", "username", "dni", "rol", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        rol = validated_data.get("rol")

        try:
            if rol == "inversor":
                return UserCustomFactory.create_inversor(
                    validated_data["username"],
                    validated_data["dni"],
                    validated_data["email"],
                    validated_data["password"],
                )
            elif rol == "operador":
                return UserCustomFactory.create_operador(
                    validated_data["username"],
                    validated_data["dni"],
                    validated_data["email"],
                    validated_data["password"],
                )
            else:
                raise ValueError("Invalid rol. Options: inversor, operador")
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

    @staticmethod
    def user_auth(username, password):
        try:
            user = UserCustomRepository().get_by_username(username=username)
            if user is not None and user.check_password(password):
                return user
            return None
            return user
        except UserCustom.DoesNotExist:
            return None

    @staticmethod
    def get_all():
        return UserCustomRepository().get_all()
