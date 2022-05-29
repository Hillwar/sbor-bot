
import string
from people import Service, Person, PersonRole, Squad, Duty


def parse(workbook):
    first_row = 3

    def get_cell_value(sheet, col, row):
        value = sheet.cell(row = row, column = col).value
        if not value:
            return value

        return value

    def parse_people(sheet):
        people = []
        id_col = 1
        surname_col = 2
        name_col = 3
        phone_col = 4
        squad_id_col = 5
        role_id_col = 6
        row = first_row

        while get_cell_value(sheet, id_col, row):
            id = get_cell_value(sheet, id_col, row)
            surname = get_cell_value(sheet, surname_col, row)
            name = get_cell_value(sheet, name_col, row)
            phone = get_cell_value(sheet, phone_col, row)
            squad_id = get_cell_value(sheet, squad_id_col, row)
            role_id = get_cell_value(sheet, role_id_col, row)

            person = Person(id, name, surname, phone, squad_id, role_id)
            people.append(person)
            row += 1

        return people

    def parse_squads(sheet):
        squads = []
        id_col = 1
        name_col = 2
        vozhatiy_id_col = 3
        komsorg_id_col = 4
        row = first_row

        while get_cell_value(sheet, id_col, row):
            id = get_cell_value(sheet, id_col, row)
            name = get_cell_value(sheet, name_col, row)
            vozhatiy_id = get_cell_value(sheet, vozhatiy_id_col, row)
            komsorg_id = get_cell_value(sheet, komsorg_id_col, row)

            squad = Squad(id, name, vozhatiy_id, komsorg_id)
            squads.append(squad)
            row += 1

        return squads

    def parse_services(sheet):
        services = []
        id_col = 1
        name_col = 2
        supervisor_id_col = 3
        row = first_row

        while get_cell_value(sheet, id_col, row):
            id = get_cell_value(sheet, id_col, row)
            name = get_cell_value(sheet, name_col, row)
            supervisor_id = get_cell_value(sheet, supervisor_id_col, row)

            service = Service(id, name, supervisor_id)
            services.append(service)
            row += 1

        return services

    def parse_roles(sheet):
        roles = []
        id_col = 1
        name_col = 2
        row = first_row

        while get_cell_value(sheet, id_col, row):
            id = get_cell_value(sheet, id_col, row)
            name = get_cell_value(sheet, name_col, row)

            role = PersonRole(id, name)
            roles.append(role)
            row += 1

        return roles

    def parse_duties(sheet):
        duties = []
        commander_id_col = 2
        commander_squad_id_col = 3
        row = first_row

        while get_cell_value(sheet, commander_id_col, row):
            commander_id = get_cell_value(sheet, commander_id_col, row)
            commander_squad_id = get_cell_value(sheet, commander_squad_id_col, row)

            duty = Duty(commander_id, commander_squad_id)
            duties.append(duty)
            row += 1

        return duties

    people = parse_people(workbook.get_sheet_by_name('People'))
    squads = parse_squads(workbook.get_sheet_by_name('Squads'))
    duties = parse_duties(workbook.get_sheet_by_name('Duty'))
    services = parse_services(workbook.get_sheet_by_name('Services'))
    roles = parse_roles(workbook.get_sheet_by_name('Roles'))

    return people, squads, duties, services, roles
