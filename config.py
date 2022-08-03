import enum
TOKEN = '5539809650:AAHs5klO3qZy10OMLkrTS_SJ5QdBN4WnCcs'

class BotType(enum.Enum):
    Sbor = 1
    Solovki = 2

class Bot:
    type = BotType.Sbor

class Paths:
    resource = 'resource'
    data = resource + '/data'
    images = resource + '/images'
    timetable = resource + '/timetable'


class Resources:
    class Timetable:
        today = Paths.timetable + '/today.png'
        all = Paths.timetable + '/all.png'

    class Images:
        background_1 = Paths.images + '/background_1.jpg'
        background_2 = Paths.images + '/background_2.jpg'
        background_3 = Paths.images + '/background_3.jpg'
        background_4 = Paths.images + '/background_4.jpg'
        background_5 = Paths.images + '/background_5.jpg'

    class Data:
        excel = Paths.data + '/sbor_data.xlsx'
        admins = Paths.data + '/admins.xlsx'
        users = Paths.data + '/users.txt'
