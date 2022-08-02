from people import Admin, AdminRole, DutySquad, Service, Person, PersonRole, Squad, Commander, Info
from config import spreadsheet_id

service = None

def get_cell_value(sheet, col, row):
    value = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet}!{chr(64 + col)}{row}:{chr(64 + col)}{row}",
        majorDimension='COLUMNS'
    ).execute()
    return value["values"][0][0]


def set_cell_value(sheet, col, row, value):
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"{sheet}!{chr(64 + col)}{row}:{chr(64 + col)}{row}",
                 "majorDimension": "ROWS",
                 "values": [[value]]}
            ]
        }
    ).execute()


def get_sbor(serv):
    global service
    service = serv
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

    def parse_supervisors(sheet):
        supervisors = []
        name_col = 1
        supervisor_id_col = 2
        row = first_row

        while get_cell_value(sheet, name_col, row):
            name = get_cell_value(sheet, name_col, row)
            supervisor_id = get_cell_value(sheet, supervisor_id_col, row)

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
        name_col = 1
        supervisor_id_col = 2
        row = first_row

        while get_cell_value(sheet, name_col, row):
            name = get_cell_value(sheet, name_col, row)
            supervisor_id = get_cell_value(sheet, supervisor_id_col, row)

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

        while get_cell_value(sheet, id_col, row):
            id = get_cell_value(sheet, id_col, row)
            name = get_cell_value(sheet, name_col, row)
            plural = get_cell_value(sheet, plural_col, row)

            role = PersonRole(id, name, plural)
            roles.append(role)
            row += 1

        return roles

    def parse_commanders(sheet):
        commanders = []
        commander_id_col = 2
        commander_squad_id_col = 3
        row = first_row

        while get_cell_value(sheet, commander_id_col, row):
            commander_id = get_cell_value(sheet, commander_id_col, row)
            commander_squad_id = get_cell_value(sheet, commander_squad_id_col, row)

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

        number = get_cell_value(sheet, col, number_row)
        dks_number = get_cell_value(sheet, col, dks_number_row)
        adress = get_cell_value(sheet, col, adress_row)
        location_link = get_cell_value(sheet, col, location_link_row)
        vk_link = get_cell_value(sheet, col, vk_link_row)

        return Info(number, dks_number, adress, location_link, vk_link)

    people = parse_people('People')
    squads = parse_squads('Squads')
    commanders = parse_commanders('Commanders')
    services = parse_services('Services')
    roles = parse_roles('Roles')
    supervisors = parse_supervisors('Supervisors')
    info = parse_info('Info')

    return people, squads, commanders, services, roles, supervisors, info


def save_sbor(commanders):
    first_row = 3

    def set_commanders(sheet, commanders):
        commander_id_col = 2
        commander_squad_id_col = 3
        row = first_row

        while get_cell_value(sheet, commander_id_col, row):
            commander_squad_id = get_cell_value(sheet, commander_squad_id_col, row)
            commander_saved = False
            for commander in commanders:
                if commander_squad_id == commander.commander_squad_id:
                    set_cell_value(sheet, commander_id_col, row, commander.commander_id)
                    commander_saved = True
                    break

            if not commander_saved:
                raise Exception("Can't save all commanders")

            row += 1

    set_commanders('Commanders', commanders)


def get_admins():
    first_row = 3

    def parse_admins(sheet):
        admins = []
        id_col = 1
        telegram_col = 2
        role_id_col = 3
        row = first_row

        while get_cell_value(sheet, id_col, row):
            id = get_cell_value(sheet, id_col, row)
            telegram = get_cell_value(sheet, telegram_col, row)
            role_id = get_cell_value(sheet, role_id_col, row)

            admin = Admin(id, telegram, role_id)
            admins.append(admin)
            row += 1

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
        row = first_row

        def role_right_to_bool(right):
            return True if right == '+' else False

        while get_cell_value(sheet, id_col, row):
            id = get_cell_value(sheet, id_col, row)
            name = get_cell_value(sheet, name_col, row)
            public_messages = get_cell_value(sheet, public_messages_col, row)
            see_ids = get_cell_value(sheet, see_ids_col, row)
            edit_timetable = get_cell_value(sheet, edit_timetable_col, row)
            edit_commanders = get_cell_value(sheet, edit_commanders_col, row)
            manage_admins = get_cell_value(sheet, edit_admins_col, row)

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
            row += 1

        return adminRoles

    admins = parse_admins('Admins')
    roles = parse_roles('Roles')

    return admins, roles


def save_admins(admins):
    first_row = 3

    def set_admins(sheet, admins):
        id_col = 1
        telegram_col = 2
        role_id_col = 3
        row = first_row

        for admin in admins:
            set_cell_value(sheet, id_col, row, admin.id)
            set_cell_value(sheet, telegram_col, row, admin.telegram)
            set_cell_value(sheet, role_id_col, row, admin.role_id)
            row += 1

        set_cell_value(sheet, id_col, row, '')
        set_cell_value(sheet, telegram_col, row, '')
        set_cell_value(sheet, role_id_col, row, '')

    set_admins('Admins', admins)


def get_users(file):
    user_ids = set()
    for line in file:
        user_ids.add(int(line))

    return user_ids


def save_users(file, users):
    for user in users:
        file.write('{}\n'.format(user))
