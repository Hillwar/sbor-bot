class Tools:
    @staticmethod
    def get_index(index, max_index, left_bracket = '', right_bracket = ''):
        if max_index > 999:
            return '{}{:04}{}'.format(left_bracket, index, right_bracket)
        elif max_index > 99:
            return '{}{:03}{}'.format(left_bracket, index, right_bracket)
        elif max_index > 9:
            return '{}{:02}{}'.format(left_bracket, index, right_bracket)
        else:
            return '{}{:01}{}'.format(left_bracket, index, right_bracket)

    @staticmethod
    def bool_to_russian(value):
        return 'Да' if value else 'Нет'


    @staticmethod
    def check_list_for(list, predicate):
        for value in list:
            if predicate(value):
                return True

        return False

    @staticmethod
    def in_range(value, min, max):
        return value >= min and value <= max

    @staticmethod
    def get_russian_number(number):
        if not number:
            return None

        return '+7' + str(number)