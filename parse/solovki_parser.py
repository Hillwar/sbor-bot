from parse.excel_parser import Parser
from people import Service, Person, PersonRole, Squad, Commander, Info

def get_solovki(workbook):
    first_row = 3

    def parse_people(sheet):
        people = []
        id_col = 1
        surname_col = 2
        name_col = 3
        phone_col = 4
        squad_id_col = 5
        row = first_row

        while Parser.get_cell_value(sheet, id_col, row):
            id = Parser.get_cell_value(sheet, id_col, row)
            surname = Parser.get_cell_value(sheet, surname_col, row)
            name = Parser.get_cell_value(sheet, name_col, row)
            phone = Parser.get_cell_value(sheet, phone_col, row)
            squad_id = Parser.get_cell_value(sheet, squad_id_col, row)
            print(int(id))
            person = Person(id, name, surname, phone, squad_id)
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
        supervisor_id_col = 3
        row = first_row

        while Parser.get_cell_value(sheet, id_col, row):
            id = Parser.get_cell_value(sheet, id_col, row)
            name = Parser.get_cell_value(sheet, name_col, row)
            supervisor_id = Parser.get_cell_value(sheet, supervisor_id_col, row)

            squad = Squad(id, name, supervisor_id)
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

    def parse_commanders(sheet):
        commanders = []
        commander_id_col = 2
        row = first_row

        commander_id = Parser.get_cell_value(sheet, commander_id_col, row)
        commander = Commander(commander_id)
        commanders.append(commander)

        return commanders

    def parse_info(sheet):
        number_row = 3
        dkl_number_row = 4
        col = 2

        number = Parser.get_cell_value(sheet, col, number_row)
        dkl_number = Parser.get_cell_value(sheet, col, dkl_number_row)

        return Info(number, dkl_number)

    people = parse_people(workbook.get_sheet_by_name('People'))
    squads = parse_squads(workbook.get_sheet_by_name('Squads'))
    commanders = parse_commanders(workbook.get_sheet_by_name('Commanders'))
    services = parse_services(workbook.get_sheet_by_name('Services'))
    supervisors = parse_supervisors(workbook.get_sheet_by_name('Supervisors'))
    info = parse_info(workbook.get_sheet_by_name('Info'))

    return people, squads, commanders, services, supervisors, info


def save_solovki(workbook, path, commanders):
    first_row = 3

    def set_commander(sheet, commanders):
        commander_id_col = 2
        row = first_row
        Parser.set_cell_value(sheet, commander_id_col, row, commanders[0].commander_id)

    set_commander(workbook.get_sheet_by_name('Commanders'), commanders)
    workbook.save(path)
