# Generated by Django 4.1.2 on 2023-04-21 10:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0017_alter_cart_payment_cart_change'),
    ]

    operations = [
        migrations.CreateModel(
            name='Return_product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=200, unique=True, verbose_name='Product Code')),
                ('product_name', models.CharField(max_length=200, null=True, verbose_name='Product Name')),
                ('product_unit', models.CharField(max_length=200, verbose_name='Unit')),
                ('product_qty', models.BigIntegerField(null=True, verbose_name='Available Stock')),
                ('return_date', models.DateField(default=django.utils.timezone.now, verbose_name='Return Date')),
                ('product_status', models.CharField(choices=[('', ''), ('returned', 'returned'), ('not return', 'not return')], max_length=200, verbose_name='Status')),
            ],
        ),
    ]
