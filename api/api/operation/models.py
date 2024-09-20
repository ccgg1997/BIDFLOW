from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


def get_current_date():
    return timezone.now().date()


class Operation(models.Model):
    """
    Model to store the operations
    """

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.01,
        validators=[
            MinValueValidator(
                0.01, message="El monto debe ser mayor que cero."
            )
        ],
    )
    topic = models.CharField(max_length=50, default="General")
    description = models.TextField(blank=True)
    anual_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField(default=get_current_date())
    end_date = models.DateField()
    user = models.ForeignKey(
        "user_custom.UserCustom", on_delete=models.CASCADE, default=1
    )
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.topic} - {self.end_date} - {self.anual_rate}% EA"
