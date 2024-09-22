# serializers.py
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Operation
from .service import OperationService


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
        if data["amount"] <= 0:
            raise ValidationError(
                "The amount must be greater than zero."
            )

        if not (0 < float(data["anual_rate"]) <= 1):
            raise ValidationError(
                "Anual Rate must be between 0.0 and 1.0"
            )

        if data["end_date"] < datetime.now().date() + timedelta(days=1):
            raise ValidationError(
                "All projects must have a minimum of 1 day in advance."
            )

        return data

    def create(self, validated_data):
        try:
            user = self.context.get("user")

            operation = OperationService.create_operation(
                validated_data, user
            )
            return operation
        except Exception as e:
            raise serializers.ValidationError(
                "Can't create an operation. " + str(e)
            )


class OperationSerializerListInfo(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ["id", "amount", "end_date"]


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
