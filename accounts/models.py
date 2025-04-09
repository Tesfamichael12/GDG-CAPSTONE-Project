from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Ensures email is unique for each user
    bio = models.TextField(blank=True, null=True)  # Optional bio field

    # To specify the username field for authentication (username is the default)
    USERNAME_FIELD = 'username'

    # Fields required for creating a superuser (this is required)
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username  # Return the username as the string representation
