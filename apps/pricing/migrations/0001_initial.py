# Generated by Django 3.0.8 on 2020-07-25 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sde', '0003_auto_20200725_0141'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegionPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_buy', models.FloatField(default=0)),
                ('max_sell', models.FloatField(default=0)),
                ('min_buy', models.FloatField(default=0)),
                ('min_sell', models.FloatField(default=0)),
                ('average_buy', models.FloatField(default=0)),
                ('average_sell', models.FloatField(default=0)),
                ('percentile_buy', models.FloatField(default=0)),
                ('percentile_sell', models.FloatField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='sde.Region')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='sde.Type')),
            ],
        ),
    ]