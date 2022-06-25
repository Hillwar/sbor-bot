from modulefinder import ReplacePackage
from re import I
import telebot
import config

from config import Resources
from sbor import Sbor
from people import Person
from telebot import types
from users import Admins, Users

bot = telebot.TeleBot(config.TOKEN)
sbor = Sbor(Resources.Data.sbor)
admins = Admins(Resources.Data.admins)
users = Users(Resources.Data.users)


def is_right_user(user, right_usernames):
    return user.username in right_usernames


class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_admin'

    @staticmethod
    def check(message: telebot.types.Message):
        return is_right_user(message.from_user, admins.get_users_in_admins_list())


bot.add_custom_filter(IsAdmin())


class Buttons:
    class Main:
        timetable = types.KeyboardButton(text='Расписание')
        commanders = types.KeyboardButton(text='ДКС и ДКО')
        squads = types.KeyboardButton(text='Отряды')
        services = types.KeyboardButton(text='Службисты')
        people = types.KeyboardButton(text='Люди')
        other = types.KeyboardButton(text='Другое')

    class General:
        cancel = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')

    class Other:
        search = types.InlineKeyboardButton(text='Поиск человека', callback_data='other search')
        edit = types.InlineKeyboardButton(text='Изменить данные', callback_data='other edit')
        admins = types.InlineKeyboardButton(text='Управление админами', callback_data='other admins')
        message = types.InlineKeyboardButton(text='Опубликовать сообщение', callback_data='other message')

    class Edit:
        timetable = types.InlineKeyboardButton(text='Изменить расписание', callback_data='edit timetable')
        commanders = types.InlineKeyboardButton(text='Изменить ДКС и ДКО', callback_data='edit commanders')

    class Admins:
        list = types.InlineKeyboardButton(text='Список админов', callback_data='admins list')
        roles = types.InlineKeyboardButton(text='Типы ролей', callback_data='admins roles')
        add = types.InlineKeyboardButton(text='Добавить админа', callback_data='admins add')
        remove = types.InlineKeyboardButton(text='Удалить админа', callback_data='admins remove')
        edit_role = types.InlineKeyboardButton(text='Изменить роль админа', callback_data='admins edit_role')

    class Timetable:
        today = types.InlineKeyboardButton(text='Показать расписание на сегодня', callback_data='timetable today')
        sbor = types.InlineKeyboardButton(text='Показать расписание на сбор', callback_data='timetable sbor')
        today_refresh = types.InlineKeyboardButton(text='Обновить', callback_data='timetable today_refresh')

    class Squads:
        all = types.InlineKeyboardButton(text='Все отряды', callback_data='squads show_squads')
        concrete = []
        hide_buttons = types.InlineKeyboardButton(text='Скрыть кнопки', callback_data='squads hide_buttons')
        show_buttons = types.InlineKeyboardButton(text='Показать кнопки', callback_data='squads show_buttons')
        for squad_id in range(1, sbor.get_squads_count() + 1):
            # buttons_squad.append(types.KeyboardButton('Отряд \'' + sbor.get_squad(squad_id).name + '\''))
            concrete.append(types.InlineKeyboardButton(text='Отряд \'' + sbor.get_squad(squad_id).name + '\'',
                                                       callback_data='squads show_squad ' + str(squad_id)))

    class People:
        sort = types.InlineKeyboardButton(text='Сортировать', callback_data='people sort')
        group = types.InlineKeyboardButton(text='Группировать', callback_data='people group')
        hide_buttons = types.InlineKeyboardButton(text='Скрыть кнопки', callback_data='people hide_buttons')
        show_buttons = types.InlineKeyboardButton(text='Показать кнопки', callback_data='people show_buttons')
        back = types.InlineKeyboardButton(text='Назад', callback_data='people back')

        class Sort:
            by_id = types.InlineKeyboardButton(text='Сортировать по ID', callback_data='people_sort id')
            by_name = types.InlineKeyboardButton(text='Сортировать по имени', callback_data='people_sort name')
            by_surname = types.InlineKeyboardButton(text='Сортировать по фамилии', callback_data='people_sort surname')


