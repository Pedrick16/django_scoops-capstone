# Generated by Django 4.1.3 on 2022-12-03 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0005_rename_products_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_expiry',
            field=models.CharField(max_length=200, null=True, verbose_name='Status'),
        ),
    ]
