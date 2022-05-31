import imp
import resource
from tabnanny import check
from tkinter.messagebox import YES
import telebot
import config
from parser import parse

from config import Admins, Resources
from sbor import Sbor
from people import Person
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
sbor = Sbor(Resources.Data.sbor)


def is_admin(user):
    return user.username in Admins.list

class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    # Class will check whether the user is admin or creator in group or not
    key='is_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return is_admin(message.from_user)

# To register filter, you need to use method add_custom_filter.
bot.add_custom_filter(IsAdmin())

class Buttons:
    class Main:
        timetable = types.KeyboardButton(text = 'Расписание')
        commanders = types.KeyboardButton(text = 'ДКС и ДКО')
        squads = types.KeyboardButton(text = 'Отряды')
        services = types.KeyboardButton(text = 'Службисты')
        people = types.KeyboardButton(text = 'Люди')
        other = types.KeyboardButton(text = 'Другое')

    class General:
        cancel = types.InlineKeyboardButton(text = 'Отмена', callback_data = 'cancel')

    class Other:
        search = types.InlineKeyboardButton(text = 'Поиск человека', callback_data = 'other search')
        edit = types.InlineKeyboardButton(text = 'Изменить данные', callback_data = 'other edit')

    class Edit:
        timetable = types.InlineKeyboardButton(text = 'Изменить расписание', callback_data = 'edit timetable')
        commanders = types.InlineKeyboardButton(text = 'Изменить ДКС и ДКО', callback_data = 'edit commanders')
        admins = types.InlineKeyboardButton(text = 'Изменить админов', callback_data = 'edit admins')

        class Commanders:
            yes = types.InlineKeyboardButton(text = 'Да', callback_data = 'edit_commanders yes')
            no = types.InlineKeyboardButton(text = 'Нет', callback_data = 'edit_commanders no')

    class Timetable:
        today = types.InlineKeyboardButton(text = 'Расписание на сегодня', callback_data = 'timetable today')
        sbor = types.InlineKeyboardButton(text = 'Расписание на сбор', callback_data = 'timetable sbor')

    class Squads:
        all = types.InlineKeyboardButton(text = 'Все отряды', callback_data = 'squads show_squads')
        concrete = []
        hide_buttons = types.InlineKeyboardButton(text = 'Скрыть кнопки', callback_data = 'squads hide_buttons')
        show_buttons = types.InlineKeyboardButton(text = 'Показать кнопки', callback_data = 'squads show_buttons')
        for squad_id in range(1, sbor.get_squads_count() + 1):
            #buttons_squad.append(types.KeyboardButton('Отряд \'' + sbor.get_squad(squad_id).name + '\''))
            concrete.append(types.InlineKeyboardButton(text = 'Отряд \'' + sbor.get_squad(squad_id).name + '\'', callback_data = 'squads show_squad ' + str(squad_id)))

    class People:
        sort = types.InlineKeyboardButton(text = 'Сортировать', callback_data = 'people sort')
        group = types.InlineKeyboardButton(text = 'Группировать', callback_data = 'people group')
        hide_buttons = types.InlineKeyboardButton(text = 'Скрыть кнопки', callback_data = 'people hide_buttons')
        show_buttons = types.InlineKeyboardButton(text = 'Показать кнопки', callback_data = 'people show_buttons')
        back = types.InlineKeyboardButton(text = 'Назад', callback_data = 'people back')

        class Sort:
            by_id = types.InlineKeyboardButton(text = 'Сортировать по ID', callback_data = 'people_sort id')
            by_name = types.InlineKeyboardButton(text = 'Сортировать по имени', callback_data = 'people_sort name')
            by_surname = types.InlineKeyboardButton(text = 'Сортировать по фамилии', callback_data = 'people_sort surname')


