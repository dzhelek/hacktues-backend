# Generated by Django 3.1 on 2021-02-27 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wave3', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='elsys',
            field=models.SmallIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='free',
            field=models.TextField(),
        ),
    ]
