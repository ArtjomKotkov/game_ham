# Generated by Django 3.1b1 on 2020-07-16 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero_app', '0023_auto_20200716_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hero',
            name='in_battle',
            field=models.IntegerField(default=-1, null=True),
        ),
    ]
