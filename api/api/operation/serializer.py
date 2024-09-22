from datetime import datetime, timedelta

from rest_framework import serializers

from api.operation.factory.operation_factory import OperationFactory
from api.operation.repository.operation_repository import (
    OperationRepository,
)
from api.user_custom.models import UserCustom

from .models import Operation

USER_TYPE_OPERATOR = "operator"


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = [
            "id",
            "amount",
            "topic",
            "description",
            "anual_rate",
            "end_date",
        ]

    def validate(self, data):
        request = self.context.get("request")
        user = UserCustom.objects.get(id=request.data["user"])

        if str(user.rol) != USER_TYPE_OPERATOR:
            raise serializers.ValidationError(
                str("The investor can't create an operation.")
            )

        if data["amount"] <= 0:
            raise serializers.ValidationError(
                "The amount must be greater than zero."
            )

        if not (0 < float(data["anual_rate"]) <= 1):
            raise serializers.ValidationError(
                "Anual Rate must be between 0.0 and 1.0"
            )

        if data["end_date"] < datetime.now().date() + timedelta(days=1):
            raise serializers.ValidationError(
                "All project have a minimum of 1 day in advance."
            )

        return data

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            user = UserCustom.objects.get(id=request.data["user"])
            operation = OperationFactory.create_operation_and_auction(
                amount=validated_data["amount"],
                topic=validated_data["topic"],
                description=validated_data["description"],
                anual_rate=validated_data["anual_rate"],
                end_date=validated_data["end_date"],
                user_id=user.id,
            )
            return operation
        except Exception as e:
            raise serializers.ValidationError(
                "Can't create an operation." + str(e)
            )


class OperationSerializerListInfo(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ["id", "amount", "end_date"]

    def fetch_active_operation():
        return OperationRepository().fetch_open_operations()

    def fetch_operation_id(id):
        return OperationRepository().fetch_operation_by_id(id)


class OperationSerializerInfo(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = [
            "id",
            "amount",
            "topic",
            "description",
            "anual_rate",
            "end_date",
            "status",
        ]

    def fetch_active_operation():
        return OperationRepository().fetch_open_operations()

    def fetch_operation_id(id):
        return OperationRepository().fetch_operation_by_id(id)
