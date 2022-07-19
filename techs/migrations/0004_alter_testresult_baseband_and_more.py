# Generated by Django 4.0 on 2022-07-19 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techs', '0003_alter_phone_phonespec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='baseband',
            field=models.BooleanField(default=0, verbose_name='Baseband Issue'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='charging_port',
            field=models.BooleanField(default=0, verbose_name='Charging Port Faulty'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='digitizer',
            field=models.BooleanField(default=0, verbose_name='Digitizer Faulty'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='face_id',
            field=models.BooleanField(default=0, verbose_name='Face ID Issue'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='front_camera',
            field=models.BooleanField(default=0, verbose_name='Front Camera Faulty'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='housing',
            field=models.BooleanField(default=0, verbose_name='Back Cover Broken'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='lcd',
            field=models.BooleanField(default=0, verbose_name='LCD Faulty'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='locked_back_camera',
            field=models.BooleanField(default=0, verbose_name='Back Camera OK'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='locked_charging_port',
            field=models.BooleanField(default=0, verbose_name='Charging Port OK'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='locked_housing',
            field=models.BooleanField(default=0, verbose_name='Housing OK'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='locked_screen',
            field=models.BooleanField(default=0, verbose_name='Screen OK'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='rear_camera',
            field=models.BooleanField(default=0, verbose_name='Rear Camera Faulty'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='sound',
            field=models.BooleanField(default=0, verbose_name='Audio Issue'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='total_repair_cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=15, max_digits=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='testresult',
            name='wifi_bluetooth',
            field=models.BooleanField(default=0, verbose_name='Wifi/Bluetooth Issue'),
        ),
    ]