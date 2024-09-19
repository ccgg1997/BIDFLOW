from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils import timezone

from api.operation.models import Operation


class OperationRepository:

    @staticmethod
    def create_operation(
        amount, topic, description, anual_rate, end_date, user_id
    ):
        operation = Operation(
            amount=amount,
            topic=topic,
            description=description,
            anual_rate=anual_rate,
            end_date=end_date,
            user_id=user_id,
        )
        try:
            operation.save()
            return operation
        except Exception as e:
            return f"Error occurred during save operation: {e}"

    @staticmethod
    def fetch_open_operations():
        try:
            operaciones = get_list_or_404(
                Operation.objects.filter(
                    status=True, end_date__gte=timezone.now()
                )
            )
            return operaciones
        except Http404:
            return []

    @staticmethod
    def fetch_operation_by_id(operation_id):
        try:
            operation = get_object_or_404(Operation, id=operation_id)
            return operation
        except Operation.DoesNotExist:
            return None

    @staticmethod
    def update_operation(operation_id, end_date=None, amount=None):
        if end_date is None and amount is None:
            return None
        if end_date is not None:
            return Operation.get(
                id=operation_id
            ).update_operation_end_date(operation_id, end_date)
        if amount is not None:
            return Operation.get(
                id=operation_id
            ).update_operation_amount(operation_id, amount)

    @staticmethod
    def delete(operation_id, user_id):
        try:
            operation = get_object_or_404(Operation, id=operation_id)
            if operation.user_id != user_id:
                return None

            operation.delete()
            return operation
        except Operation.DoesNotExist:
            return None