class Markup:
    remove = types.ReplyKeyboardRemove()

    class Main:
        show = types.ReplyKeyboardRemove()
        # show = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
        # show.add(Buttons.Main.timetable, Buttons.Main.commanders, Buttons.Main.squads, Buttons.Main.services, Buttons.Main.people, Buttons.Main.other)

    class Exit:
        admins_add_exit = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        admins_add_exit.add(types.KeyboardButton(text='Выход из режима добавления админа'))

        admins_edit_role_exit = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        admins_edit_role_exit.add(types.KeyboardButton(text='Выход из режима изменения роли админа'))

        admins_remove_exit = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        admins_remove_exit.add(types.KeyboardButton(text='Выход из режима удаления админа'))

        commander_edit_exit = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        commander_edit_exit.add(types.KeyboardButton(text='Выход из режима изменения ДКС и ДКО'))

        people_search_exit = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        people_search_exit.add(types.KeyboardButton(text='Выход из режима поиска'))

        timetable_edit_exit = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        timetable_edit_exit.add(types.KeyboardButton(text='Выход из режима изменения расписания'))

        public_message_exit = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        public_message_exit.add(types.KeyboardButton(text='Выход из режима публикации сообщения'))

    class Other:
        def show(user):
            markup = types.InlineKeyboardMarkup(row_width=1)
            if is_right_user(user, admins.get_users_who_can_manage_admins()):
                markup.add(Buttons.Other.admins)
            if is_right_user(user, admins.get_users_who_can_edit_something()):
                markup.add(Buttons.Other.edit)
            if is_right_user(user, admins.get_users_who_can_public_messages()):
                markup.add(Buttons.Other.message)
            markup.add(Buttons.Other.search, Buttons.General.cancel)
            return markup

    class Edit:
        def show(user):
            markup = types.InlineKeyboardMarkup(row_width=1)
            if is_right_user(user, admins.get_users_who_can_edit_timetable()):
                markup.add(Buttons.Edit.timetable)
            if is_right_user(user, admins.get_users_who_can_edit_commanders()):
                markup.add(Buttons.Edit.commanders)

            markup.add(Buttons.General.cancel)
            return markup

    class Admins:
        show = types.InlineKeyboardMarkup(row_width=1)
        show.add(Buttons.Admins.list, Buttons.Admins.roles, Buttons.Admins.add, Buttons.Admins.edit_role,
                 Buttons.Admins.remove, Buttons.General.cancel)

    class Timetable:
        sbor = types.InlineKeyboardMarkup(row_width=1)
        sbor.add(Buttons.Timetable.today)

        today = types.InlineKeyboardMarkup(row_width=1)
        today.add(Buttons.Timetable.sbor, Buttons.Timetable.today_refresh)

    class Squads:
        show = types.InlineKeyboardMarkup(row_width=1)
        for squad in Buttons.Squads.concrete:
            show.add(squad)
        show.add(Buttons.Squads.all, Buttons.Squads.hide_buttons)

        hide = types.InlineKeyboardMarkup(row_width=1)
        hide.add(Buttons.Squads.show_buttons)

    class People:
        show = types.InlineKeyboardMarkup(row_width=1)
        show.add(Buttons.People.sort, Buttons.People.hide_buttons)

        hide = types.InlineKeyboardMarkup(row_width=1)
        hide.add(Buttons.People.show_buttons)

        def sort(user):
            markup = types.InlineKeyboardMarkup(row_width=1)
            if is_right_user(user, admins.get_users_who_can_see_ids()):
                markup.add(Buttons.People.Sort.by_id)
            markup.add(Buttons.People.Sort.by_name, Buttons.People.Sort.by_surname, Buttons.People.back)
            return markup


def send_message(id, photo_path=None, photo=None, text=None, reply_markup=None, parse_mode='Markdown'):
    if photo:
        return bot.send_photo(chat_id=id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode=parse_mode)
    elif photo_path:
        with open(photo_path, 'rb') as photo:
            return bot.send_photo(chat_id=id, photo=photo, caption=text, reply_markup=reply_markup,
                                  parse_mode=parse_mode)
    else:
        return bot.send_message(chat_id=id, text=text, reply_markup=reply_markup, parse_mode=parse_mode)


def edit_message(message, text=None, reply_markup=None, parse_mode='Markdown'):
    if message.photo:
        return bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption=text,
                                        reply_markup=reply_markup, parse_mode=parse_mode)
    else:
        return bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text,
                                     reply_markup=reply_markup, parse_mode=parse_mode)


