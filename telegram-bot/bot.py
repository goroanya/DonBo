from datetime import date, timedelta, datetime
import datetime as dt

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

schedule_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
schedule_markup.row('Меню')
schedule_markup.row('Записатись на прийом')
schedule_markup.row('Переглянути вільні місця на найближчі 7 днів')
schedule_markup.row('Переглянути вільні місця певного дня')


@bot.message_handler(
    func=lambda message: message.text == '/start' or message.text == 'Меню')
def start(message):
    bot.set_data({'master': None}, message.chat.id)
    bot.send_message(message.chat.id, "Оберіть опцію", reply_markup=choose_markup)


@bot.message_handler(func=lambda message: message.text == 'Заповнити/Змінити інформацію про себе')
def fill_information_about_user(message):
    bot.send_message(message.chat.id, "Як Вас звати?")
    bot.set_state('expect_user_name', message.chat.id)


@bot.message_handler(state='expect_user_name')
def on_user_name_begin(message):
    bot.set_data({'user_name': message.text}, message.chat.id)
    data = storage.get_data(message.chat.id)

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row('Пропустити')

    bot.send_message(message.chat.id, "Ваш email (необов'язково)", reply_markup=markup)

    bot.set_state('expect_user_email', message.chat.id)


@bot.message_handler(state='expect_user_email')
def on_user_email_begin(message):
    bot.update_data({'user_email': message.text if message.text != 'Пропустити' else None}, message.chat.id)

    bot.send_message(message.chat.id, 'Ваш номер телефону (допустимі символи-цифри)')
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
    bot.send_message(message.chat.id, "Інформацію успішно запам'ятовано/змінено!", reply_markup=choose_markup)


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

    master_id = message.text
    master = session.query(Master).get(master_id)

    if master is None:
        bot.send_message(message.chat.id, 'Фахівця з таким ідентифікатором не знайдено.Спробуйте ще раз.')
    else:
        master_info = f"Інформація про знайденого фахівця:" + \
                      f"\nІм'я: {master.name}" + \
                      f"\nНомер телефону: {master.phone_number}" + \
                      f"\nПошта: {master.email if master.email is not None else ''}" + \
                      f"\nГРАФІК РОБОТИ:" + \
                      f"\nГодини роботи: {master.start_work_time}-{master.end_work_time}" + \
                      f"\nРобочі дні: {', '.join(master.days)}"

        bot.send_message(message.chat.id, master_info)

        bot.update_data({'master': master}, message.chat.id)
        bot.set_state(None, message.chat.id)

        bot.send_message(message.chat.id, "Бажаєте переглянути розклад цього фахівця?", reply_markup=schedule_markup)


@bot.message_handler(func=lambda message: 'Переглянути вільні місця на найближчі 7 днів' in message.text)
def show_7_days_schedule(message):
    master = check_is_master_data_present(message.chat.id)
    if master:
        send_free_appointments(message.chat.id, master, next_7_days_=True)


@bot.message_handler(func=lambda message: 'Переглянути вільні місця певного дня' in message.text)
def show_day_of_schedule(message):
    if check_is_master_data_present(message.chat.id):
        bot.send_message(message.chat.id, 'Введіть дату у форматі [дд.мм.рр]')
        bot.set_state('expect_date_of_appointment', message.chat.id)


@bot.message_handler(state='expect_date_of_appointment')
def on_date_of_schedule_begin(message):
    data = storage.get_data(message.chat.id)

    try:
        appointment_date = datetime.strptime(message.text, '%d.%m.%y').date()

        send_free_appointments(message.chat.id, data['master'], appointment_date=appointment_date)
    except ValueError:
        bot.send_message(message.chat.id, 'Некоректна введена дата. Спробуйте ще раз у форматі [дд.мм.рр]')
        bot.set_state('expect_date_of_appointment', message.chat.id)
        return


def send_free_appointments(chat_id, master, appointment_date=None, next_7_days_=None):
    start_time = master.start_work_time
    end_time = master.end_work_time
    appointment_duration = master.appointment_duration_minutes
    work_days = master.days

    td = datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)
    working_time = td.seconds // 60
    number_of_appointments = working_time // appointment_duration

    starts = [add_minutes_to_time(start_time, i * appointment_duration)
              for i in range(number_of_appointments)]

    if next_7_days_:
        info = f"Вільні місця:\n"
        bot.send_message(chat_id, info)

        appointments = session.query(Appointment).filter(Appointment.master_id == master.id) \
            .filter(Appointment.date >= date.today()) \
            .filter(Appointment.date <= date.today() + timedelta(days=7))

        dates = [date.today() + timedelta(days=i)
                 for i in range(8)]

        for cur_date in dates:
            if cur_date.strftime("%A") in work_days:
                info = f'\n{cur_date.strftime("%d.%m.%Y (%A)")}\n'

                for cur_time in starts:
                    cur_apps = appointments.filter(Appointment.date == cur_date) \
                        .filter(Appointment.start_time == cur_time)
                    if not len(list(cur_apps)):
                        info += f'{cur_time.strftime("%H:%M")}-' + \
                                f'{(add_minutes_to_time(cur_time, appointment_duration)).strftime("%H:%M")}\n'

                bot.send_message(chat_id, info, reply_markup=schedule_markup)
    else:
        appointments = session.query(Appointment).filter(Appointment.master_id == master.id) \
            .filter(Appointment.date == appointment_date)
        if appointment_date < date.today():
            bot.send_message(chat_id, "Дата неактуальна", reply_markup=schedule_markup)
            return
        elif appointment_date.strftime("%A") not in work_days:
            bot.send_message(chat_id, "Цього дня майстер не працює", reply_markup=schedule_markup)
            return
        else:
            bot.send_message(chat_id, "Вільні місця:\n")
            info = f'\n{appointment_date.strftime("%d.%m.%Y (%A)")}\n'
            for cur_time in starts:
                cur_apps = appointments.filter(Appointment.date == appointment_date) \
                    .filter(Appointment.start_time == cur_time)
                if not len(list(cur_apps)):
                    info += f'{cur_time.strftime("%H:%M")}-' + \
                            f'{(add_minutes_to_time(cur_time, appointment_duration)).strftime("%H:%M")}\n'
            bot.send_message(chat_id, info, reply_markup=schedule_markup)


def check_is_master_data_present(chat_id):
    data = storage.get_data(chat_id)
    if not data['master']:
        bot.send_message(chat_id, 'Введіть ідентифікатор майстра')
        bot.set_state('expect_master_id', chat_id)
        return None
    else:
        return data['master']


def fill_user_info(chat_id):
    data = storage.get_data(chat_id)

    new_info = f"Ваше ім'я: {data['user_name']}\n" + \
               f"Ваш номер телефону: {data['user_phone_number']}\n" + \
               f"Ваш email: {'Відсутній' if data['user_email'] is None else data['user_email']}"

    client_from_db = session.query(Client).get(chat_id)

    if client_from_db is None:
        client = Client(chat_id, data['user_name'], data['user_phone_number'], data['user_email'])
        session.add(client)
    else:
        client_from_db.name = data['user_name']
        client_from_db.phone_number = data['user_phone_number']
        client_from_db.email = data['user_email']

        session.commit()

    return new_info


def add_minutes_to_time(t, minutes):
    now = dt.datetime.now()
    delta = dt.timedelta(minutes=minutes)
    return (dt.datetime.combine(dt.date(1, 1, 1), t) + delta).time()


bot.polling()
