import telebot
from telebot import types

import settings
from data import (get_sections, get_subsections, get_exhibits,
                  get_halls_by_section, get_halls_by_subsection,
                  get_exhibit_info)

bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)
data = {}

def get_id_by_title(list, title):
    for item in list:
        if str(item[1]) == str(title):
            return item[0]
    return -1

@bot.message_handler(commands=['start'])
def start(message):
    data['sections'] = get_sections()
    select_section(message)

def select_section(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in data['sections']:
        btn = types.KeyboardButton(item[1])
        markup.add(btn)
    bot.send_message(message.chat.id,
                     text='Выберите раздел из списка:',
                     reply_markup=markup)
    bot.register_next_step_handler(message, get_subsection)

def get_subsection(message: telebot.types.Message):
    section_name = message.text
    section_id = get_id_by_title(data['sections'], section_name)
    if section_id == -1:
        bot.send_message(message.chat.id,
                         'Некорректный выбор раздела. Попробуйте еще раз.')
        return select_section(message)
    data['subsections'] = get_subsections(section_id)
    if data['subsections']:
        select_subsection(message)
    else:
        data['halls'] = get_halls_by_section(section_id)
        select_halls(message)

def select_subsection(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in data['subsections']:
        markup.add(types.KeyboardButton(item[1]))
    markup.add(types.KeyboardButton('<- Назад'))
    bot.send_message(message.chat.id,
                        text='Выберите подраздел из списка:',
                        reply_markup=markup)
    bot.register_next_step_handler(message, get_halls)

def get_halls(message: telebot.types.Message):
    subsection_name = message.text
    if subsection_name == '<- Назад':
        return select_section(message)
    subsection_id = get_id_by_title(data['subsections'], subsection_name)
    if subsection_id == -1:
        bot.send_message(message.chat.id,
                         'Некорректный выбор подраздела. Попробуйте еще раз.')
        return select_subsection(message)
    data['halls'] = get_halls_by_subsection(subsection_id)
    if data['halls']:
        select_halls(message)
    else:
        bot.send_message(message.chat.id, text='В данном разделе пока нет залов.')
        if data['subsections']:
            select_subsection(message)
        else:
            select_section(message)

def select_halls(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in data['halls']:
        markup.add(types.KeyboardButton(item[1]))
    markup.add(types.KeyboardButton('<- Назад'))
    bot.send_message(message.chat.id, 
                     text='Выберите зал из списка:',
                     reply_markup=markup)
    bot.register_next_step_handler(message, get_exhibits_list)

def get_exhibits_list(message: telebot.types.Message):
    hall_name = message.text
    if hall_name == '<- Назад':
        if data['subsections']:
            return select_subsection(message)
        else: 
            return select_section(message)
    hall_id = get_id_by_title(data['halls'], hall_name)
    if hall_id == -1:
        bot.send_message(message.chat.id,
                         'Некорректный выбор зала. Попробуйте еще раз.')
        return select_halls(message)
    data['exhibits'] = get_exhibits(hall_id)
    if data['exhibits']:
        select_exhibits(message)
    else:
        bot.send_message(message.chat.id, text='В данном зале пока нет экспонатов.')
        select_halls(message)

def select_exhibits(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in data['exhibits']:
        markup.add(types.KeyboardButton(item[1]))
    markup.add(types.KeyboardButton('<- Назад'))
    bot.send_message(message.chat.id,
                     text='Выберите номер экспоната из списка:',
                     reply_markup=markup)        
    bot.register_next_step_handler(message, show_exhibit_info)

def show_exhibit_info(message: telebot.types.Message):
    exhibit_number = message.text
    if exhibit_number == '<- Назад':
        return select_halls(message)
    exhibit_id = get_id_by_title(data['exhibits'], exhibit_number)
    if exhibit_id == -1:
        bot.send_message(message.chat.id,
                        'Некорректный выбор экспоната. Попробуйте еще раз.')
        return select_exhibits(message)
    exhibit = get_exhibit_info(exhibit_id)[0]
    exhibit_info = f'''
- *Номер эспоната в зале:* {exhibit[6]} \n
- *Название:* {exhibit[1]}\n
- *Год создания:* {exhibit[2]}\n
- *Описание:*\n{exhibit[3]}
    '''
    bot.send_message(message.chat.id,
                     text=exhibit_info,
                     parse_mode="Markdown")
    
    bot.send_message(message.chat.id,
                     text='''Выберите новый экспонат для просмотра, 
или воспользуйтесь кнопкой "<- Назад" для перехода в другой зал.
    ''')
    select_exhibits(message)

def main():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()