# coding: utf8

import telebot
from telebot import types
import sys
import re
import db

API_TOKEN = '904381993:AAEAVFwFVvIO1BwCGYFUes7lCH_h5w_B1z4'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am bank_searching_bot.\n
I can help you to find nearest bank branch/ATM/currency exchange \n
If you are reading this message in group chat,
please write any message in private 
https://t.me/bank_searching_bot \n
run /help to know my commands
""")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, """\
here are my commands:
/start - info about me
/help - my commands
/search - look for nearest bank branch/ATM/currency exchange
""")

###############################################################################

@bot.message_handler(commands=['search'])
def main_func(message):
    if message.from_user.id == message.chat.id:
    
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_bank = types.KeyboardButton(text="bank")
        keyboard.add(button_bank)

        button_atm = types.KeyboardButton(text="atm")
        keyboard.add(button_atm)

        button_currency_exchange = types.KeyboardButton(text="currency exchange")
        keyboard.add(button_currency_exchange)

        msg = bot.send_message(message.chat.id, "choose one you want bot to look for", reply_markup=keyboard)

        bot.register_next_step_handler(msg, step2) 
        

    else:
          bot.reply_to(message, "please, write me this in private messages")



def step2(message):

    global mode
    mode = message.text

    keyboard2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="send my location", request_location=True)
    keyboard2.add(button_geo)
    bot.send_message(message.chat.id, "push the button to send location", reply_markup=keyboard2)


###############################################################################

@bot.message_handler(content_types=['location'])
def handle_location(message):
    bot.reply_to(message, str(message.location.latitude) + "  " + str(message.location.longitude))
    print(mode)
    db.read(mode)



###############################################################################


try:
    bot.polling()
except Exception:
    print(sys.exc_info())

