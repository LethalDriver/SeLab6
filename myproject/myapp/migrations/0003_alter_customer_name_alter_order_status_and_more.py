# Generated by Django 5.1.3 on 2024-11-13 09:03

import myapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_customer_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'New'), ('PROCESSING', 'In Process'), ('SENT', 'Sent'), ('COMPLETED', 'Completed')], default='NEW', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[myapp.models.validate_price]),
        ),
    ]
