# Generated by Django 5.1 on 2024-10-13 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_alter_customuser_options_alter_customuser_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='auth_user',
        ),
    ]