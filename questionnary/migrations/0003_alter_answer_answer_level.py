# Generated by Django 3.2.1 on 2021-05-05 08:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnary', '0002_alter_choice_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_level',
            field=models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
