# Generated by Django 3.1 on 2020-10-04 08:02

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wave2', '0006_auto_20200929_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='team',
            name='github_link',
            field=models.CharField(max_length=400, validators=[django.core.validators.RegexValidator(regex='github.com/.+/.+')]),
        ),
    ]
