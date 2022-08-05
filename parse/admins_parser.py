from parse.excel_parser import Parser
from people import Admin, AdminRole

def get_admins(workbook):
    first_row = 3

    def parse_admins(sheet):
        admins = []
        id_col = 1
        telegram_col = 2
        role_id_col = 3
        row = first_row

        while Parser.get_cell_value(sheet, id_col, row):
            id = Parser.get_cell_value(sheet, id_col, row)
            telegram = Parser.get_cell_value(sheet, telegram_col, row)
            role_id = Parser.get_cell_value(sheet, role_id_col, row)

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

        while Parser.get_cell_value(sheet, id_col, row):
            id = Parser.get_cell_value(sheet, id_col, row)
            name = Parser.get_cell_value(sheet, name_col, row)
            public_messages = Parser.get_cell_value(sheet, public_messages_col, row)
            see_ids = Parser.get_cell_value(sheet, see_ids_col, row)
            edit_timetable = Parser.get_cell_value(sheet, edit_timetable_col, row)
            edit_commanders = Parser.get_cell_value(sheet, edit_commanders_col, row)
            manage_admins = Parser.get_cell_value(sheet, edit_admins_col, row)

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

    admins = parse_admins(workbook.get_sheet_by_name('Admins'))
    roles = parse_roles(workbook.get_sheet_by_name('Roles'))

    return admins, roles


def save_admins(workbook, path, admins):
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

        Parser.set_cell_value(sheet, id_col, row, '')
        Parser.set_cell_value(sheet, telegram_col, row, '')
        Parser.set_cell_value(sheet, role_id_col, row, '')

    set_admins(workbook.get_sheet_by_name('Admins'), admins)
    workbook.save(path)
