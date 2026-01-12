from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Keeping standard AbstractUser fields for name (first_name, last_name)
    # but we can access full name via get_full_name()

    def __str__(self):
        return self.username
