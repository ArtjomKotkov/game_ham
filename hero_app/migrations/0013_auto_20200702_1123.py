# Generated by Django 3.0.7 on 2020-07-02 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero_app', '0012_defaulthero_human_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaulthero',
            name='human_name',
            field=models.CharField(max_length=36),
        ),
    ]