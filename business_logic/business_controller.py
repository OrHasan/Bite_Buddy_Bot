import logging

import bot_secrets
import telebot
from telebot import types
from api_manager import API_Manager



bot = telebot.TeleBot(bot_secrets.TOKEN)
api_manager=API_Manager()
user_state = {}



def show_menu(chat_id,message):
    markup = types.InlineKeyboardMarkup(row_width=2)  # row_width => how many buttons per row
    button1 = types.InlineKeyboardButton("Add_Food", callback_data="add_food")
    button2 = types.InlineKeyboardButton("Generate_Report", callback_data="view_stats")
    button3 = types.InlineKeyboardButton("Show_eaten_food", callback_data="help")
    markup.add(button1, button2, button3)
    bot.send_message(chat_id, message,
                     reply_markup=markup)

@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message):
    show_menu(message.chat.id,"Welcome to Bite Buddy, your nutrition tracker! Choose an option below:")


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: types.CallbackQuery):
    if call.data == "add_food":
        bot.send_message(call.message.chat.id, "please enter what you have eaten.")
        user_state[call.message.chat.id] = 'waiting_for_food_name'
    elif call.data == "Generate_Report":
        pass
    elif call.data == "Show_eaten_food":
        pass

@bot.message_handler(func=lambda message: message.chat.id in user_state and user_state[message.chat.id] == 'waiting_for_food_name')
def add_food(message: telebot.types.Message):
    try:
        result=api_manager.get_info_by_api(message.text)

        if result==None:

            bot.send_message(message.chat.id, "please enter a valid food")

        else:
            # Todo
            #save in the DB
            bot.reply_to(message, f"added food successfuly : {message.text}")
            user_state[message.chat.id] = None
            show_menu(message.chat.id,"Choose an option below:")
    except Exception:
        bot.send_message(message.chat.id, "please enter what you have eaten.")






@bot.message_handler(func=lambda m: True)
def echo_all(message: telebot.types.Message):

    bot.reply_to(message, f"You said: {message.text}")




bot.infinity_polling()

