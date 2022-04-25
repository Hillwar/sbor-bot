import telebot
import config

from telebot import types

keyboard1 = telebot.types.ReplyKeyboardMarkup()
bot = telebot.TeleBot(config.TOKEN)
timetable = ''
list_of_servicemans = ''
dks = ''
group = 0
best_people = ['MikhKir', 'julia_severyanova', "EgorVkimow"]
markup = None
timetable_button_clicked = False
servisemans_button_clicked = False
dks_button_clicked = False


@bot.message_handler(commands=['start'])
def start(message):
    global markup, best_people
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    button_1 = types.KeyboardButton('Расписание')
    button_2 = types.KeyboardButton('ДКС')
    button_3 = types.KeyboardButton('Добавить')
    button_4 = types.KeyboardButton('Отряд 1')
    button_5 = types.KeyboardButton('Отряд 2')
    button_6 = types.KeyboardButton('Отряд 3')
    button_7 = types.KeyboardButton('Отряд 4')
    button_8 = types.KeyboardButton('Службисты')
    if message.from_user.username in best_people:
        markup.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8)
    else:
        markup.add(button_1, button_2, button_4, button_5, button_6, button_7, button_8)
    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def take_text(message):
    global timetable_button_clicked, dks_button_clicked, dks, markup, group, best_people, servisemans_button_clicked
    if message.text == 'Расписание':
        if timetable != '':
            photo = open(timetable, 'rb')
            bot.send_photo(message.chat.id, photo)
        else:
            bot.send_message(message.chat.id, 'Расписание не добавлено')
    elif message.text == 'Службисты':
        if list_of_servicemans != '':
            photo = open(list_of_servicemans, 'rb')
            bot.send_photo(message.chat.id, photo)
        else:
            bot.send_message(message.chat.id, 'Список службистов не добавлен')
    elif message.text == 'ДКС':
        if dks != '':
            bot.send_message(message.chat.id, dks)
        else:
            bot.send_message(message.chat.id, 'ДКС не добавлен')
    elif message.text == 'Добавить':
        local_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button_1 = types.KeyboardButton('Добавить расписание')
        button_2 = types.KeyboardButton('Добавить список службистов')
        button_3 = types.KeyboardButton('Добавить ДКС')
        button_4 = types.KeyboardButton('Назад')
        local_markup.add(button_1, button_2, button_3, button_4)
        bot.send_message(message.chat.id, message.text, reply_markup=local_markup)
    elif message.text == 'Добавить расписание':
        bot.send_message(message.chat.id, 'Отправьте фото расписания)')
        timetable_button_clicked = True
    elif message.text == 'Добавить список службистов':
        bot.send_message(message.chat.id, 'Отправьте фото списка службистов')
        servisemans_button_clicked = True
    elif message.text == 'Добавить ДКС':
        bot.send_message(message.chat.id, 'Введите имя')
        dks_button_clicked = True
    elif message.text == 'Добавить Службистов':
        bot.send_message(message.chat.id, 'Отправьте список службистов')
        servisemans_button_clicked = True
    elif message.text[:-1] == 'Отряд ':
        group = int(message.text[-1:])
        local_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        button_1 = types.KeyboardButton('Список отряда')
        button_2 = types.KeyboardButton('Комсорг')
        button_2 = types.KeyboardButton('ДКО')
        button_3 = types.KeyboardButton('Назад')
        local_markup.add(button_1, button_2, button_3)
        bot.send_message(message.chat.id, message.text, reply_markup=local_markup)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, message.text, reply_markup=markup)
        group = 0
        timetable_button_clicked = False
        dks_button_clicked = False
    elif message.text == 'Список отряда':
        if group != 0:
            timetable_of_group = open('resource/timetable_' + str(group) + '.png', 'rb')
            bot.send_photo(message.chat.id, timetable_of_group)
    elif message.text == 'Комсорг':
        if group != 0:
            bot.send_message(message.chat.id, 'Комсорг отряда ' + str(group))
    elif message.text == 'ДКО':
        if group != 0:
            bot.send_message(message.chat.id, 'ДКО отряда ' + str(group))
    elif dks_button_clicked and message.from_user.username in best_people:
        dks = message.text
        dks_button_clicked = False


@bot.message_handler(content_types=['photo'])
def take_photo(message):
    global timetable, timetable_button_clicked, servisemans_button_clicked, list_of_servicemans
    if timetable_button_clicked:
        file = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file.file_path)
        timetable = 'resource/timetable.png'
        with open('resource/timetable.png', 'wb') as new_file:
            new_file.write(downloaded_file)
        timetable_button_clicked = False
    elif servisemans_button_clicked:
        file = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file.file_path)
        list_of_servicemans = 'resource/servicemans.png'
        with open('resource/servicemans.png', 'wb') as new_file:
            new_file.write(downloaded_file)
        servisemans_button_clicked = False


bot.polling(none_stop=True)
