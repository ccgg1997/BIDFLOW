from django.db import transaction
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils import timezone

from api.auction.models import Auction
from api.operation.models import Operation


class OperationRepository:
    @staticmethod
    def create_operation(
        amount, topic, description, anual_rate, end_date, user_id
    ):
        """
        Método privado para crear una operación.
        """
        operation = Operation(
            amount=amount,
            topic=topic,
            description=description,
            anual_rate=anual_rate,
            end_date=end_date,
            user_id=user_id,
        )
        operation.save()
        return operation

    @staticmethod
    def create_auction(operation):
        """
        Método privado para crear una subasta asociada a una operación.
        """
        Auction.objects.create(
            operation=operation, remaining_amount=operation.amount
        )

    @staticmethod
    def create_operation_and_auction(
        amount, topic, description, anual_rate, end_date, user_id
    ):
        """
        Crea una operación y su subasta asociada dentro de una transacción.
        """
        try:
            with transaction.atomic():
                operation = OperationRepository.create_operation(
                    amount,
                    topic,
                    description,
                    anual_rate,
                    end_date,
                    user_id,
                )
                OperationRepository.create_auction(operation)

                return operation
        except Exception as e:
            return f"Error occurred during save operation: {e}"

    @staticmethod
    def fetch_open_operations():
        try:
            operaciones = get_list_or_404(
                Operation.objects.filter(
                    status=True,
                    end_date__gte=timezone.now(),
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
