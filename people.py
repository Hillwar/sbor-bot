import enum
from tools import Tools


class Person:
    def __init__(self, id, name, surname, phone_number, squad_id, role_id):
        self.id = id
        self.name = name.lower()
        self.surname = surname.lower()
        self.phone_number = phone_number
        self.squad_id = squad_id
        self.role_id = role_id

    def get_full_name(self, name_first = False):
        def get_capitalized_name(name):
            result = ''
            for split_name in name.split():
                result += ' ' if result else ''
                result += split_name.capitalize()
            return result

        name = get_capitalized_name(self.name)
        surname = get_capitalized_name(self.surname)
        return name + ' ' + surname if name_first else surname + ' ' + name

    def get_phone_number(self):
        return Tools.get_russian_number(self.phone_number)

    class Sort:
        def id(people): return people.id
        def name(people): return people.name
        def surname(people): return people.surname

    class Filter:
        def id(id): return lambda person: person.id == id
        def name(name): return lambda person: name in person.name
        def surname(surname): return lambda person: surname in person.surname
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
    def __init__(self, name, supervisor_id):
        self.name = name
        self.supervisor_id = supervisor_id

class Duty:
    def __init__(self, commander_id, commander_squad_id):
        self.commander_id = commander_id
        self.commander_squad_id = commander_squad_id

    def get_commander_nickname(self):
        return 'ДКО' if self.commander_squad_id else 'ДКС'

class Admin:
    def __init__(self, id, telegram, role_id):
        self.id = id
        self.telegram = telegram
        self.role_id = role_id

class AdminRole:
    def __init__(self, id, name, public_messages, see_ids, edit_timetable, edit_commanders, manage_admins):
        self.id = id
        self.name = name
        self.public_messages = public_messages
        self.see_ids = see_ids
        self.edit_timetable = edit_timetable
        self.edit_commanders = edit_commanders
        self.manage_admins = manage_admins

class Info:
    def __init__(self, number, dks_number, adress, location_link, vk_link):
        self.number = number
        self.dks_number = dks_number
        self.adress = adress
        self.location_link = location_link
        self.vk_link = vk_link

    def get_dks_number(self):
        return Tools.get_russian_number(self.dks_number)