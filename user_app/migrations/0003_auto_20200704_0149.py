# Generated by Django 3.0.7 on 2020-07-03 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hero_app', '0015_hero_in_battle'),
        ('user_app', '0002_auto_20200704_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heroapp',
            name='selected_hero',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='hero_app.Hero'),
        ),
    ]