from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.


class User(AbstractUser):
    username_regex = RegexValidator(
        regex='^[a-zA-Z]{6,30}$', message='The username must be between 6 and 30 characters long, and only uppercase and lowercase Latin letters are allowed.')
    username = models.CharField(
        max_length=30, unique=True, validators=[username_regex])
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
