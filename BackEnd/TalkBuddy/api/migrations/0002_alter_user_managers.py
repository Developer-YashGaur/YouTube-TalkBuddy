# Generated by Django 5.0.3 on 2024-04-02 12:28

import api.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', api.models.CustomUserManager()),
            ],
        ),
    ]
