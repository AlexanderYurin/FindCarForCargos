# Generated by Django 4.2 on 2024-03-29 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cargo',
            name='car',
        ),
    ]