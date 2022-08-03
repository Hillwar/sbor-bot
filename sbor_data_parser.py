import imp
from people import Admin, AdminRole, DutySquad, Service, Person, PersonRole, Squad, Commander, Info
from google_parser import Parser
from config import SpreadsheetIds


def get_sbor(google_service, spreadsheet_id):
    first_row = 3

    def parse_people(sheet):
        people = []
        id_col = 1
        surname_col = 2
        name_col = 3
        phone_col = 4
        squad_id_col = 5
        role_id_col = 6

        for i in range(first_row, Parser.get_row_length(sheet) + 1):
            id = Parser.get_cell_value(sheet, id_col, i)
            surname = Parser.get_cell_value(sheet, surname_col, i)
            name = Parser.get_cell_value(sheet, name_col, i)
            phone = Parser.get_cell_value(sheet, phone_col, i)
            squad_id = Parser.get_cell_value(sheet, squad_id_col, i)
            role_id = Parser.get_cell_value(sheet, role_id_col, i)

            person = Person(id, name, surname, phone, squad_id, role_id)
            people.append(person)

        return people

    def parse_supervisors(sheet):
        supervisors = []
        name_col = 1
        supervisor_id_col = 2

        for i in range(first_row, Parser.get_row_length(sheet) + 1):
            name = Parser.get_cell_value(sheet, name_col, i)
            supervisor_id = Parser.get_cell_value(sheet, supervisor_id_col, i)

            supervisor = Service(name, supervisor_id)
            supervisors.append(supervisor)

        return supervisors

    def parse_squads(sheet):
        squads = []
        id_col = 1
        name_col = 2
        vozhatiy_id_col = 3
        komsorg_id_col = 4

        for i in range(first_row, Parser.get_row_length(sheet) + 1):
            id = Parser.get_cell_value(sheet, id_col, i)
            name = Parser.get_cell_value(sheet, name_col, i)
            vozhatiy_id = Parser.get_cell_value(sheet, vozhatiy_id_col, i)
            komsorg_id = Parser.get_cell_value(sheet, komsorg_id_col, i)

            squad = Squad(id, name, vozhatiy_id, komsorg_id)
            squads.append(squad)

        return squads

    def parse_services(sheet):
        services = []
        name_col = 1
        supervisor_id_col = 2

        for i in range(first_row, Parser.get_row_length(sheet) + 1):
            name = Parser.get_cell_value(sheet, name_col, i)
            supervisor_id = Parser.get_cell_value(sheet, supervisor_id_col, i)

            service = Service(name, supervisor_id)
            services.append(service)

        return services

    def parse_roles(sheet):
        roles = []
        id_col = 1
        name_col = 2
        plural_col = 3

        for i in range(first_row, Parser.get_row_length(sheet) + 1):
            id = Parser.get_cell_value(sheet, id_col, i)
            name = Parser.get_cell_value(sheet, name_col, i)
            plural = Parser.get_cell_value(sheet, plural_col, i)

            role = PersonRole(id, name, plural)
            roles.append(role)

        return roles

    def parse_commanders(sheet):
        commanders = []
        commander_id_col = 2
        commander_squad_id_col = 3

        for i in range(first_row, Parser.get_row_length(sheet) + 1):
            commander_id = Parser.get_cell_value(sheet, commander_id_col, i)
            commander_squad_id = Parser.get_cell_value(sheet, commander_squad_id_col, i)

            commander = Commander(commander_id, commander_squad_id)
            commanders.append(commander)

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

    people = parse_people(Parser.get_google_sheet(google_service, spreadsheet_id, 'People', 'A', 'F', 1))
    squads = parse_squads(Parser.get_google_sheet(google_service, spreadsheet_id, 'Squads', 'A', 'D', 1))
    commanders = parse_commanders(Parser.get_google_sheet(google_service, spreadsheet_id, 'Commanders', 'A', 'C', 1))
    services = parse_services(Parser.get_google_sheet(google_service, spreadsheet_id, 'Services', 'A', 'B', 1))
    roles = parse_roles(Parser.get_google_sheet(google_service, spreadsheet_id, 'Roles', 'A', 'C', 1))
    supervisors = parse_supervisors(Parser.get_google_sheet(google_service, spreadsheet_id, 'Supervisors', 'A', 'B', 1))
    info = parse_info(Parser.get_google_sheet(google_service, spreadsheet_id, 'Info', 'A', 'B', 1))


    return people, squads, commanders, services, roles, supervisors, info