def edit_photo(message, photo_path=None, photo=None, reply_markup=None, parse_mode='Markdown'):
    if message.photo:
        if photo:
            media = types.InputMediaPhoto(photo)
            return bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id,
                                          reply_markup=reply_markup)
        elif photo_path:
            with open(photo_path, 'rb') as photo:
                media = types.InputMediaPhoto(photo)
                return bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id,
                                              reply_markup=reply_markup)
        else:
            return bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                         text='ОШИБКА! Вы не передали фото для изменения!', reply_markup=None,
                                         parse_mode=parse_mode)
    else:
        return bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                     text='ОШИБКА! У этого сообщения нет фото, которое можно изменить!',
                                     reply_markup=None, parse_mode=parse_mode)


def show_timetable(message):
    send_message(message.chat.id, photo_path=Resources.Timetable.today, reply_markup=Markup.Timetable.today)


def show_services(message):
    services_info = sbor.get_services_info()
    send_message(message.chat.id, photo_path=Resources.Images.background_3, text=services_info)


def show_squads(message):
    send_message(message.chat.id, photo_path=Resources.Images.background_1, reply_markup=Markup.Squads.show)


def show_duties(message):
    duties_info = sbor.get_duties_info()
    send_message(message.chat.id, photo_path=Resources.Images.background_5, text=duties_info)


def show_people(message):
    info = Person.Info.Compact
    send_message(message.chat.id, text=sbor.get_all_people_info(Person.Sort.surname, info),
                 reply_markup=Markup.People.show)


def show_other(message):
    send_message(message.chat.id, photo_path=Resources.Images.background_4,
                 reply_markup=Markup.Other.show(message.from_user))


def show_edit(message):
    if is_right_user(message.from_user, admins.get_users_who_can_edit_something()):
        send_message(message.chat.id, photo_path=Resources.Images.background_4,
                     reply_markup=Markup.Edit.show(message.from_user))


def show_admins(message):
    if is_right_user(message.from_user, admins.get_users_who_can_manage_admins()):
        send_message(message.chat.id, photo_path=Resources.Images.background_4, reply_markup=Markup.Admins.show)


def show_help(message):
    send_message(message.chat.id, text='help')


def show_sbor(message):
    sbor_info = sbor.get_sbor_info()
    send_message(message.chat.id, photo_path=Resources.Images.background_2, text=sbor_info)


@bot.message_handler(commands=['start'])
def start_command(message):
    users.add_user(message.from_user.id)
    users.save()
    send_message(message.chat.id, text='Привет!', reply_markup=Markup.Main.show)


@bot.message_handler(commands=['restart'])
def restart_command(message):
    start_command(message)


@bot.message_handler(commands=['edit'], is_admin=True)
def edit_command(message):
    show_edit(message)


@bot.message_handler(commands=['admins'], is_admin=True)
def admins_command(message):
    show_admins(message)


@bot.message_handler(commands=['help'])
def help_command(message):
    show_help(message)


@bot.message_handler(commands=['sbor'])
def help_command(message):
    show_sbor(message)


@bot.message_handler(commands=['timetable'])
def help_command(message):
    show_timetable(message)


@bot.message_handler(commands=['duties'])
def help_command(message):
    show_duties(message)


@bot.message_handler(commands=['squads'])
def help_command(message):
    show_squads(message)


@bot.message_handler(commands=['services'])
def help_command(message):
    show_services(message)


@bot.message_handler(commands=['people'])
def help_command(message):
    show_people(message)


@bot.message_handler(commands=['other'])
def help_command(message):
    show_other(message)


@bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'other')
def other_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'search':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=None)
        message = send_message(call.message.chat.id,
                               text='Введите имя и/или фамилию человека, которого хотите найти. *Лучше вводить только фамилию.*',
                               reply_markup=Markup.Exit.people_search_exit)
        bot.register_next_step_handler(message, find_people)
    elif keyword == 'message':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=None)
        message = send_message(call.message.chat.id,
                               text='Введите сообщение, которое хотите передать всему сбору.\n*Отправку нельзя отменить! Будьте бдительны!*',
                               reply_markup=Markup.Exit.public_message_exit)
        bot.register_next_step_handler(message, public_message)
    elif keyword == 'edit':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=Markup.Edit.show(call.from_user))
    elif keyword == 'admins':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=Markup.Admins.show)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'edit', is_admin=True)
