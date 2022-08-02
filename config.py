TOKEN = '5539809650:AAHs5klO3qZy10OMLkrTS_SJ5QdBN4WnCcs'
spreadsheet_id = '1WnmZeMH7uOJ3tz9YgyClo9wFUGulasIeR7dBg7-ZzaY'


class Paths:
    resource = 'resource'
    images = resource + '/images'
    timetable = resource + '/timetable'


class Resources:
    class Timetable:
        today = Paths.timetable + '/today.png'
        sbor = Paths.timetable + '/sbor.png'

    class Images:
        background_1 = Paths.images + '/background_1.jpg'
        background_2 = Paths.images + '/background_2.jpg'
        background_3 = Paths.images + '/background_3.jpg'
        background_4 = Paths.images + '/background_4.jpg'
        background_5 = Paths.images + '/background_5.jpg'

    class Data:
        pass
