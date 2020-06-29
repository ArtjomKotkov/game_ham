# Generated by Django 3.0.7 on 2020-06-29 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hero_app', '0003_spell_spelltome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spell',
            name='hero',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spells', to='hero_app.Hero'),
        ),
        migrations.AlterField(
            model_name='spell',
            name='tome',
            field=models.ManyToManyField(related_name='spells', to='hero_app.SpellTome'),
        ),
    ]
