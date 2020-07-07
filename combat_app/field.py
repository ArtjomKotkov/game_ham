from .models import Field

class Fields:
    hero_placement_height = 8

    def __init__(self, combat_type, team_size, obstacles=None):
        """
        :param combat_type:
        :param hero_placement_height:
        :param team_size:
        :param obstacles: List of obstacles, every obstacle is a tuple with x, y cords of obstacle.
        [((x,y)),((x,y), (x,y), (x,y))]
        """
        self.combat_type = combat_type
        self.team_size = team_size
        self.height = self.calculate_field_height()
        self.width = self.calculate_field_width()
        self.obstacles = [] if obstacles == None else obstacles

    def create(self, name):
        self.instance = Field.objects.create(name=name,
                                             height=self.height,
                                             width=self.width,
                                             # obstacles=self.obstacles
                                             )
        return self

    @classmethod
    def load(cls, field):
        instance = cls.__new__(cls)
        setattr(instance, 'instance', field)
        setattr(instance, 'height', field.height)
        setattr(instance, 'width', field.width)
        # setattr(instance, 'obstacles', field.obstacles)
        return instance

    def add_obstacle(self, obstacle: tuple):
        """
        :param obstacle:((x,y), (x,y))
        :return:
        """
        for coords in obstacle:
            assert len(coords) == 2, 'Coords must containt 2 values, x and y.'
            assert isinstance(coords[0], int), 'X value must be int.' + coords
            assert isinstance(coords[0], int), 'Y value must be int.' + coords
        self.obstacles.append(obstacle)

    def calculate_field_height(self):
        if self.combat_type == 'DF':
            height = self.hero_placement_height * self.team_size if self.team_size >= 2 else self.hero_placement_height * 2
        else:
            if self.team_size in [3, 4]:
                height = self.hero_placement_height + 10
            else:
                height = self.hero_placement_height * 2 + 12
        return height

    def calculate_field_width(self):
        if self.combat_type == 'DF':
            width = self.hero_placement_height * 2 + (self.team_size - 1) + 2

        else:
            if self.team_size in [3, 4]:
                width = self.hero_placement_height + 10
            else:
                width = self.hero_placement_height * 2 + 12
        return width

    def get_instance(self):
        assert hasattr(self, 'instance'), 'Fields object doesn\'t have instance.'
        return self.instance