import inspect


class Obstacles:

    def __init__(self):
        self.obstacles = []

    def add_obstacle(self, *args):
        for coord in args:
            assert isinstance(coord, tuple), f'All coords must be a tuple - error: {coord}.'
        self.obstacles.append(tuple([arg for arg in args]))
        return self

    def is_obstacle(self, x, y):
        for obstacle in self.obstacles:
            if (x, y) in obstacle:
                return True
        return False

    def __dict__(self):
        return self.obstacles

class FieldABS:
    hero_placement_height = 8
    image = None
    name = None
    obstacles = Obstacles()


class DefaultFieldDFSize1(FieldABS):
    height = 16
    width = 18
    combat_type = 'DF'
    _team_size = 1


class DefaultFieldDFSize2(FieldABS):
    height = 16
    width = 18
    combat_type = 'DF'
    _team_size = 2


class DefaultFieldDFSize3(FieldABS):
    height = 24
    width = 22
    combat_type = 'DF'
    _team_size = 3


class MeatGrinderField3(FieldABS):
    height = 16
    width = 16
    combat_type = 'MG'
    team_size = 4


class MeatGrinderField4(FieldABS):
    height = 16
    width = 16
    combat_type = 'MG'
    team_size = 4


class MeatGrinderField5(FieldABS):
    height = 28
    width = 28
    combat_type = 'MG'
    team_size = 5


class MeatGrinderField6(FieldABS):
    height = 28
    width = 28
    combat_type = 'MG'
    team_size = 6


class MeatGrinderField7(FieldABS):
    height = 28
    width = 28
    combat_type = 'MG'
    team_size = 7


class MeatGrinderField8(FieldABS):
    height = 28
    width = 28
    combat_type = 'MG'
    team_size = 8


class Fields:
    """
    Basic Field class.
    """

    @classmethod
    def _available_fields(cls):
        return {
            key: {
                value.team_size: {
                    key: value for key, value in value.__dict__.items() if inspect.isclass(value)
                } for key, value in value.__dict__.items() if inspect.isclass(value)
            } for key, value in cls.__dict__.items() if inspect.isclass(value)}

    @classmethod
    def fields_serialize(cls):
        return {'fields':{
                key: {
                    value.team_size: {
                        key: {
                            'name': value.name,
                            'image': value.image,

                        } for key, value in value.__dict__.items() if inspect.isclass(value)
                    } for key, value in value.__dict__.items() if inspect.isclass(value)
                } for key, value in cls.__dict__.items() if inspect.isclass(value)}}

    @classmethod
    def _available_battle_types(cls) -> list:
        return [key for key in cls._available_fields().keys()]

    @classmethod
    def _available_team_size(cls, battle_type: str) -> list:
        battle_type = battle_type.upper()
        return [key for key in cls._available_fields()[battle_type].keys()]

    @classmethod
    def _available_field(cls, battle_type: str, team_size: int) -> list:
        battle_type = battle_type.upper()
        return [key for key in cls._available_fields()[battle_type][team_size].keys()]

    @classmethod
    def get_field(cls, battle_type: str, team_size: int, name: str):
        battle_type = battle_type.upper()
        name = name.capitalize()
        assert battle_type in cls._available_fields(), f'Invalid battle type - {battle_type}. Available: {", ".join(cls._available_battle_types())}.'
        assert team_size in cls._available_fields()[battle_type], \
            f'Invalid team size - {team_size} for battle type {battle_type}. Available: {", ".join(cls._available_team_size(battle_type))}.'
        assert name in cls._available_fields()[battle_type][team_size], \
            f'Invalid field - {name} for battle type {battle_type} with size {team_size}. Available: {", ".join(cls._available_field(battle_type, team_size))}.'
        return cls._available_fields()[battle_type][team_size][name]

    @classmethod
    def get_fields(cls, battle_type: str, team_size: int):
        battle_type = battle_type.upper()
        assert battle_type in cls._available_fields(), f'Invalid battle type - {battle_type}. Available: {", ".join(cls._available_battle_types())}.'
        assert team_size in cls._available_fields()[battle_type], \
            f'Invalid team size - {team_size} for battle type {battle_type}. Available: {", ".join(cls._available_team_size(battle_type))}.'
        return cls._available_field(battle_type, team_size)


    @classmethod
    def check_field_is_aviable(cls, battle_type: str, team_size: int, name: str):
        battle_type = battle_type.upper()
        name = name.capitalize()
        if battle_type not in cls._available_fields():
            return False, 'Invalid battle class.'
        if team_size not in cls._available_fields()[battle_type]:
            return False, 'Invalid team size.'
        if name not in cls._available_fields()[battle_type][team_size]:
            return False, 'Invalid field name.'
        return True, 'Success.'

    @classmethod
    def is_obstacle(cls, x:int, y:int):
        return cls.obstacles.is_obstacle(x, y)

    class DF:
        """
        Default battle type Field class.
        """

        class Single:
            """
            Field class with size 1x1.
            """
            team_size = 1

            class Simple(DefaultFieldDFSize1):
                name = 'Simple'

            class Hard(DefaultFieldDFSize1):
                name = 'Hard'

        class Duo:
            """
            Field class with size 2x2.
            """
            team_size = 2

            class Simple(DefaultFieldDFSize2):
                name = 'Simple'

        class Trio:
            """
            Field class with size 3x3.
            """
            team_size = 3

            class Simple(DefaultFieldDFSize3):
                name = 'Simple'

    class MG:

        class Trio:
            team_size = 3

            class Simple(MeatGrinderField4):
                name = 'Simple'

        class Quartet:
            team_size = 4

            class Simple(MeatGrinderField4):
                name = 'Simple'

        class Quintet:
            team_size = 5

            class Simple(MeatGrinderField8):
                name = 'Simple'

        class Sextet:
            team_size = 6

            class Simple(MeatGrinderField8):
                name = 'Simple'

        class Septet:
            team_size = 7

            class Simple(MeatGrinderField8):
                name = 'Simple'

        class Octet:
            team_size = 8

            class Simple(MeatGrinderField8):
                name = 'Simple'