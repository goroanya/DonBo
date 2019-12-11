import fsm_telebot
from fsm_telebot.storage.memory import MemoryStorage
from telebot import types

TOKEN = '1018240929:AAHvM9gt11JBDlK3KInbkqfIubXLVNKV-dY'

storage = MemoryStorage()
bot = fsm_telebot.TeleBot(TOKEN)

choose_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
choose_markup.row('Знайти фахівця')
choose_markup.row('Заповнити інформацію про себе')
choose_markup.row('Показати мої записи')
choose_markup.row('Відмінити запис')
menu_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_markup.row('Меню')


@bot.message_handler(func=lambda message: message.text == '/start' or message.text == 'Меню')
def start(message):
    bot.send_message(message.chat.id, "Оберіть опцію:", reply_markup=choose_markup)


@bot.message_handler(func=lambda message: message.text == 'Заповнити інформацію про себе')
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
    bot.set_data({'user_email': message.text}, message.chat.id)

    bot.send_message(message.chat.id, 'Ваш номер телефону')
    bot.set_state('expect_user_phone_number', message.chat.id)


@bot.message_handler(state='expect_user_phone_number')
def on_user_phone_number_begin(message):
    bot.set_data({'user_phone_number': message.text}, message.chat.id)



bot.polling()
