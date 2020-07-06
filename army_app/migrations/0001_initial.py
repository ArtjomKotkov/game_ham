# Generated by Django 3.1b1 on 2020-07-06 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hero_app', '0015_hero_in_battle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Army',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('structure', models.JSONField()),
                ('hero', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='army', to='hero_app.hero')),
            ],
        ),
    ]