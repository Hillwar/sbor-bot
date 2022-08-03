class Parser:
    @staticmethod
    def get_cell_value(sheet, col, row):
        value = sheet.cell(row=row, column=col).value
        return value

    @staticmethod
    def set_cell_value(sheet, col, row, value):
        sheet.cell(row=row, column=col, value=value)
