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


class Offert(models.Model):
    """
    Model to represent an Offert for an auction,"
    "this model is related to the User model"
    "and the Auction model (in the actual solution"
    "an auction can have multiple offerts)
    """

    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    rate_wished = models.DecimalField(max_digits=3, decimal_places=2)
    user = models.ForeignKey(
        "user_custom.UserCustom", on_delete=models.CASCADE
    )
    auction = models.ForeignKey(
        "auction.Auction", on_delete=models.CASCADE, related_name='offers'
    )
