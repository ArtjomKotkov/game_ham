class CombatQueue:

    def __init__(self, combat):

        self.combat = combat
        assert self.combat.combat.is_started == True, 'Combat must be started.'
        self.current_index = 0
        self.total_units = 0
        self.queue = self._create_initiative_list()

    def _create_initiative_list(self):
        """Create queue, containing all stacks and heroes."""
        temp_queue = []
        for id, hero in self.combat.heroes.items():
            self._add_hero_to_initiate_queue(temp_queue, hero, id)
            for stack in hero.get_army().get_all_stacks():
                self._add_stack_to_initiate_queue(temp_queue, stack, id)
        temp_queue.sort(key=lambda x: x['initiative'], reverse=True)
        return temp_queue

    def sort_queue(self):
        self.queue.sort(key=lambda x: x['initiative'], reverse=True)
        return self.queue

    def _add_hero_to_initiate_queue(self, queue, hero, id):
        queue.append({
            'id': id,
            'type': 'hero',
            'object': hero,
            'initiative': hero.initiative
        })

    def _add_stack_to_initiate_queue(self, queue, stack, id):
        queue.append({
            'id': id,
            'type': 'stack',
            'object': stack,
            'initiative': stack.unit.initiative
        })

    def add_stack(self, stack):
        for index, item in enumerate(self.queue):
            if item['initiative'] < stack.unit.initiative:
                self.queue.insert(index, {
                    'object': stack,
                    'initiative': stack.unit.initiative
                })
        return self.queue

    def delete_stack(self, stack):
        for id, item in enumerate(self.queue):
            if item['object'] is stack:
                self.queue.pop(id)
        return self.queue

    def next_unit(self):
        """Give turn to the next unit in the queue."""
        if self.current_index + 1 == len(self.queue):
            self.current_index = 0
        else:
            self.current_index += 1
        return self.queue[self.current_index]

    def get_current_unit(self):
        return self.queue[self.current_index]['object']

    def is_hero_turn(self, hero_id):
        hero = self.combat.get_hero(hero_id)
        return True if self.get_current_unit() is hero else False

    def is_stack_turn(self, hero_id, stack_id):
        """Check that now is the hero_id+stack_id unit turn."""
        stack = self.combat.get_stack(hero_id, stack_id)
        return True if self.get_current_unit() is stack else False

    def serialize_short(self):
        return [{
            'id': item['id'],
            'type': item['type']
        } for item in self.queue]
