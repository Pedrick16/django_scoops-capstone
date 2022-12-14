# Generated by Django 4.1.3 on 2022-12-11 11:33

import admin_site.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity_log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=250, verbose_name=' Username')),
                ('activity', models.CharField(max_length=250, verbose_name='Activity')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date and Time')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OrderItem_transactionNo', models.CharField(max_length=200, null=True, verbose_name='Transaction Number')),
                ('OrderItem_user', models.CharField(default=None, max_length=200, verbose_name='List Username')),
                ('OrderItem_category', models.CharField(max_length=200, verbose_name='Category')),
                ('OrderItem_name', models.CharField(max_length=200, verbose_name='Product Name')),
                ('OrderItem_size', models.CharField(max_length=200, verbose_name='Size')),
                ('OrderItem_quantity', models.CharField(max_length=200, null=True, verbose_name='quantity')),
                ('OrderItem_amount', models.FloatField(null=True, verbose_name='Amount')),
            ],
        ),
        migrations.CreateModel(
            name='Pos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos_user', models.CharField(default=None, max_length=200, verbose_name='List user')),
                ('pos_pcode', models.CharField(max_length=200, verbose_name='Product Code')),
                ('pos_category', models.CharField(max_length=200, verbose_name='Category')),
                ('pos_name', models.CharField(max_length=200, verbose_name='Product Name')),
                ('pos_size', models.CharField(max_length=200, verbose_name='Size')),
                ('pos_price', models.FloatField(null=True, verbose_name='Price')),
                ('pos_quantity', models.CharField(max_length=200, null=True, verbose_name='quantity')),
                ('pos_amount', models.FloatField(null=True, verbose_name='Amount')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=200, unique=True, verbose_name='Product Code')),
                ('product_category', models.CharField(max_length=200, verbose_name='Category')),
                ('product_name', models.CharField(max_length=200, verbose_name='Product Name')),
                ('product_size', models.CharField(max_length=200, verbose_name='Size')),
                ('product_price', models.FloatField(null=True, verbose_name='Price')),
                ('product_stock', models.CharField(max_length=200, verbose_name='Available Stock')),
                ('product_status', models.CharField(choices=[('available', 'available'), ('n/a', 'n/a')], max_length=200, verbose_name='Status')),
                ('product_expiry', models.DateField(default=None, null=True, verbose_name='Expiry Date')),
            ],
        ),
        migrations.CreateModel(
            name='Reseller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reseller_fname', models.CharField(max_length=200, verbose_name='First Name')),
                ('reseller_mname', models.CharField(max_length=200, verbose_name='Middle Name')),
                ('reseller_lname', models.CharField(max_length=200, verbose_name='Last Name')),
                ('reseller_gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=50, verbose_name='Gender')),
                ('reseller_contact', models.CharField(max_length=12, verbose_name='Contact Number')),
                ('reseller_address', models.CharField(max_length=200, verbose_name='Address')),
                ('reseller_email', models.EmailField(max_length=200, unique=True, verbose_name='Email')),
                ('reseller_id', models.ImageField(upload_to=admin_site.models.image_path, verbose_name='valid id')),
                ('reseller_businessp', models.ImageField(upload_to=admin_site.models.image_path, verbose_name='business id')),
                ('reseller_status', models.CharField(choices=[('pending', 'pending'), ('active', 'active'), ('inactive', 'inactive')], max_length=200, null=True, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_no', models.CharField(max_length=200, verbose_name='Transaction Number')),
                ('transaction_user', models.CharField(max_length=250, null=True, verbose_name='List Username')),
                ('transaction_fname', models.CharField(max_length=250, null=True, verbose_name='First Name')),
                ('transaction_lname', models.CharField(max_length=250, null=True, verbose_name='Last Name')),
                ('transaction_address', models.TextField(verbose_name='Address')),
                ('transaction_contactno', models.BigIntegerField(null=True, verbose_name='Contact Number')),
                ('transaction_doption', models.CharField(choices=[('pickup', 'pickup'), ('delivery', 'delivery')], max_length=250, null=True, verbose_name='Delivery Option')),
                ('transaction_totalprice', models.FloatField(null=True, verbose_name='Total Price')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('transaction_orderstatus', models.CharField(choices=[('Pending', 'Pending'), ('Out for Shipping', 'Out for Shipping'), ('Completed', 'Completed')], default='Pending', max_length=250, null=True, verbose_name='Status')),
                ('transaction_delivered', models.DateTimeField(blank=True, null=True, verbose_name='Delivered Time')),
            ],
        ),
    ]
