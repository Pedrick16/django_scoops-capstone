# Generated by Django 4.1.2 on 2022-12-16 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0023_by_batch_remove_product_product_batch_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='by_batch',
            name='product_quantity',
            field=models.BigIntegerField(null=True, verbose_name='Quantity'),
        ),
    ]
