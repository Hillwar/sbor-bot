TOKEN = '5248759255:AAF9LH5NoSFcTj2r_obycP2uPjoashqvMM8'

class Admins:
    list = ['MikhKir', 'julia_severyanova', "EgorVkimow"]

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

    class Data:
        sbor = Paths.data + '/sbor_data.xlsx'
        admins = Paths.data + '/admins.txt'