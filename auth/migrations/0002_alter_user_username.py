# Generated by Django 4.1.3 on 2023-02-02 03:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message='The username must be between 6 and 30 characters long, and only uppercase and lowercase Latin letters are allowed.', regex='^[a-zA-Z]{6,30}$')]),
        ),
    ]