def edit_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'timetable':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=None)
        message = send_message(call.message.chat.id, text='Отправьте фото расписания)',
                               reply_markup=Markup.Exit.timetable_edit_exit)
        bot.register_next_step_handler(message, edit_timetable, )
    elif keyword == 'commanders':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=None)
        message = send_message(call.message.chat.id,
                               text='Отправьте ID ДКС и всех ДКО через пробел. ДКС обязательно первым!',
                               reply_markup=Markup.Exit.commander_edit_exit)
        bot.register_next_step_handler(message, edit_commanders)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'admins')
def timetable_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'list':
        edit_message(call.message, text='*Список админов*')
        for admin in admins.get_admins_info():
            send_message(id=call.message.chat.id, text=admin)
    elif keyword == 'roles':
        edit_message(call.message, text='*Список ролей*')
        text = '\n\n'.join(admins.get_roles_info())
        send_message(id=call.message.chat.id, text=text)
    elif keyword == 'add':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=None)
        message = send_message(call.message.chat.id, text='Отправьте Telegram и ID роли нового админа',
                               reply_markup=Markup.Exit.admins_add_exit)
        bot.register_next_step_handler(message, add_admin)
    elif keyword == 'edit_role':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=None)
        message = send_message(call.message.chat.id, text='Отправьте ID админа и ID его новой роли',
                               reply_markup=Markup.Exit.admins_edit_role_exit)
        bot.register_next_step_handler(message, edit_role_of_admins)
    elif keyword == 'remove':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=None)
        message = send_message(call.message.chat.id, text='Отправьте ID админа, которого хотите удалить',
                               reply_markup=Markup.Exit.admins_remove_exit)
        bot.register_next_step_handler(message, remove_admin)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'timetable')
def timetable_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'today':
        edit_photo(call.message, photo_path=Resources.Timetable.today, reply_markup=Markup.Timetable.today)
    elif keyword == 'sbor':
        edit_photo(call.message, photo_path=Resources.Timetable.sbor, reply_markup=Markup.Timetable.sbor)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'squads')
def squads_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'show_squad':
        squad_id = int(call.data[-1:])
        squad = sbor.get_squad(squad_id)
        squad_info = sbor.get_squad_info_with_people(squad)
        edit_message(call.message, text=squad_info, reply_markup=Markup.Squads.hide)
    elif keyword == 'show_squads':
        squads_info = sbor.get_squads_info()
        edit_message(call.message, text=squads_info, reply_markup=Markup.Squads.hide)
    elif keyword == 'hide_buttons':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=Markup.Squads.hide)
    elif keyword == 'show_buttons':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=Markup.Squads.show)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'people')
def people_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'sort':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=Markup.People.sort(call.from_user))
    elif keyword == 'hide_buttons':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=Markup.People.hide)
    elif keyword == 'show_buttons':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=Markup.People.show)
    elif keyword == 'back':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=Markup.People.show)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'people_sort')
