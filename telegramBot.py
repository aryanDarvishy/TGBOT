import telebot
import databaseWork
from telebot import types

<<<<<<< Updated upstream
bot = telebot.TeleBot('key')
=======
bot = telebot.TeleBot('7780379541:AAHjpvmXg4-VDoENfEk6jvolXSaw5tM58Ao')
>>>>>>> Stashed changes

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button0 = types.KeyboardButton('Мои темы')
    button1 = types.KeyboardButton('Новая тема')
    markup.add(button0)
    markup.add(button1)
    databaseWork.start(message)
    bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '!')
    bot.send_message(message.chat.id, 'Добро пожаловать в бот "Дневник записей"!', reply_markup=markup)
    bot.register_next_step_handler(message, OnClick)

def OnClick(message):
    if message.text == 'Мои темы':
        bot.send_message(message.chat.id, 'тут короче эээ лан иди нахуй' )
    elif message.text == 'Новая тема':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message.from_user.first_name + ', напишите название темы', reply_markup=markup)
        bot.register_next_step_handler(message, OnCreateNewTheme)

def OnCreateNewTheme(message):
    databaseWork.saveTheme(message)
    bot.send_message(message.chat.id, 'Ваша тема ' + message.text + ' записана. Добавьте первые заметки или задачи.')
    bot.register_next_step_handler(message, OnCreateNewEntry)

def OnCreateNewEntry(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button0 = types.KeyboardButton('Мои темы')
    button1 = types.KeyboardButton('Новая тема')
    markup.add(button0)
    markup.add(button1)
    bot.send_message(message.chat.id, 'Запись добавлена', reply_markup=markup)
    bot.register_next_step_handler(message, OnClick)

bot.polling(non_stop=True)
