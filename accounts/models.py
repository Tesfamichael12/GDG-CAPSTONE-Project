from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Ensures email is unique for each user
    bio = models.TextField(blank=True, null=True)  # Optional bio field

    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    # To specify the username field for authentication (username is the default)
    USERNAME_FIELD = 'username'

    # Fields required for creating a superuser (this is required)
    REQUIRED_FIELDS = ['email']


    def __str__(self):
        return self.username  # Return the username as the string representation

    """ Customizing related_name to avoid reverse accessor clashes """
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # This avoids clashing with the default 'user_set'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # This avoids clashing with the default 'user_permissions'
    )