from django.shortcuts import render
from django.views.generic import View, ListView
from django.shortcuts import get_object_or_404, redirect, reverse
from django.http import HttpResponseForbidden

from .combat.combat import Combats
from .combat.field import Fields
from .models import Combat
from hero_app.views import CustomAPIView, NoModelAPIView
from .serializers import CombatFullSerializer, CombatShortSerializer, FieldsSerializer


class CombatListView(ListView):
    model = Combat
    context_object_name = 'combats'
    template_name = 'books/combat_list.html'


def cobmat(request, pk):
    combat = get_object_or_404(Combat, pk=pk)
    if not combat.started:
        return HttpResponseForbidden()
    context = {
        'combat_pk': pk
    }
    return render(request, 'combat_app/combat_page.html', context)


class Income(View):
    def get(self, request, pk):
        data = request.GET
        team = data.get('team')
        combat = Combats().load(get_object_or_404(Combat, pk=pk))
        if team == 'left':
            combat.add_hero_to_left_team(request.user.heroapp.selected_hero)
        elif team == 'right':
            combat.add_hero_to_right_team(request.user.heroapp.selected_hero)
        else:
            combat.add_hero_to_combat(request.user.heroapp.selected_hero)
        return redirect(reverse('combat:combat_list'))


class CombatApi(CustomAPIView):
    short_serializer = CombatShortSerializer
    full_serializer = CombatFullSerializer
    model = Combat


class FieldsApi(NoModelAPIView):
    serializer = FieldsSerializer
    data = Fields.fields_serialize()
    available_methods = ['GET']
