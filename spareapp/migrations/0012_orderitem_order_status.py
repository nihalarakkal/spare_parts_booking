# Generated by Django 5.1.5 on 2025-02-11 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0011_rename_oderitem_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='order_status',
            field=models.BooleanField(default=True),
        ),
    ]
