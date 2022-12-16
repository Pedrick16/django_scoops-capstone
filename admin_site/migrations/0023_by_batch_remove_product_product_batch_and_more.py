# Generated by Django 4.1.2 on 2022-12-16 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0022_rename_product_size_product_product_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='By_Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=200, null=True, verbose_name='Product Code')),
                ('product_batch', models.CharField(max_length=200, null=True, verbose_name='Batch Number')),
                ('product_expired', models.DateField(null=True, verbose_name='Expiration Date')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_batch',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_expired',
        ),
    ]
