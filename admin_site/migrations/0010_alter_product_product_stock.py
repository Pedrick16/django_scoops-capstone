# Generated by Django 4.1.3 on 2022-12-14 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0009_alter_product_product_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_stock',
            field=models.BigIntegerField(null=True, verbose_name='Available Stock'),
        ),
    ]