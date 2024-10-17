# Generated by Django 5.1 on 2024-10-17 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_doctitle_type_feepayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='feepayment',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='feepayment',
            name='student_name',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
