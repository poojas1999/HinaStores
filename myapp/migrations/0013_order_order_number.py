# Generated by Django 5.0.1 on 2024-03-22 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_remove_order_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.IntegerField(default=2, max_length=100),
            preserve_default=False,
        ),
    ]