def save_sbor(google_service, spreadsheet_id, commanders):
    first_row = 3

    def set_commanders(sheet, commanders):
        commander_id_col = 2
        commander_squad_id_col = 3

        for i in range(first_row, Parser.get_row_length(sheet) + 1):
            commander_squad_id = Parser.get_cell_value(sheet, commander_squad_id_col, i)
            commander_saved = False
            for commander in commanders:
                if commander_squad_id == commander.commander_squad_id:
                    Parser.set_cell_value(sheet, commander_id_col, i, commander.commander_id)
                    commander_saved = True
                    break

            if commander_saved:
                Parser.set_google_sheet(google_service, spreadsheet_id, 'Commanders', sheet, 'A', 'C', 1)
            else:
                raise Exception("Can't save all commanders")

    set_commanders(Parser.get_google_sheet(google_service, spreadsheet_id, 'Commanders', 'A', 'C', 1), commanders)


def get_admins(google_service, spreadsheet_id):
    first_row = 3

    def parse_admins(sheet):
        admins = []
        id_col = 1
        telegram_col = 2
        role_id_col = 3

        for i in range(first_row, Parser.get_row_length(sheet) + 1):
            id = Parser.get_cell_value(sheet, id_col, i)
            telegram = Parser.get_cell_value(sheet, telegram_col, i)
            role_id = Parser.get_cell_value(sheet, role_id_col, i)

            admin = Admin(id, telegram, role_id)
            admins.append(admin)

        return admins

    def parse_roles(sheet):
        adminRoles = []
        id_col = 1
        name_col = 2
        public_messages_col = 3
        see_ids_col = 4
        edit_timetable_col = 5
        edit_commanders_col = 6
        edit_admins_col = 7

        def role_right_to_bool(right):
            return True if right == '+' else False

        for i in range(first_row, Parser.get_row_length(sheet) + 1):
            id = Parser.get_cell_value(sheet, id_col, i)
            name = Parser.get_cell_value(sheet, name_col, i)
            public_messages = Parser.get_cell_value(sheet, public_messages_col, i)
            see_ids = Parser.get_cell_value(sheet, see_ids_col, i)
            edit_timetable = Parser.get_cell_value(sheet, edit_timetable_col, i)
            edit_commanders = Parser.get_cell_value(sheet, edit_commanders_col, i)
            manage_admins = Parser.get_cell_value(sheet, edit_admins_col, i)

            adminRole = AdminRole(
                id=id,
                name=name,
                public_messages=role_right_to_bool(public_messages),
                see_ids=role_right_to_bool(see_ids),
                edit_timetable=role_right_to_bool(edit_timetable),
                edit_commanders=role_right_to_bool(edit_commanders),
                manage_admins=role_right_to_bool(manage_admins)
            )
            adminRoles.append(adminRole)

        return adminRoles


    admins = parse_admins(Parser.get_google_sheet(google_service, spreadsheet_id, 'Admins', 'A', 'C', 1))
    roles = parse_roles(Parser.get_google_sheet(google_service, spreadsheet_id, 'Roles', 'A', 'G', 1))

    return admins, roles


def save_admins(admins, google_service, spreadsheet_id):
    first_row = 3

    def set_admins(sheet, admins):
        id_col = 1
        telegram_col = 2
        role_id_col = 3
        row = first_row

        for admin in admins:
            Parser.set_cell_value(sheet, id_col, row, admin.id)
            Parser.set_cell_value(sheet, telegram_col, row, admin.telegram)
            Parser.set_cell_value(sheet, role_id_col, row, admin.role_id)
            row += 1

        Parser.set_google_sheet(google_service, spreadsheet_id, 'Admins', sheet, 'A', 'C', 1)

    Parser.clear_google_sheet(google_service, spreadsheet_id, 'Admins', 'A', 'C', 3)
    set_admins(Parser.get_google_sheet(google_service, spreadsheet_id, 'Admins', 'A', 'C', 1), admins)


def get_users(file):
    user_ids = set()
    for line in file:
        user_ids.add(int(line))

    return user_ids


def save_users(file, users):
    for user in users:
        file.write('{}\n'.format(user))
