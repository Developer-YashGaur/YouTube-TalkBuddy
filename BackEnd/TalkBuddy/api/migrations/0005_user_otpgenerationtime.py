# Generated by Django 5.0.3 on 2024-04-04 17:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_user_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otpGenerationTime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 4, 4, 17, 18, 15, 703091)),
        ),
    ]