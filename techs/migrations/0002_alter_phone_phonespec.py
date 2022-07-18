# Generated by Django 4.0 on 2022-07-18 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phones', '0001_initial'),
        ('techs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='phonespec',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='phones', to='phones.phonespec'),
        ),
    ]