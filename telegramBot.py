import telebot
import databaseWork
from telebot import types

bot = telebot.TeleBot('7780379541:AAGtgyw4cJerCiXO36HhL8TUllD6oHdhyFI')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button0 = types.KeyboardButton('Мои темы')
    button1 = types.KeyboardButton('Добавить тему')
    markup.add(button0)
    markup.add(button1)
    databaseWork.start(message)
    bot.send_message(message.chat.id, 'Привет!', reply_markup=markup)
    bot.register_next_step_handler(message, OnClick)

def OnClick(message):
    if message.text == 'Мои темы':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button0 = types.KeyboardButton('Личная тема')
        button1 = types.KeyboardButton('Общая тема')
        markup.add(button0)
        markup.add(button1)
        bot.send_message(message.chat.id, message.from_user.id, reply_markup=markup)
    elif message.text == 'Добавить тему':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button0 = types.KeyboardButton('Личная тема')
        button1 = types.KeyboardButton('Общая тема')
        markup.add(button0)
        markup.add(button1)
        bot.send_message(message.chat.id, message.from_user.id, reply_markup=markup)

bot.polling(non_stop=True)