from django.db import models
from django.contrib.auth.models import AbstractUser

class UserCustom(AbstractUser):
    dni = models.CharField(max_length=14, unique=True)
    ROL_CHOICES = [
        ("inversor", "Inversor"),
        ("operador", "Operador"),
    ]
    rol = models.CharField(max_length=8, choices=ROL_CHOICES, default="")
    
    def __str__(self):
        return f"{self.username} - {self.rol}"
