# Generated by Django 5.0.1 on 2024-03-19 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_stockz_pname'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock')], default=2, max_length=50),
            preserve_default=False,
        ),
    ]
