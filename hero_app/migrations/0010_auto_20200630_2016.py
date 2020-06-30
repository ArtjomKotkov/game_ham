# Generated by Django 3.0.7 on 2020-06-30 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero_app', '0009_hero_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultHero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24, unique=True)),
                ('attack', models.IntegerField(default=1)),
                ('defense', models.IntegerField(default=0)),
                ('mana', models.IntegerField(default=0)),
                ('spell_power', models.IntegerField(default=0)),
                ('initiative', models.FloatField(default=10)),
            ],
        ),
        migrations.AddField(
            model_name='spell',
            name='default_hero',
            field=models.ManyToManyField(blank=True, related_name='spells', to='hero_app.DefaultHero'),
        ),
    ]