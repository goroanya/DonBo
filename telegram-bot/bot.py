import fsm_telebot
from fsm_telebot.storage.memory import MemoryStorage
from telebot import types
import re

from model import Appointment, Master, Client, session

TOKEN = '1018240929:AAHvM9gt11JBDlK3KInbkqfIubXLVNKV-dY'

storage = MemoryStorage()
bot = fsm_telebot.TeleBot(TOKEN, storage=storage)

choose_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
choose_markup.row('Знайти фахівця')
choose_markup.row('Заповнити/Змінити інформацію про себе')
choose_markup.row('Показати мої записи')
choose_markup.row('Відмінити запис')

menu_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_markup.row('Меню')


@bot.message_handler(func=lambda message: message.text == '/start' or message.text == 'Меню')
def start(message):
    bot.send_message(message.chat.id, "Оберіть опцію:", reply_markup=choose_markup)


@bot.message_handler(func=lambda message: message.text == 'Заповнити/Змінити інформацію про себе')
def fill_information_about_user(message):
    bot.send_message(message.chat.id, "Як Вас звати?")
    bot.set_state('expect_user_name', message.chat.id)


@bot.message_handler(state='expect_user_name')
def on_user_name_begin(message):
    bot.set_data({'user_name': message.text}, message.chat.id)

    bot.send_message(message.chat.id, 'Ваш email')
    bot.set_state('expect_user_email', message.chat.id)


@bot.message_handler(state='expect_user_email')
def on_user_email_begin(message):
    bot.update_data({'user_email': message.text}, message.chat.id)

    bot.send_message(message.chat.id, 'Ваш номер телефону')
    bot.set_state('expect_user_phone_number', message.chat.id)


@bot.message_handler(state='expect_user_phone_number')
def on_user_phone_number_begin(message):
    reg = re.match("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})",
                   message.text)
    if not reg:
        bot.send_message(message.chat.id, 'Некоректний номер телефону. Спробуйте ще раз')
        bot.set_state('expect_user_phone_number', message.chat.id)
        return

    bot.update_data({'user_phone_number': message.text}, message.chat.id)
    bot.send_message(message.chat.id, fill_user_info(message.chat.id))


@bot.message_handler(func=lambda message: message.text == 'Знайти фахівця')
def find_master(message):
    bot.send_message(message.chat.id, "Введіть ідентифікатор фахівця, якого бажаєте знайти")
    bot.set_state('expect_master_id', message.chat.id)


@bot.message_handler(state='expect_master_id')
def on_master_id_begin(message):
    try:
        int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Невірний формат ідентифікатора. Спробуйте ще раз.')
        return

    master = session.query(Master).get(message.text)

    if master is None:
        bot.send_message(message.chat.id, 'Фахівця з таким ідентифікатором не знайдено')
    else:
        master_info = f"Інформація про знайденого фахівця:" + \
                      f"\nІм'я: {master.name}" + \
                      f"\nНомер телефону: {master.phone_number}" + \
                      f"\nПошта: {master.email if master.email is not None else ''}" + \
                      f"\nГРАФІК РОБОТИ:" + \
                      f"\nГодини роботи: {master.start_work_time}-{master.end_work_time}" + \
                      f"\nРобочі дні: {', '.join(master.days)}"

        bot.send_message(message.chat.id, master_info)
        bot.send_message(message.chat.id, "Бажаєте переглянути розклад цього фахівця?")
        bot.set_state('show_master_schedule', message.chat.id)


def fill_user_info(chat_id):
    data = storage.get_data(chat_id)
    new_info = f"Ваше ім'я: {data['user_name']}\n" + \
               f"Ваш номер телефону: {data['user_phone_number']}\n" + \
               f"Ваш email: {data['user_phone_number']}"

    client_from_db = session.query(Client).get(chat_id)

    if client_from_db is None:
        client = Client(chat_id, data['user_name'], data['user_phone_number'], data['user_phone_number'])
        session.add(client)
    else:
        client_from_db.update({'name': data['user_name'],
                               'phone_number': data['user_phone_number'],
                               'email': data['user_phone_number']})
    session.commit()

    return new_info


bot.polling()
