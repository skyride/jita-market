# Generated by Django 3.0.8 on 2020-07-25 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0002_auto_20200725_0136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type',
            name='highest_buy',
        ),
        migrations.RemoveField(
            model_name='type',
            name='highest_sell',
        ),
        migrations.RemoveField(
            model_name='type',
            name='lowest_buy',
        ),
        migrations.RemoveField(
            model_name='type',
            name='lowest_sell',
        ),
    ]
