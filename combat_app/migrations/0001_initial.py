# Generated by Django 3.0.7 on 2020-07-03 20:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hero_app', '0014_auto_20200702_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Combat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('duration', models.DurationField(null=True)),
                ('placement_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(3)])),
                ('placement_type', models.CharField(choices=[('FR', 'Free'), ('EQ', 'Equal')], default='EQ', max_length=2)),
                ('battle_type', models.CharField(choices=[('DF', 'TeamVsTeam'), ('MG', 'MeatGrinder')], default='DF', max_length=2)),
                ('team_size', models.IntegerField(default=1, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('hero_placement_height', models.IntegerField()),
                ('field_height', models.IntegerField()),
                ('field_width', models.IntegerField()),
                ('started', models.BooleanField(default=False)),
                ('left_team', models.ManyToManyField(blank=True, related_name='lt', to='hero_app.Hero')),
                ('mg_team', models.ManyToManyField(blank=True, related_name='mgt', to='hero_app.Hero')),
                ('right_team', models.ManyToManyField(blank=True, related_name='rt', to='hero_app.Hero')),
            ],
        ),
    ]
