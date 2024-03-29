# Generated by Django 4.2.9 on 2024-01-20 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('status', models.CharField(default='Available', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
                ('volume', models.FloatField()),
                ('status', models.CharField(default='Pending', max_length=10)),
                ('owner_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cost', models.FloatField()),
                ('max_weight', models.FloatField()),
                ('max_volume', models.FloatField()),
                ('status', models.CharField(default='Available', max_length=10)),
                ('current_weight', models.FloatField(default=0.0)),
                ('current_volume', models.FloatField(default=0.0)),
                ('maintenance_check', models.DateTimeField(blank=True, null=True)),
                ('lines', models.ManyToManyField(to='mailservice.line')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailservice.line')),
                ('parcel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailservice.parcel')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailservice.train')),
            ],
        ),
    ]
