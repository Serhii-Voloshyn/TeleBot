import telebot as tb
from telebot.apihelper import delete_message
import config
from bs4 import BeautifulSoup

from converter import get_ScheduleDays_by_group
from exam_converter import get_exams_by_group

from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton


#Create a bot
bot = tb.TeleBot(config.TOKEN)

#Define reply keyboard and inline keyboard for schedule message
keyboard = ReplyKeyboardMarkup(True)
keyboard.row('Розклад занять', 'Розклад екзаменів')
keyboard.add('Змінити групу')

#Keyboard for schedule message, needed to navigate
keyboard_schedule = InlineKeyboardMarkup()
keyboard_schedule.row(
    InlineKeyboardButton(text = 'Пн', callback_data = 'Mon_schedule'),
    InlineKeyboardButton(text = 'Вт', callback_data = 'Tue_schedule'),
    InlineKeyboardButton(text = 'Ср', callback_data = 'Wen_schedule'),
    InlineKeyboardButton(text = 'Чт', callback_data = 'Thu_schedule'),
    InlineKeyboardButton(text = 'Пт', callback_data = 'Fri_schedule'))


def form_exam_text(exams):
    """Forms exam, needed to send it to user. Returns string
    exams - list of Exam"""
    text = ''
    for i in exams:
        text += '\n-------'
        text += str(i)

    return text


def get_day_index(day_name, schedule_week):
    """Find index of that day, returns index in schedule_week
    day_name - string, name of a day
    schedule week - list of ScheduleDay obj"""
    #Needed when days aren't in their place. 
    #Example, first element in schedule_week has day_name = Tuesday
    return [i.get_day_name() for i in schedule_week].index(day_name)


def send_schedule_day(call, day_name, schedule_week):
    """Make bot send schedule to user, when user press button
    call - callback from bot massage
    day_name - string, name of specific day
    schedule week - list of ScheduleDay objects"""
    #If requested day_name has no lessons (list of ScheduleDay object don't contain this day)
    if day_name not in [i.get_day_name() for i in schedule_week]:
        #Edit message
        bot.edit_message_text(
            chat_id = call.message.chat.id, 
            message_id = call.message.message_id, 
            text = 'Вітаю, у вас вікно!', 
            parse_mode = 'HTML', 
            reply_markup = keyboard_schedule)
    #If day_name in schedule_week
    else:
        
        day_index = get_day_index(day_name, schedule_week)

        bot.edit_message_text(
            chat_id = call.message.chat.id, 
            message_id = call.message.message_id, 
            text = str(schedule_week[day_index]), 
            parse_mode = 'HTML', 
            reply_markup = keyboard_schedule)


def send_exams(message):
    """Make bot send exams to user, when user press button
    call - callback from bot massage
    day_name - string, name of specific day
    schedule week - list of ScheduleDay objects"""
    #Create list of Exam obj
    exams = get_exams_by_group(config.group_current)

    bot.send_message(
        message.chat.id, 
        "Ось твій розклад екзаменів, хорошого дня", 
        reply_markup = keyboard)
    
    text = form_exam_text(exams)
    
    bot.send_message(
        message.chat.id, 
        text = text,
        parse_mode = 'HTML', 
        reply_markup = keyboard)


def send_schedule(message):
    """Sends schedule first time, after user pressed 'Розклад занять'"""
    schedule_week = get_ScheduleDays_by_group(config.group_current)

    bot.send_message(
        message.chat.id, 
        "Ось твій розклад на тиждень, хорошого дня", 
        reply_markup = keyboard)
    bot.send_message(
        message.chat.id, 
        text = str(schedule_week[0]), 
        parse_mode = 'HTML', 
        reply_markup = keyboard_schedule)

def change_group(message):
    """Edit group_current in config.py"""
    #Make it eq to ''
    #If group_current = '', next message is always a group name
    config.group_current = ''
    bot.send_message(message.chat.id, "Відправ мені назву групи(Наприклад ІТ-11)")

def set_group(message, group):
    """Change group_current in config.py
    group - string, grop name like 'CA-11'"""

    #If group exists in groups.html
    if is_valid_group(group):
            config.group_current = group
            bot.send_message(message.chat.id, text = 'Тепер ти належиш групі ' + group, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, text = 'Сорі, братішка, такої групи немає в базі', reply_markup=keyboard)


def is_valid_group(group):
    """Return True, if group is in groups.html
    group - string, like CA-11
    """
    #Take group list from local file. It's easier to save these groups as html, not list like
    with open('local\\groups.html', 'r', encoding = 'utf-8') as groups:
        content = groups.read()
        soup = BeautifulSoup(content, 'lxml')

        tag = soup.find('option', value = group)
        
        if(tag == None):
            return False
        else:
            return True


#Do on start
@bot.message_handler(commands = ['start'])
def onStart(message):
    bot.send_message(message.chat.id, "Привіт\nЯ студ криса :)")

    if(config.group_current == ''):
        bot.send_message(message.chat.id, "Відправ мені назву групи(Наприклад ІТ-11) і я скину тобі розклад")


#When message sent
@bot.message_handler(content_types = ['text'])
def processing(message):
    """Handle user simple messages"""

    #If group not defined in config.py
    #All messages will stop here, till user define group
    if config.group_current == '':
        set_group(message, message.text)
    
    if message.text == 'Розклад занять':
        send_schedule(message)
    elif message.text == 'Розклад екзаменів':
        send_exams(message)
    elif message.text == 'Змінити групу':
        change_group(message)
    else:
        bot.send_message(message.chat.id, "Ти биканув?")


@bot.callback_query_handler(func=lambda call: True)
def shedule_calls(call):
    """Callback handler from buttons in Schedule message"""
    schedule_week = get_ScheduleDays_by_group(config.group_current)
    if call.data == "Mon_schedule":
        send_schedule_day(call, 'Пн', schedule_week)
    elif call.data == "Tue_schedule":
        send_schedule_day(call, 'Вт', schedule_week)
    elif call.data == "Wen_schedule":
        send_schedule_day(call, 'Ср', schedule_week)
    elif call.data == "Thu_schedule":
        send_schedule_day(call, 'Чт', schedule_week)
    elif call.data == "Fri_schedule":
        send_schedule_day(call, 'Пт', schedule_week)


#Start bot activity
bot.polling(none_stop = True)