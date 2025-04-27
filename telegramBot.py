import telebot
import databaseWork
from telebot import types

bot = telebot.TeleBot('key')
databaseWork.create_tables()
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button0 = types.KeyboardButton('Мои темы')
    button1 = types.KeyboardButton('Новая тема')
    button2 = types.KeyboardButton('Удалить тему')
    markup.add(button0)
    markup.add(button1)
    markup.add(button2)
    databaseWork.start(message)
    bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '!')
    bot.send_message(message.chat.id, 'Добро пожаловать в бот "Дневник записей"!', reply_markup=markup)
    bot.register_next_step_handler(message, OnClick)

def OnClick(message):
    
    if message.text == 'Мои темы':
        markup = types.ReplyKeyboardRemove()
        themesData = databaseWork.returnTheme(message)
        themesData = [x[0] for x in themesData]
        bot.send_message(message.chat.id, 'Выберете вашу тему:', reply_markup=markup)

        for i in range(0, len(themesData)):
            bot.send_message(message.chat.id, f'{i}: ' + str(themesData[i]))

        bot.register_next_step_handler(message, OnShowEntry, themesData)
    
    
    
    elif message.text == 'Новая тема':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message.from_user.first_name + ', напишите название темы', reply_markup=markup)
        bot.register_next_step_handler(message, OnCreateNewTheme)
    
    
    
    elif message.text == 'Удалить тему':
        markup = types.ReplyKeyboardRemove()
        bot.register_next_step_handler(message, DeleteTheme)
    


    

def OnShowEntry(message, themesData):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button0 = types.KeyboardButton('В главное меню')
    button1 = types.KeyboardButton('Добавить новую запись')
    markup.add(button0)
    markup.add(button1)
    themeIndex = int(message.text)
    entryData = databaseWork.returnEntry(message, str(themesData[themeIndex]))
    entryData = [x[0] for x in entryData]

    for i in range(0, len(entryData)):
            bot.send_message(message.chat.id, str(entryData[i]), reply_markup=markup)

    bot.register_next_step_handler(message, ShowEntryNextStep, themesData[themeIndex])

def ShowEntryNextStep(message, themeName):
    if message.text == 'В главное меню':
        start(message)
    elif message.text == 'Добавить новую запись':
        bot.send_message(message.chat.id, 'Тема: ' + themeName + '. Добавьте новую заметку или задачу.')
        bot.register_next_step_handler(message, OnCreateNewEntry, themeName)

def OnCreateNewTheme(message):
    databaseWork.saveTheme(message)
    themeName = message.text
    bot.send_message(message.chat.id, 'Ваша тема ' + themeName + ' записана. Добавьте первые заметки или задачи.')
    bot.register_next_step_handler(message, OnCreateNewEntry, themeName)

def OnCreateNewEntry(message, themeName):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button0 = types.KeyboardButton('Мои темы')
    button1 = types.KeyboardButton('Новая тема')
    markup.add(button0)
    markup.add(button1)
    databaseWork.saveEntry(message, themeName)
    bot.send_message(message.chat.id, 'Запись добавлена', reply_markup=markup)
    bot.register_next_step_handler(message, OnClick)



def DeleteTheme(message):
    # Убираем клавиатуру
    markup = types.ReplyKeyboardRemove()
    
    # Получаем все темы пользователя
    themesData = databaseWork.returnTheme(message)
    themesData = [x[0] for x in themesData]

    if not themesData:
        bot.send_message(message.chat.id, "У тебя нет тем для удаления.", reply_markup=markup)
        start(message)
        return

    # Показываем список тем с индексами
    bot.send_message(message.chat.id, 'Выбери тему для удаления (напиши номер):', reply_markup=markup)
    for i in range(len(themesData)):
        bot.send_message(message.chat.id, f'{i}: {themesData[i]}')

    # Переходим к следующему шагу
    bot.register_next_step_handler(message, ConfirmDeleteTheme, themesData)

def ConfirmDeleteTheme(message, themesData):
    try:
        themeIndex = int(message.text)
        themeName = themesData[themeIndex]
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Некорректный ввод. Попробуй снова.")
        start(message)
        return

    # Удаляем тему из базы данных
    databaseWork.deleteTheme(message, themeName)
    bot.send_message(message.chat.id, f"Тема '{themeName}' удалена.")

    # Возвращаем в главное меню
    start(message)





bot.polling(non_stop=True)