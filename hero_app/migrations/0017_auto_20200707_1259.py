# Generated by Django 3.1b1 on 2020-07-07 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero_app', '0016_hero_army'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hero',
            name='army',
            field=models.JSONField(default={}),
        ),
    ]
