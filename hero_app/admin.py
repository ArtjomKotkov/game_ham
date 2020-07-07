from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Hero, Spell, SpellTome, DefaultHero


class Spells(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'damage_per_tail',
                    'scheme', 'height', 'width', 'tome', 'html_scheme')
    ordering = ('tome',)

    def html_scheme(self, obj):

        td_white = '<td width="22" height="22" style="padding:0;"></td>'
        td_colored = '<td style="background-color:gray; border: 1px solid white; padding:0;" width="22" height="22"></td>'
        scheme = ''
        if obj.scheme == 'CROSS':
            for line in range(1, obj.height + 1):
                row = ''
                for column in range(1, obj.width + 1):
                    if column == obj.width // 2 + 1 or line == obj.height // 2 + 1:
                        row += td_colored
                    else:
                        row += td_white
                scheme += '<tr>' + row + '</tr>'
            scheme = f'<table style="width:{22 * column}px; height:{22 * line}px;">' + scheme + '</table>'

        elif obj.scheme == 'RECTAN':
            for line in range(1, obj.height + 1):
                row = ''
                for column in range(1, obj.width + 1):
                    row += td_colored
                scheme += '<tr>' + row + '</tr>'
            scheme = f'<table style="width:{22 * column}px; height:{22 * line}px;">' + scheme + '</table>'

        elif obj.scheme == 'CF':
            radius = obj.height // 2
            for line in range(1, obj.height + 1):
                row = ''
                for column in range(1, obj.width + 1):
                    row += td_colored if in_circle(line, column, radius) else td_white
                scheme += '<tr>' + row + '</tr>'
            scheme = f'<table style="width:{22 * column}px; height:{22 * line}px;">' + scheme + '</table>'

        return format_html(scheme)

    html_scheme.short_description = 'Модель схемы'


class SpellTomes(admin.ModelAdmin):
    list_display = ('name', 'ListOfSpells')

    def ListOfSpells(self, obj):
        spells = obj.spells.all()
        li_list = ''
        for spell in spells:
            li_list += f'<li><a href="{reverse("admin:hero_app_spell_change", args=(spell.id,))}">{spell.name}</a></li>'
        li_list = '<ul>' + li_list + '</ul>'
        return format_html(li_list)


class Heroes(admin.ModelAdmin):
    list_display = (
    'id', 'user', 'name', 'attack', 'defense', 'mana', 'spell_power', 'initiative', 'ListOfSpells')
    ordering = ('user',)

    def ListOfSpells(self, obj):
        spells = obj.spells.all()
        li_list = ''
        for spell in spells:
            li_list += f'<li><a href="{reverse("admin:hero_app_spell_change", args=(spell.id,))}">{spell.name}</a></li>'
        li_list = '<ul>' + li_list + '</ul>'
        return format_html(li_list)


admin.site.register(Hero, Heroes)
admin.site.register(SpellTome, SpellTomes)
admin.site.register(Spell, Spells)
admin.site.register(DefaultHero)


def in_circle(x, y, radius):
    return True if ((x - radius - 1) ** 2 + (y - radius - 1) ** 2) ** (1 / 2) <= radius else False
