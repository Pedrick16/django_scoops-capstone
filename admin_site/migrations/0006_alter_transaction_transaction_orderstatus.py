# Generated by Django 4.1.3 on 2022-12-09 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0005_alter_transaction_transaction_contactno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_orderstatus',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out for Shipping', 'Out for Shipping'), ('Completed', 'Completed')], default='Pending', max_length=250, null=True, verbose_name='Status'),
        ),
    ]
