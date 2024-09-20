from django.db import models


class Auction(models.Model):
    """
    Model to represent an auction for an operation
    """

    operation = models.OneToOneField(
        "operation.Operation", on_delete=models.CASCADE
    )
    remaining_amount = models.DecimalField(
        max_digits=20, decimal_places=2
    )

    def __str__(self):
        return (
            f"Auction for operationID: {self.operation.id} - "
            f"Remaining: {self.remaining_amount}"
            f"Initial_amount: {self.operation.amount}"
        )
