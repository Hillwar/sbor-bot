import sys


class Tools:
    @staticmethod
    def get_index(index, max_index, left_bracket='', right_bracket=''):
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
        return min <= value <= max

    @staticmethod
    def get_russian_number(number):
        if not number:
            return None

        return '+7' + str(number)

    @staticmethod
    def log(message=None, call=None):
        if "log" in sys.argv:
            print("<!------!>")
            from datetime import datetime
            print(datetime.now())
            if message:
                print("Сообщение от {0} {1} (id = {2}) \n {3}".format(message.from_user.first_name,
                                                                      message.from_user.last_name,
                                                                      str(message.from_user.id), message.text))
            else:
                print("Команда от {0} {1} (id = {2}) \n {3}".format(call.from_user.first_name,
                                                                    call.from_user.last_name,
                                                                    str(call.from_user.id), call.data))
