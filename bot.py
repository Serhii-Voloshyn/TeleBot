import telebot as tb
import config
from bs4 import BeautifulSoup

from pretty_print import pretty_schedule_for_group
from lesson import Lesson



def send_schedule(message, group):
    bot.send_message(message.chat.id, "Ось твій розклад на тиждень, хорошого дня")
    for i in pretty_schedule_for_group(group):
        bot.send_message(message.chat.id, text = i, parse_mode = 'HTML')

def is_valid_group(group):
    """
    Return True, if group is in groups.html
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

    #If impossible to open file
    return False

#Create a bot
bot = tb.TeleBot(config.TOKEN)


#Do on start
@bot.message_handler(commands = ['start'])
def onStart(message):
    bot.send_message(message.chat.id, "Привіт\nЯ студ криса :)")

    if(config.group_current != ''):
        bot.send_message(message.chat.id, "Ось твій розклад на тиждень, хорошого дня")
        send_schedule(message, config.group_current)
        print('Done 1')

    else:
        bot.send_message(message.chat.id, "Відправ мені назву групи(Наприклад ІП-11) і я скину тобі розклад")
        print('Done 2')



#When message sent
@bot.message_handler(content_types = ['text'])
def processing(message):

    if(config.group_current == ''):
        if(is_valid_group(message.text)):

            config.group_current = message.text
            
            send_schedule(message, config.group_current)

        else:
            bot.send_message(message.chat.id, text = 'Сорі, братішка, такої групи немає в базі')

    else:
        send_schedule(message, config.group_current)
        




#Start bot activity
bot.polling(none_stop = True)