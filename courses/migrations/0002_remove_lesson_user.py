# Generated by Django 5.0.4 on 2024-04-24 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='user',
        ),
    ]