def people_sort_callback(call):
    keyword = call.data.split()[1]
    info = Person.Info.Compact
    if keyword == 'id':
        edit_message(call.message, text=sbor.get_all_people_info(Person.Sort.id, info),
                     reply_markup=Markup.People.sort(call.from_user))
    elif keyword == 'name':
        edit_message(call.message, text=sbor.get_all_people_info(Person.Sort.name, info, name_first=True),
                     reply_markup=Markup.People.sort(call.from_user))
    elif keyword == 'surname':
        edit_message(call.message, text=sbor.get_all_people_info(Person.Sort.surname, info),
                     reply_markup=Markup.People.sort(call.from_user))
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'cancel')
def people_group_callback(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
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
    if message.text and (message.text == 'Выход из режима изменения расписания' or message.text == 'Отмена'):
        send_message(message.chat.id, text='Отмена изменений', reply_markup=Markup.Main.show)
        return

    result = save_photo(message, Resources.Timetable.today)
    if not result:
        send_message(message.chat.id, text='Вы не передали фото расписания. Повторите.',
                     reply_markup=Markup.Exit.timetable_edit_exit)
        bot.register_next_step_handler(message, edit_timetable)
        return

    send_message(message.chat.id, text='Новое расписание сохранено!', reply_markup=Markup.Main.show)


def edit_commanders(message):
    if not message.text:
        send_message(message.chat.id, text='Вы не передали ID новых коммандиров. Повторите.',
                     reply_markup=Markup.Exit.commander_edit_exit)
        bot.register_next_step_handler(message, edit_commanders)
        return

    if message.text == 'Выход из режима изменения ДКС и ДКО' or message.text == 'Отмена':
        send_message(message.chat.id, text='Отмена изменений', reply_markup=Markup.Main.show)
        return

    id_strings = message.text.split()

    ids = []
    for id_string in id_strings:
        if not id_string.isdigit():
            send_message(message.chat.id,
                         text='Вы должны передать ID командиров. Повторите.'.format(sbor.get_people_count()))
            bot.register_next_step_handler(message, edit_commanders)
            return
        id = int(id_string)
        ids.append(id)

    result, error = sbor.edit_commanders(ids[0], ids[1:])
    if result:
        send_message(message.chat.id, text=sbor.get_duties_info(), reply_markup=Markup.Main.show)
        send_message(message.chat.id, text='Информация сохранена!')
        sbor.save()
    else:
        send_message(message.chat.id, text=error + ' Повторите.')
        bot.register_next_step_handler(message, edit_commanders)


def edit_role_of_admins(message):
    if not message.text:
        send_message(message.chat.id, text='Вы не передали ID админа и ID новой роли. Повторите.',
                     reply_markup=Markup.Exit.admins_edit_role_exit)
        bot.register_next_step_handler(message, edit_role_of_admins)
        return

    if message.text == 'Выход из режима изменения роли админа' or message.text == 'Отмена':
        send_message(message.chat.id, text='Отмена изменения роли админа', reply_markup=Markup.Main.show)
        return

    id_strings = message.text.split()

    if len(id_strings) != 2:
        send_message(message.chat.id, text='Нужно передать 2 числа. ID админа и ID новой роли. Повторите.',
                     reply_markup=Markup.Exit.admins_edit_role_exit)
        bot.register_next_step_handler(message, edit_role_of_admins)
        return

    ids = []
    for id_string in id_strings:
        if not id_string.isdigit():
            send_message(message.chat.id,
                         text='Нужно передать ID числами, а не словами. Повторите.'.format(sbor.get_people_count()),
                         reply_markup=Markup.Exit.admins_edit_role_exit)
            bot.register_next_step_handler(message, edit_role_of_admins)
            return
        id = int(id_string)
        ids.append(id)

    result, error = admins.edit_role_admin(ids[0], ids[1])
    if result:
        send_message(message.chat.id, text=admins.get_admin_info(admins.get_admin(ids[0])),
                     reply_markup=Markup.Main.show)
        send_message(message.chat.id, text='Информация сохранена!')
        admins.save()
    else:
        send_message(message.chat.id, text=error + ' Повторите.', reply_markup=Markup.Exit.admins_edit_role_exit)
        bot.register_next_step_handler(message, edit_role_of_admins)


def add_admin(message):
    if not message.text:
        send_message(message.chat.id, text='Вы не передали Telegram админа и ID его роли. Повторите.',
                     reply_markup=Markup.Exit.admins_add_exit)
        bot.register_next_step_handler(message, add_admin)
        return

    if message.text == 'Выход из режима добавления админа' or message.text == 'Отмена':
        send_message(message.chat.id, text='Отмена добавления админа', reply_markup=Markup.Main.show)
        return

    id_strings = message.text.split()

    if len(id_strings) != 2:
        send_message(message.chat.id, text='Нужно передать 2 значения. Telegram админа и ID его роли. Повторите.',
                     reply_markup=Markup.Exit.admins_add_exit)
        bot.register_next_step_handler(message, add_admin)
        return

    if not id_strings[1].isdigit():
        send_message(message.chat.id,
                     text='Нужно передать ID роли числом, а не словом. Повторите.'.format(sbor.get_people_count()),
                     reply_markup=Markup.Exit.admins_add_exit)
        bot.register_next_step_handler(message, add_admin)
        return

    result, error = admins.add_admin(id_strings[0], int(id_strings[1]))
    if result:
        send_message(message.chat.id, text=admins.get_admin_info(admins.get_admin(admins.get_admins_count())),
                     reply_markup=Markup.Main.show)
        send_message(message.chat.id, text='Информация сохранена!')
        admins.save()
    else:
        send_message(message.chat.id, text=error + ' Повторите.', reply_markup=Markup.Exit.admins_add_exit)
        bot.register_next_step_handler(message, add_admin)


def remove_admin(message):
    if not message.text:
        send_message(message.chat.id, text='Вы не передали ID админа. Повторите.',
                     reply_markup=Markup.Exit.admins_remove_exit)
        bot.register_next_step_handler(message, remove_admin)
        return

    if message.text == 'Выход из режима удаления админа' or message.text == 'Отмена':
        send_message(message.chat.id, text='Отмена удаления админа', reply_markup=Markup.Main.show)
        return

    id_strings = message.text.split()

    if len(id_strings) != 1:
        send_message(message.chat.id, text='Нужно передать 1 значение. ID админа. Повторите.')
        bot.register_next_step_handler(message, remove_admin)
        return

    if not id_strings[0].isdigit():
        send_message(message.chat.id,
                     text='Нужно передать ID админа числом, а не словом. Повторите.'.format(sbor.get_people_count()))
        bot.register_next_step_handler(message, remove_admin)
        return

    admin_id = int(id_strings[0])
    admin_telegram = admins.get_admin(admin_id).telegram
    result, error = admins.remove_admin(admin_id)
    if result:
        send_message(message.chat.id, text='Админ `{}` удален!'.format(admin_telegram), reply_markup=Markup.Main.show)
        admins.save()
    else:
        send_message(message.chat.id, text=error + ' Повторите.', reply_markup=Markup.Exit.admins_remove_exit)
        bot.register_next_step_handler(message, remove_admin)


def find_people(message):
    if not message.text:
        send_message(message.chat.id,
                     text='Вы не передали данные для поиска человека. Нужно передать имя и/или фамилию человека. Повторите.',
                     reply_markup=Markup.Exit.people_search_exit)
        bot.register_next_step_handler(message, find_people)
        return

    if message.text == 'Выход из режима поиска' or message.text == 'Отмена':
        send_message(message.chat.id, text='Поиск закончен', reply_markup=Markup.Main.show)
        return

    keys = message.text.split()
    if len(keys) > 2:
        send_message(message.chat.id,
                     text='Передано слишком много аргументов. Нужно передать только имя и/или фамилию человека. Повторите.')
        bot.register_next_step_handler(message, find_people)
        return

    for key in keys:
        if key.isdigit():
            if len(keys) == 1 and is_right_user(message.from_user, admins.get_users_who_can_see_ids()):
                break
            send_message(message.chat.id,
                         text='Вы передали числа. Нужно передать имя и/или фамилию человека. Повторите.')
            bot.register_next_step_handler(message, find_people)
            return

    people = sbor.find_people(keys)
    if not people:
        send_message(message.chat.id, text='Не найдено ни одного человека. Повторите.')
        bot.register_next_step_handler(message, find_people)
        return

    info = Person.Info.Debug if is_right_user(message.from_user,
                                              admins.get_users_who_can_see_ids()) else Person.Info.Full
    send_message(message.chat.id, text='Вот кого я нашел', reply_markup=Markup.Exit.people_search_exit)
    for person in people:
        send_message(message.chat.id, text=sbor.get_person_info(person, info))
    bot.register_next_step_handler(message, find_people)


def public_message(message):
    if not message.text and not message.photo:
        send_message(message.chat.id, text='Вы не передали текст для публикации. Повторите.',
                     reply_markup=Markup.Exit.public_message_exit)
        bot.register_next_step_handler(message, public_message)
        return

    if message.text == 'Выход из режима публикации сообщения' or message.text == 'Отмена':
        send_message(message.chat.id, text='Отмена публикации сообщения', reply_markup=Markup.Main.show)
        return

    message_with_photo = False
    if message.photo:
        message_with_photo = save_photo(message=message, path=Resources.Images.temporary)

    for user in users.get_users():
        if user == message.chat.id:
            continue
        elif message_with_photo:
            send_message(user, text=message.caption, photo_path=Resources.Images.temporary,
                         reply_markup=Markup.Main.show)
        else:
            send_message(user, text=message.text, reply_markup=Markup.Main.show)

    send_message(message.chat.id, text='Сообщение опубликовано!', reply_markup=Markup.Main.show)


bot.polling(none_stop=True)
