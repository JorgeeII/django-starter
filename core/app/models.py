from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLES = (
        (1, 'Solutions architect'),
        (2, 'Engineer'),
    )


    age = models.PositiveIntegerField(null=True, blank=True)
    role = models.IntegerField(null=True, choices=ROLES)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
