# Generated by Django 4.1.3 on 2023-01-04 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0034_alter_transaction_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pos_sales',
            name='pos_TotalAmount',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='Total Amount'),
        ),
        migrations.AlterField(
            model_name='pos_sales',
            name='pos_change',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='Change'),
        ),
    ]
