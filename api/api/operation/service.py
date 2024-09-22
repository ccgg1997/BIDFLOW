from django.core.exceptions import ValidationError

from api.operation.factory.operation_factory import OperationFactory
from api.operation.repository.operation_repository import (
    OperationRepository,
)

USER_TYPE_OPERATOR = "operator"


class OperationService:

    @staticmethod
    def validate_user(user_rol):
        if user_rol != USER_TYPE_OPERATOR:
            raise ValidationError(
                "The investor can't create an operation."
            )

    @staticmethod
    def create_operation(data, user):
        try:
            operation = OperationFactory.create_operation_and_auction(
                amount=data["amount"],
                topic=data["topic"],
                description=data["description"],
                anual_rate=data["anual_rate"],
                end_date=data["end_date"],
                user_id=user.id,
            )
            return operation
        except Exception:
            raise ValidationError(
                "Problem in Operation service. Can't create operation."
            )

    @staticmethod
    def fetch_active_operations():
        try:
            return OperationRepository().fetch_open_operations()
        except Exception:
            raise ValidationError(
                "Problem in Operation service. Can't fetch active operations."
            )

    @staticmethod
    def fetch_operation_by_id(id):
        try:
            return OperationRepository().fetch_operation_by_id(id)
        except Exception:
            raise ValidationError(
                "Problem in Operation service. Can't fetch operation by id."
            )
