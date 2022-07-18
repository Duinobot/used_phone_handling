# Generated by Django 4.0 on 2022-07-18 07:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'verbose_name': '1. Brand',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'verbose_name': '3. Phone Color',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(max_length=1)),
            ],
            options={
                'verbose_name': '8. Phone Grade',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': '9. Phone Location',
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('model', models.CharField(max_length=20, unique=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='phones.brand')),
            ],
            options={
                'verbose_name': '2. Phone Model',
            },
        ),
        migrations.CreateModel(
            name='UnlockedPartsCost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('lcd', models.DecimalField(decimal_places=2, max_digits=6)),
                ('digitizer', models.DecimalField(decimal_places=2, max_digits=6)),
                ('rear_camera', models.DecimalField(decimal_places=2, max_digits=6)),
                ('front_camera', models.DecimalField(decimal_places=2, max_digits=6)),
                ('baseband', models.DecimalField(decimal_places=2, max_digits=6)),
                ('face_id', models.DecimalField(decimal_places=2, max_digits=6)),
                ('wifi_bluetooth', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sound', models.DecimalField(decimal_places=2, max_digits=6)),
                ('charging_port', models.DecimalField(decimal_places=2, max_digits=6)),
                ('housing', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='parts_cost', to='phones.model')),
            ],
            options={
                'verbose_name': '7. [Unlocked] Parts Cost',
            },
        ),
        migrations.CreateModel(
            name='PhoneSpec',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('fullname', models.CharField(blank=True, max_length=30, null=True)),
                ('storage', models.CharField(choices=[('16GB', '16GB'), ('32GB', '32GB'), ('64GB', '64GB'), ('128GB', '128GB'), ('256GB', '256GB'), ('512GB', '512GB'), ('1TB', '1TB')], default='64GB', max_length=5)),
                ('listing_id', models.IntegerField(blank=True, null=True)),
                ('sku', models.IntegerField(blank=True, null=True)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='phonespec', to='phones.color')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='phonespec', to='phones.model')),
            ],
            options={
                'verbose_name': '0. Phone Specification',
            },
        ),
        migrations.CreateModel(
            name='LockedPartsWorth',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('screen', models.DecimalField(decimal_places=2, max_digits=6)),
                ('housing', models.DecimalField(decimal_places=2, max_digits=6)),
                ('back_camera', models.DecimalField(decimal_places=2, max_digits=6)),
                ('charging_port', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='parts_worth', to='phones.model')),
            ],
            options={
                'verbose_name': '6. [Locked] Parts Value',
            },
        ),
        migrations.AddConstraint(
            model_name='phonespec',
            constraint=models.UniqueConstraint(fields=('model', 'storage', 'color'), name='unique_phonespec_detail'),
        ),
        migrations.AddConstraint(
            model_name='model',
            constraint=models.UniqueConstraint(fields=('model', 'brand'), name='unique_model_brand'),
        ),
    ]
