# Generated by Django 3.1b1 on 2020-07-06 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero_app', '0015_hero_in_battle'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='army',
            field=models.JSONField(null=True),
        ),
    ]