from parse.excel_parser import Parser
from people import DutySquad, Service, Person, PersonRole, Squad, Commander, Info

def get_sbor(workbook):
    first_row = 3

    def parse_people(sheet):
        people = []
        id_col = 1
        surname_col = 2
        name_col = 3
        phone_col = 4
        squad_id_col = 5
        role_id_col = 6
        row = first_row

        while Parser.get_cell_value(sheet, id_col, row):
            id = Parser.get_cell_value(sheet, id_col, row)
            surname = Parser.get_cell_value(sheet, surname_col, row)
            name = Parser.get_cell_value(sheet, name_col, row)
            phone = Parser.get_cell_value(sheet, phone_col, row)
            squad_id = Parser.get_cell_value(sheet, squad_id_col, row)
            role_id = Parser.get_cell_value(sheet, role_id_col, row)

            person = Person(id, name, surname, phone, squad_id, role_id)
            people.append(person)
            row += 1

        return people

    def parse_supervisors(sheet):
        supervisors = []
        name_col = 1
        supervisor_id_col = 2
        row = first_row

        while Parser.get_cell_value(sheet, name_col, row):
            name = Parser.get_cell_value(sheet, name_col, row)
            supervisor_id = Parser.get_cell_value(sheet, supervisor_id_col, row)

            supervisor = Service(name, supervisor_id)
            supervisors.append(supervisor)
            row += 1

        return supervisors

    def parse_squads(sheet):
        squads = []
        id_col = 1
        name_col = 2
        vozhatiy_id_col = 3
        komsorg_id_col = 4
        row = first_row

        while Parser.get_cell_value(sheet, id_col, row):
            id = Parser.get_cell_value(sheet, id_col, row)
            name = Parser.get_cell_value(sheet, name_col, row)
            vozhatiy_id = Parser.get_cell_value(sheet, vozhatiy_id_col, row)
            komsorg_id = Parser.get_cell_value(sheet, komsorg_id_col, row)

            squad = Squad(id, name, vozhatiy_id, komsorg_id)
            squads.append(squad)
            row += 1

        return squads

    def parse_services(sheet):
        services = []
        name_col = 1
        supervisor_id_col = 2
        row = first_row

        while Parser.get_cell_value(sheet, name_col, row):
            name = Parser.get_cell_value(sheet, name_col, row)
            supervisor_id = Parser.get_cell_value(sheet, supervisor_id_col, row)

            service = Service(name, supervisor_id)
            services.append(service)
            row += 1

        return services

    def parse_roles(sheet):
        roles = []
        id_col = 1
        name_col = 2
        plural_col = 3
        row = first_row

        while Parser.get_cell_value(sheet, id_col, row):
            id = Parser.get_cell_value(sheet, id_col, row)
            name = Parser.get_cell_value(sheet, name_col, row)
            plural = Parser.get_cell_value(sheet, plural_col, row)

            role = PersonRole(id, name, plural)
            roles.append(role)
            row += 1

        return roles

    def parse_commanders(sheet):
        commanders = []
        commander_id_col = 2
        commander_squad_id_col = 3
        row = first_row

        while Parser.get_cell_value(sheet, commander_id_col, row):
            commander_id = Parser.get_cell_value(sheet, commander_id_col, row)
            commander_squad_id = Parser.get_cell_value(sheet, commander_squad_id_col, row)

            commander = Commander(commander_id, commander_squad_id)
            commanders.append(commander)
            row += 1

        return commanders

    def parse_info(sheet):
        number_row = 3
        dks_number_row = 4
        adress_row = 5
        location_link_row = 6
        vk_link_row = 7
        col = 2

        number = Parser.get_cell_value(sheet, col, number_row)
        dks_number = Parser.get_cell_value(sheet, col, dks_number_row)
        adress = Parser.get_cell_value(sheet, col, adress_row)
        location_link = Parser.get_cell_value(sheet, col, location_link_row)
        vk_link = Parser.get_cell_value(sheet, col, vk_link_row)

        return Info(number, dks_number, adress, location_link, vk_link)

    people = parse_people(workbook.get_sheet_by_name('People'))
    squads = parse_squads(workbook.get_sheet_by_name('Squads'))
    commanders = parse_commanders(workbook.get_sheet_by_name('Commanders'))
    services = parse_services(workbook.get_sheet_by_name('Services'))
    roles = parse_roles(workbook.get_sheet_by_name('Roles'))
    supervisors = parse_supervisors(workbook.get_sheet_by_name('Supervisors'))
    info = parse_info(workbook.get_sheet_by_name('Info'))

    return people, squads, commanders, services, roles, supervisors, info


def save_sbor(workbook, path, commanders):
    first_row = 3

    def set_commanders(sheet, commanders):
        commander_id_col = 2
        commander_squad_id_col = 3
        row = first_row

        while Parser.get_cell_value(sheet, commander_id_col, row):
            commander_squad_id = Parser.get_cell_value(sheet, commander_squad_id_col, row)
            commander_saved = False
            for commander in commanders:
                if commander_squad_id == commander.commander_squad_id:
                    Parser.set_cell_value(sheet, commander_id_col, row, commander.commander_id)
                    commander_saved = True
                    break

            if not commander_saved:
                raise Exception("Can't save all commanders")

            row += 1

    set_commanders(workbook.get_sheet_by_name('Commanders'), commanders)
    workbook.save(path)
