import telebot
import config
from parser import parse

from sbor import Sbor
from telebot import types


bot = telebot.TeleBot(config.TOKEN)
sbor = Sbor()
timetable = ''
best_people = ['MikhKir', 'julia_severyanova', "EgorVkimow"]
timetable_buttons_clicked = False

class Buttons:
    timetable = types.KeyboardButton('Расписание')
    commanders = types.KeyboardButton('ДКС и ДКО')
    squads = types.KeyboardButton('Отряды')
    services = types.KeyboardButton('Службисты')
    edit = types.KeyboardButton('Изменить')
    back = types.KeyboardButton('Назад')

    edit_timetable = types.KeyboardButton('Изменить расписание')
    edit_commanders = types.KeyboardButton('Изменить ДКС и ДКО')

    show_all_squads = types.KeyboardButton('Все отряды')
    show_squad = []
    for squad_id in range(1, sbor.get_squads_count() + 1):
        #buttons_squad.append(types.KeyboardButton('Отряд \'' + sbor.get_squad(squad_id).name + '\''))
        show_squad.append(types.KeyboardButton('Отряд ' + str(squad_id)))

class Markup:
    main = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    main.add(Buttons.timetable, Buttons.commanders, Buttons.squads, Buttons.services)

    edit = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    edit.add(Buttons.edit_timetable, Buttons.edit_commanders, Buttons.back)

    squads = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for squad in Buttons.show_squad:
        squads.add(squad)
    squads.add(Buttons.show_all_squads, Buttons.back)

def send_message(message, text, reply_markup = None):
    bot.send_message(message.chat.id, text, reply_markup = reply_markup, parse_mode='Markdown')

def show_timetable(message):
    if timetable != '':
        photo = open(timetable, 'rb')
        bot.send_photo(message.chat.id, photo)
    else:
        send_message(message, 'Расписание не добавлено')

def show_services(message):
    services_info = sbor.get_services_info()
    send_message(message, services_info)

def show_squads(message):
    squads_info = sbor.get_squads_info()
    send_message(message, squads_info)

def show_squad(message, squad_id):
    squad = sbor.get_squad(squad_id)
    squad_info = sbor.get_squad_info_with_people(squad)
    send_message(message, squad_info)

def show_duties(message):
    duties_info = sbor.get_duties_info()
    send_message(message, duties_info)


@bot.message_handler(commands=['start'])
def start(message):
    global best_people
    if message.from_user.username in best_people:
        Markup.main.add(Buttons.edit)

    send_message(message, 'Привет', reply_markup=Markup.main)


@bot.message_handler(content_types=['text'])
def take_text(message):
    global timetable_buttons_clicked, markup, best_people
    if message.text == 'Расписание':
        show_timetable(message)
    elif message.text == 'Службисты':
        show_services(message)
    elif message.text == 'ДКС и ДКО':
        show_duties(message)

    elif message.text == 'Отряды':
        send_message(message, message.text, reply_markup=Markup.squads)
    elif message.text.split()[0] == 'Отряд':
        squad = int(message.text[-1:])
        show_squad(message, squad)
    elif message.text == 'Все отряды':
        show_squads(message)

    elif message.text == 'Изменить':
        send_message(message, message.text, reply_markup=Markup.edit)
    elif message.text == 'Изменить расписание':
        send_message(message, 'Отправьте фото расписания)')
        timetable_buttons_clicked = True
    elif message.text == 'Изменить ДКС и ДКО':
        send_message(message, 'Пока не доступно')

    elif message.text == 'Назад':
        send_message(message, message.text, reply_markup=Markup.main)
        timetable_buttons_clicked = False


@bot.message_handler(content_types=['photo'])
def take_photo(message):
    global timetable, timetable_buttons_clicked
    if timetable_buttons_clicked:
        file = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file.file_path)
        timetable = 'resource/timetable.png'
        with open('resource/timetable.png', 'wb') as new_file:
            new_file.write(downloaded_file)
        timetable_buttons_clicked = False


bot.polling(none_stop=True)
