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
        background = Paths.images + '/background_main.png'

    class Data:
        sbor = Paths.data + '/sbor_data.xlsx'
        admins = Paths.data + '/admins.txt'