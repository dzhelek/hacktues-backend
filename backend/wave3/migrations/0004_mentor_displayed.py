# Generated by Django 3.1 on 2021-03-03 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wave3', '0003_auto_20210227_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='displayed',
            field=models.BooleanField(default=True),
        ),
    ]