class Markup:
    remove = types.ReplyKeyboardRemove()

    class Main:
        show = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
        show.add(Buttons.Main.timetable, Buttons.Main.commanders, Buttons.Main.squads, Buttons.Main.services, Buttons.Main.people, Buttons.Main.other)

    class Other:
        def show(user):
            markup = types.InlineKeyboardMarkup(row_width = 1)
            if is_admin(user):
                markup.add(Buttons.Other.edit)
            markup.add(Buttons.Other.search, Buttons.General.cancel)
            return markup

    class Edit:
        show = types.InlineKeyboardMarkup(row_width = 1)
        show.add(Buttons.Edit.timetable, Buttons.Edit.commanders, Buttons.Edit.admins, Buttons.General.cancel)

        commander_confirm = types.InlineKeyboardMarkup(row_width = 2)
        commander_confirm.add(Buttons.Edit.Commanders.yes, Buttons.Edit.Commanders.no)

    class Timetable:
        show = types.InlineKeyboardMarkup(row_width = 1)
        show.add(Buttons.Timetable.today, Buttons.Timetable.sbor)

    class Squads:
        show = types.InlineKeyboardMarkup(row_width = 1)
        for squad in Buttons.Squads.concrete:
            show.add(squad)
        show.add(Buttons.Squads.all, Buttons.Squads.hide_buttons)

        hide = types.InlineKeyboardMarkup(row_width = 1)
        hide.add(Buttons.Squads.show_buttons)

    class People:
        show = types.InlineKeyboardMarkup(row_width = 1)
        show.add(Buttons.People.sort, Buttons.People.hide_buttons)

        hide = types.InlineKeyboardMarkup(row_width = 1)
        hide.add(Buttons.People.show_buttons)

        def sort(user):
            markup = types.InlineKeyboardMarkup(row_width = 1)
            if is_admin(user):
                markup.add(Buttons.People.Sort.by_id)
            markup.add(Buttons.People.Sort.by_name, Buttons.People.Sort.by_surname, Buttons.People.back)
            return markup

def send_message(message, text = None, reply_markup = None):
    return bot.send_message(message.chat.id, text = text, reply_markup = reply_markup, parse_mode='Markdown')

def edit_message(message, text = None, reply_markup = None):
    return bot.edit_message_text(chat_id = message.chat.id, message_id = message.message_id, text = text, reply_markup = reply_markup, parse_mode='Markdown')

def send_menu(message, photo_path = Resources.Images.background, text = None, reply_markup = None):
    main_background = open(photo_path, 'rb')
    if not main_background:
        return

    return bot.send_photo(message.chat.id, photo=main_background, caption=text, reply_markup = reply_markup, parse_mode='Markdown')

def edit_menu(message, text = None, reply_markup = None):
    return bot.edit_message_caption(chat_id = message.chat.id, message_id = message.message_id, caption = text, reply_markup = reply_markup, parse_mode='Markdown')


def show_timetable(message):
    send_menu(message, photo_path = Resources.Timetable.today, reply_markup = Markup.Timetable.show)

def show_services(message):
    services_info = sbor.get_services_info()
    send_message(message, text = services_info)

def show_squads(message):
    send_menu(message, reply_markup = Markup.Squads.show)

def show_duties(message):
    duties_info = sbor.get_duties_info()
    send_message(message, text = duties_info)

def show_people(message):
    info = Person.Info.Full if is_admin(message.from_user) else Person.Info.Compact
    send_menu(message, text = sbor.get_all_people_info(Person.Sort.surname, info), reply_markup = Markup.People.show)

def show_other(message):
    send_menu(message, reply_markup = Markup.Other.show(message.from_user))

def show_edit(message):
    send_menu(message, reply_markup=Markup.Edit.show)


@bot.message_handler(commands=['start'])
def start_command(message):
    send_message(message, 'Привет!', reply_markup = Markup.Main.show)

@bot.message_handler(commands=['restart'])
def restart_command(message):
    start_command(message)

@bot.message_handler(commands=['edit'], is_admin = True)
def edit_command(message):
    show_edit(message)


@bot.message_handler(content_types=['text'])
def take_text(message):
    if message.text == 'Расписание':
        show_timetable(message)
    elif message.text == 'ДКС и ДКО':
        show_duties(message)
    elif message.text == 'Отряды':
        show_squads(message)
    elif message.text == 'Службисты':
        show_services(message)
    elif message.text == 'Люди':
        show_people(message)
    elif message.text == 'Другое':
        show_other(message)

@bot.callback_query_handler(func = lambda call: call.data.split()[0] == 'other')
def other_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'search':
        edit_menu(call.message, text = 'Кнопка \'Поиск человека\' пока не доступна')
    elif keyword == 'edit':
        bot.edit_message_reply_markup(chat_id = call.message.chat.id,message_id = call.message.message_id, reply_markup = Markup.Edit.show)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func = lambda call: call.data.split()[0] == 'edit', is_admin = True)
