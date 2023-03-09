# Generated by Django 4.1.3 on 2023-03-09 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0003_alter_pos_pos_reselleramount_alter_pos_pos_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pos',
            name='pos_ResellerAmount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Reseller Amount'),
        ),
        migrations.AlterField(
            model_name='pos',
            name='pos_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Pos Amount'),
        ),
        migrations.AlterField(
            model_name='pos',
            name='pos_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Pos Price'),
        ),
        migrations.AlterField(
            model_name='pos',
            name='pos_reseller_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Reseller Price'),
        ),
    ]
