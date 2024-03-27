# Generated by Django 5.0.1 on 2024-03-20 11:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentz',
            name='pname',
        ),
        migrations.RemoveField(
            model_name='paymentz',
            name='quantity',
        ),
        migrations.AddField(
            model_name='paymentz',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.cartitem'),
        ),
        migrations.AddField(
            model_name='paymentz',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.product'),
        ),
    ]