def edit_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'timetable':
        message = edit_menu(call.message, 'Отправьте фото расписания)')
        bot.register_next_step_handler(message, edit_timetable)
    elif keyword == 'commanders':
        message = edit_menu(call.message, 'Отправьте ID ДКС и всех ДКО через пробел. ДКС обязательно первым!')
        bot.register_next_step_handler(message, edit_commanders)
    elif keyword == 'admins':
        edit_menu(call.message, 'Кнопка \'Изменить админов\' пока не доступна', reply_markup = Markup.Edit.show)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func = lambda call: call.data.split()[0] == 'edit_commanders', is_admin = True)
def edit_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'yes':
        edit_message(call.message, '{}\n\n*Информация сохранена!*'.format(sbor.get_duties_info(Person.Info.Debug)))
        sbor.save()
    elif keyword == 'no':
        edit_message(call.message, '{}\n\n*Информация не сохранена*'.format(sbor.get_duties_info(Person.Info.Debug)))
        sbor.load()
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func = lambda call: call.data.split()[0] == 'timetable')
def timetable_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'today':
        edit_menu(call.message, 'Кнопка \'Расписание на сегодня\' пока не доступна', reply_markup = Markup.Timetable.show)
    elif keyword == 'sbor':
        edit_menu(call.message, 'Кнопка \'Расписание на сбор\' пока не доступна', reply_markup = Markup.Timetable.show)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func = lambda call: call.data.split()[0] == 'squads')
def squads_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'show_squad':
        squad_id = int(call.data[-1:])
        squad = sbor.get_squad(squad_id)
        squad_info = sbor.get_squad_info_with_people(squad)
        edit_menu(call.message, text = squad_info, reply_markup = Markup.Squads.show)
    elif keyword == 'show_squads':
        squads_info = sbor.get_squads_info()
        edit_menu(call.message, text = squads_info, reply_markup = Markup.Squads.show)
    elif keyword == 'hide_buttons':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup = Markup.Squads.hide)
    elif keyword == 'show_buttons':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup = Markup.Squads.show)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func = lambda call: call.data.split()[0] == 'people')
def people_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'sort':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup = Markup.People.sort(call.from_user))
    elif keyword == 'hide_buttons':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup = Markup.People.hide)
    elif keyword == 'show_buttons':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup = Markup.People.show)
    elif keyword == 'back':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup = Markup.People.show)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func = lambda call: call.data.split()[0] == 'people_sort')
def people_sort_callback(call):
    keyword = call.data.split()[1]
    info = Person.Info.Full if is_admin(call.from_user) else Person.Info.Compact
    if keyword == 'id':
        edit_menu(call.message, text = sbor.get_all_people_info(Person.Sort.id, info), reply_markup = Markup.People.sort(call.from_user))
    elif keyword == 'name':
        edit_menu(call.message, text = sbor.get_all_people_info(Person.Sort.name, info, name_first = True), reply_markup = Markup.People.sort(call.from_user))
    elif keyword == 'surname':
        edit_menu(call.message, text = sbor.get_all_people_info(Person.Sort.surname, info), reply_markup = Markup.People.sort(call.from_user))
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func = lambda call: call.data.split()[0] == 'cancel')
def people_group_callback(call):
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    bot.answer_callback_query(call.id)

def save_photo(message, path):
    if not message.photo:
        return False

    file = bot.get_file(message.photo[-1].file_id)
    photo = bot.download_file(file.file_path)
    with open(path, 'wb') as photo_file:
        photo_file.write(photo)

    return True

def edit_timetable(message):
    result = save_photo(message, Resources.Timetable.today)
    if not result:
        send_message(message, 'Это не фото расписания. Выход из режима изменения расписания.')
        return

    send_message(message, 'Новое расписание сохранено!')

def edit_commanders(message):
    if not message.text:
        send_message(message, 'Вы не передали ID новых коммандиров. Выход из режима изменения ДКС и ДКО.')
        return

    id_strings = message.text.split()

    ids = []
    for id_string in id_strings:
        id = int(id_string)
        if not id:
            send_message(message, 'Вы должны передать ID командиров. Выход из режима изменения ДКС и ДКО.'.format(sbor.get_people_count()))
            return
        ids.append(id)

    result, error = sbor.edit_commanders(ids[0], ids[1:])
    if result:
        send_message(message, '{}\n\n*Информация верна?*'.format(sbor.get_duties_info(Person.Info.Debug)), reply_markup = Markup.Edit.commander_confirm)
    else:
        send_message(message, error + ' Выход из режима изменения ДКС и ДКО.')


bot.polling(none_stop=True)
