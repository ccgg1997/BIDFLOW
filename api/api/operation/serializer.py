import logging

from rest_framework import serializers

from api.operation.factory.operation_factory import OperationFactory
from api.operation.repository.operation_repository import (
    OperationRepository,
)
from api.user_custom.models import UserCustom

from .models import Operation

logger = logging.getLogger(__name__)


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = [
            "id",
            "amount",
            "topic",
            "description",
            "anual_rate",
            "start_date",
            "end_date",
            "user",
        ]

    def create(self, validated_data):
        try:

            operation = OperationFactory.create_operation(
                amount=validated_data["amount"],
                topic=validated_data["topic"],
                description=validated_data["description"],
                anual_rate=validated_data["anual_rate"],
                end_date=validated_data["end_date"],
                user_id=validated_data["user"].id,
            )
            return operation
        except Exception as e:
            logger.error(
                f"Error in serializer(operation) create method: {e}"
            )
            return None

    def fetch_active_operation():
        return OperationRepository().fetch_open_operations()


class OperationDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ["id", "username"]
