from .combat import Combats
from ..models import Combat


class CombatManager:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
            setattr(cls.instance, 'current_combats', {})
        return cls.instance

    def add_combat(self, combat: Combats):
        if f'combat_{combat.combat.id}' not in self.current_combats:
            self.current_combats.update({
                f'combat_{combat.combat.id}': combat
            })

    def del_combat(self, pk):
        assert f'combat_{pk}' in self.current_combats, 'Combat with that id not exist.'
        del self.current_combats[f'combat_{pk}']

    def get_combat(self, pk):
        assert f'combat_{pk}' in self.current_combats, 'Combat with that id not exist.'
        return self.current_combats[f'combat_{pk}']

    def __dict__(self):
        return self.current_combats if hasattr(self, 'current_combats') else None

    def load_all_started(self):
        """
        Using when server was crashed.
        :param pk:
        :return:
        """
        combats = Combat.objects.exclude(status_in=[None, 'ended'])
        for combat in combats:
            self.add_combat(Combats(combat))
