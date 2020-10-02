from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """ A custom user model """

    email = models.EmailField(blank=False, max_length=100,
                              verbose_name='email address')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
