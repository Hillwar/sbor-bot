import enum



class Person:
    def __init__(self, id, name, surname, phone_number, squad_id, role_id):
        self.id = id
        self.name = name
        self.surname = surname
        self.phone_number = phone_number
        self.squad_id = squad_id
        self.role_id = role_id

    def get_full_name(self, name_first = False):
        return self.name + ' ' + self.surname if name_first else self.surname + ' ' + self.name

    def get_phone_number(self):
        if not self.phone_number:
            return None

        return '+7' + str(self.phone_number)

    class Sort:
        def id(people): return people.id
        def name(people): return people.name
        def surname(people): return people.surname

    class Filter:
        def squad_id(squad_id): return lambda person: person.squad_id == squad_id
        def role_id(role_id): return lambda person: person.role_id == role_id

    class Info(enum.Enum):
        Compact = 1
        Full = 2
        Debug = 3

class Squad:
    def __init__(self, id, name, vozhatiy_id, komsorg_id):
        self.id = id
        self.name = name
        self.vozhatiy_id = vozhatiy_id
        self.komsorg_id = komsorg_id

class PersonRole:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Service:
    def __init__(self, id, name, supervisor_id):
        self.id = id
        self.name = name
        self.supervisor_id = supervisor_id

class Duty:
    def __init__(self, commander_id, commander_squad_id):
        self.commander_id = commander_id
        self.commander_squad_id = commander_squad_id

    def get_commander_nickname(self):
        return 'ДКС' if self.commander_squad_id is None else 'ДКО'