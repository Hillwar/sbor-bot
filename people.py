import enum
from tools import Tools


class Person:
    def __init__(self, id, name, surname, phone_number, squad_id, role_id = None):
        self.id = int(id)
        self.name = name.lower() if name else ''
        self.surname = surname.lower() if surname else ''
        self.phone_number = int(phone_number)
        self.squad_id = int(squad_id) if squad_id else None
        self.role_id = int(role_id) if role_id else None

    def get_full_name(self, name_first=False):
        def get_capitalized_name(name):
            result = ''
            for split_name in name.split():
                result += ' ' if result else ''
                result += split_name.capitalize()
            return result

        name = get_capitalized_name(self.name)
        surname = get_capitalized_name(self.surname)
        if not name:
            return surname

        if not surname:
            return name

        return name + ' ' + surname if name_first else surname + ' ' + name

    def get_phone_number(self):
        return Tools.get_russian_number(self.phone_number)

    class Sort:
        def id(people): return people.id

        def name(people): return people.name

        def surname(people): return people.surname

    @staticmethod
    def sort(people, key):
        return people.sort(key=key)

    class Filter:
        def id(id): return lambda person: person.id == id

        def name(name): return lambda person: name in person.name

        def surname(surname): return lambda person: surname in person.surname

        def squad_id(squad_id): return lambda person: person.squad_id == squad_id

        def role_id(role_id): return lambda person: person.role_id == role_id

    @staticmethod
    def filter(people, key):
        return list(filter(key, people))

    class Info(enum.Enum):
        Compact = 1
        Full = 2
        Debug = 3


class Squad:
    def __init__(self, id, name, supervisor_id, vozhatiy_id = None):
        self.id = id
        self.name = name
        self.supervisor_id = supervisor_id
        self.vozhatiy_id = vozhatiy_id


class PersonRole:
    def __init__(self, id, name, plural):
        self.id = id
        self.name = name
        self.plural = plural


class Service:
    def __init__(self, name, supervisor_id):
        self.name = name
        self.supervisor_id = supervisor_id


class Commander:
    def __init__(self, commander_id, commander_squad_id = None):
        self.commander_id = commander_id
        self.commander_squad_id = commander_squad_id


class DutySquad:
    def __init__(self, squad_id):
        self.squad_id = squad_id

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
    def __init__(self, number, main_commander_number, adress = None, location_link = None, vk_link = None, tg_chat_link = None):
        self.number = number
        self.main_commander_number = main_commander_number
        self.adress = adress
        self.location_link = location_link
        self.vk_link = vk_link
        self.tg_chat_link = tg_chat_link

    def get_main_commander_number(self):
        return Tools.get_russian_number(self.main_commander_number)
