# Generated by Django 3.1b1 on 2020-07-13 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero_app', '0021_auto_20200713_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='free_point',
            field=models.BooleanField(default=False),
        ),
    ]
