# Generated by Django 5.1 on 2024-11-23 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_is_active_user_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
    ]