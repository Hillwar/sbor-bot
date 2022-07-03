TOKEN = '5393211268:AAE4FCSHsf1HICn7Y0MBi4zc68uWVn8ObOc'

class Paths:
    resource = 'resource'
    data = resource + '/data'
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
        background_gay = Paths.images + '/background_gay_special.jpg'
        temporary = Paths.images + '/temporary.png'

    class Data:
        sbor = Paths.data + '/sbor_data.xlsx'
        admins = Paths.data + '/admins.xlsx'
        users = Paths.data + '/users.txt'
