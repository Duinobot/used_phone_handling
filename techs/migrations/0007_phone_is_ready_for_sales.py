# Generated by Django 4.0 on 2022-07-20 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techs', '0006_alter_testresult_total_repair_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='is_ready_for_sales',
            field=models.BooleanField(default=0, verbose_name='Ready For Sale Phone'),
        ),
    ]