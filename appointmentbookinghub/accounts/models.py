from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("patient", "Patient"),
        ("specialist", "Specialist"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
