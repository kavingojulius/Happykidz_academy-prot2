# Generated by Django 4.2.16 on 2025-01-02 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_delete_classlevel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('term_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('year', models.PositiveIntegerField()),
            ],
        ),
    ]
