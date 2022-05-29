from openpyxl import Workbook, load_workbook
from people import Person, PersonRole, Service, Squad
from parser import parse


class Sbor:
    def __init__(self):
        workbook = load_workbook('resource/sbor_data.xlsx', data_only=True)
        self.__people, self.__squads, self.__duties, self.__services, self.__roles = parse(workbook)

    def get_people_count(self):
        return len(self.__people)

    def get_squads_count(self):
        return len(self.__squads)

    def get_services_count(self):
        return len(self.__services)

    def get_duties_count(self):
        return len(self.__duties)

    def get_person(self, id):
        return self.__people[id - 1]

    def get_squad(self, id):
        return self.__squads[id - 1]

    def get_service(self, id):
        return self.__services[id - 1]

    def get_role(self, id):
        return self.__roles[id - 1]


    def get_squad_info_people(self, squad):
        vozhatiy = self.get_person(squad.vozhatiy_id)
        komsorg = self.get_person(squad.komsorg_id)
        commander = self.get_person(self.get_duty_by_squad(squad.id).commander_id)
        return vozhatiy, komsorg, commander

    def get_squad_info_full(self, squad):
        vozhatiy, komsorg, commander = self.get_squad_info_people(squad)
        separator_middle = '\n'
        separator_end = '\n\n'
        return  '*Отряд \'' + squad.name + '\'*' + separator_end + \
                '*Вожатый*' + separator_middle + self.get_person_info(vozhatiy, True) + separator_end + \
                '*Комсорг*' + separator_middle + self.get_person_info(komsorg, True) + separator_end + \
                '*ДКО*' + separator_middle + self.get_person_info(commander, True)

    def get_squad_info_compact(self, squad):
        vozhatiy, komsorg, commander = self.get_squad_info_people(squad)
        separator_middle = ' - '
        separator_end = '\n'
        return  '*Отряд \'' + squad.name + '\'*' + separator_end + \
                'Вожатый' + separator_middle + self.get_person_info(vozhatiy, False) + separator_end + \
                'Комсорг' + separator_middle + self.get_person_info(komsorg, False) + separator_end + \
                'ДКО' + separator_middle + self.get_person_info(commander, False)

    def get_squad_info_with_people(self, squad):
        people = self.get_people_by_squad(squad.id)
        return  self.get_squad_info_full(squad) + '\n\n'\
                '*Состав*\n' + self.get_people_info(people)

    def get_person_info(self, person, full = True):
        phone_number = person.get_phone_number() if full else None
        person_info = person.get_full_name()
        if phone_number:
            person_info += ' ' + phone_number
        return person_info

    def get_service_info(self, service):
        supervisor = self.get_person(service.supervisor_id)
        return '*' + service.name + '*\n'+ self.get_person_info(supervisor)

    def get_duty_info(self, duty):
        squad_id = duty.commander_squad_id
        nickname = '*Дежурный Командир Сбора*' if squad_id == None else 'ДКО _\'' + self.get_squad(squad_id).name + '\'_'
        commander = self.get_person(duty.commander_id)
        return nickname + '\n' + self.get_person_info(commander)

    def get_duty_by_squad(self, squad_id):
        squad_duties = list(filter(lambda duty: duty.commander_squad_id == squad_id, self.__duties))
        return squad_duties[0]

    def get_people_by_squad(self, squad_id):
        squad_people = list(filter(lambda person: person.squad_id == squad_id, self.__people))
        squad_people.sort(key = lambda person: person.surname)
        return squad_people

    def get_squads_info(self):
        squad_info = ''
        for squad in self.__squads:
            squad_info += '\n\n' if squad_info else ''
            squad_info += self.get_squad_info_compact(squad)
        return squad_info

    def get_services_info(self):
        service_info = ''
        for service in self.__services:
            service_info += '\n\n' if service_info else ''
            service_info += self.get_service_info(service)
        return service_info

    def get_duties_info(self):
        duties_info = ''
        for duty in self.__duties:
            duties_info += '\n\n' if duties_info else ''
            duties_info += self.get_duty_info(duty)
        return duties_info

    def get_people_info(self, people):
        people_info = ''
        index = 1
        for person in people:
            people_info += '\n' if people_info else ''
            people_info += str(index) + ') ' + self.get_person_info(person, False)
            index += 1
        return people_info