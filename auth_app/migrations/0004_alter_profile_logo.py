# Generated by Django 5.1.4 on 2025-01-31 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0003_profile_delete_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='media/uploads/'),
        ),
    ]
