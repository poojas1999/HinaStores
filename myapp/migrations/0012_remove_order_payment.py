# Generated by Django 5.0.1 on 2024-03-21 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_order_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
    ]
