# Generated by Django 4.1.3 on 2023-01-05 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0043_alter_pos_payment_pos_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='pos_payment',
            name='pos_no',
            field=models.CharField(max_length=200, null=True, verbose_name='Pos No'),
        ),
    ]
