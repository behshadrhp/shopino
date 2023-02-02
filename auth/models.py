from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from json import load

# Create your models here.


class User(AbstractUser):
    username_regex = RegexValidator(
        regex='^[a-zA-Z]{6,30}$', message='The username must be between 6 and 30 characters long, and only uppercase and lowercase Latin letters are allowed.')
    username = models.CharField(
        max_length=30, unique=True, validators=[username_regex])
    email = models.EmailField(unique=True)

    def clean(self):
        username = self.username
        username_lower = username.lower()

        with open('auth/reserved-username/username.json', 'r') as username:
            reserved_username = load(username)

        for item in reserved_username:
            if username_lower == item:
                raise ValidationError('Sorry, this username is not available')

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
