# Generated by Django 4.2.7 on 2024-01-05 07:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0003_alter_doctor_workdays'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='workStart',
            field=models.TimeField(default=datetime.time(10, 0)),
        ),
    ]
