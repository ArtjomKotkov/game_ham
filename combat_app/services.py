from .models import Combat, TYPES, TYPES_COMBAT

class Combats:
    pass

TYPES = [elem[0] for elem in TYPES]
TYPES_COMBAT = [elem[0] for elem in TYPES_COMBAT]

class CombatManager:

    @classmethod
    def create(cls, name, placement_type='equal', combat_type='1'):
        instance = cls.__new__(cls)
        if placement_type not in TYPES:
            placement_type = 'equal'
        if combat_type not in TYPES_COMBAT:
            combat_type = '1'
        combat = Combat.objects.create(name=name, placement_type=placement_type, battle_type=combat_type)
        setattr(instance, 'combat', combat)
        return instance

    @classmethod
    def load(cls, pk):
        instance = cls.__new__(cls)
        combat = Combat.objects.get(pk=pk)
        setattr(instance, 'combat', combat)
        return instance