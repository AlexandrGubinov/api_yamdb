from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    bio = models.TextField(
        'Bio',
        blank=True,
    )
    role = models.CharField(
        'Role',
        max_length=32,
        choices=Role.choices,
        default=Role.USER,
    )
    email = models.EmailField(
        'Email',
        max_length=254,
        unique=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
