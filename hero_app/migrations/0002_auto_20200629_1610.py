# Generated by Django 3.0.7 on 2020-06-29 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hero',
            name='initiative',
            field=models.FloatField(default=0),
        ),
    ]
