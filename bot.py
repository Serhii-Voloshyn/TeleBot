import telebot as tb
import config
import logging as log


#Logging to file debug messages
def debug(text):
    """
    Logging parameter 'text' to file debug.log
    """

    log.basicConfig(filename='debug.log', encoding='utf-8', level=log.DEBUG)
    log.debug(text)



#Create a bot
bot = tb.TeleBot(config.TOKEN)


#Do on start

@bot.message_handler(commands = ['start'])
def onStart(message):
    
    bot.send_message(message.chat.id, "Hello there :)")

#When message sent
@bot.message_handler(content_types = ['text'])
def parroting(message):

    bot.send_message(message.chat.id, message.text[::-1])



#Start bot activity
bot.polling(none_stop = True)