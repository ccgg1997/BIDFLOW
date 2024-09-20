from django.contrib.auth.models import AbstractUser
from django.db import models


class UserCustom(AbstractUser):
    dni = models.CharField(max_length=14, unique=False)
    ROL_CHOICES = [
        ("investor", "Investor"),
        ("operator", "Operator"),
    ]
    rol = models.CharField(
        max_length=8, choices=ROL_CHOICES, default=""
    )

    def __str__(self):
        return f"{self.username} - {self.rol}"
