# Generated by Django 5.0.1 on 2024-03-19 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_product_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='status',
        ),
        migrations.AddField(
            model_name='product',
            name='stock_available',
            field=models.IntegerField(default=0),
        ),
    ]
