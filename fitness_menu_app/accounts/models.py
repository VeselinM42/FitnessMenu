from django.db import models

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import models as auth_models


class CustomUser(auth_models.AbstractUser):

    username = models.CharField(
        _("username"),
        max_length=30,
        unique=True,
        help_text=None
    )

    email = models.EmailField(
        _("email address"),
        blank=False,
    )

    profile_picture = models.URLField(
        blank=True,
        null=True,
    )

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'

        return self.first_name or self.last_name
