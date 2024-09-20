from api.operation.repository.operation_repository import (
    OperationRepository,
)


class OperationFactory:
    @staticmethod
    def create_operation_and_auction(
        amount, topic, description, anual_rate, end_date, user_id
    ):

        return OperationRepository().create_operation_and_auction(
            amount, topic, description, anual_rate, end_date, user_id
        )
