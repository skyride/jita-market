# Generated by Django 3.0.8 on 2020-07-25 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='regionprice',
            name='volume',
            field=models.IntegerField(default=0),
        ),
    ]
