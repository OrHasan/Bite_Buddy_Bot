import logging
from xmlrpc.client import DateTime

from pyexpat.errors import messages

import bot_secrets
import telebot

from datetime import datetime
from telebot import types
from DAO.dao_controller import DaoController
from business_logic.Report_Controller import Report_Controller
from business_logic.api_manager import API_Manager



bot = telebot.TeleBot(bot_secrets.TOKEN)
user_states = {}
api_manager=API_Manager()
dao = DaoController()
user_state = {}
report_controller=Report_Controller()

def show_reports_categroy(chat_id, message):
    markup = types.InlineKeyboardMarkup(row_width=2)  # row_width => how many buttons per row
    button1 = types.InlineKeyboardButton("daily report", callback_data="report_by_date")
    button2 = types.InlineKeyboardButton("report by categroy", callback_data="reportr_by_categroy")
    markup.add(button1, button2)
    bot.send_message(chat_id, message,
                     reply_markup=markup)

def show_reports_nutritions(chat_id, message):
    markup = types.InlineKeyboardMarkup(row_width=3)  # row_width => how many buttons per row
    button1 = types.InlineKeyboardButton("fat", callback_data="fat")
    button2 = types.InlineKeyboardButton("cholesterol", callback_data="cholesterol")
    button3 = types.InlineKeyboardButton("carbohydrate", callback_data="carbohydrate")
    button4 = types.InlineKeyboardButton("protein", callback_data="protein")
    button5 = types.InlineKeyboardButton("sodium", callback_data="sodium")
    button6 = types.InlineKeyboardButton("potassium", callback_data="potassium")


    markup.add(button1, button2,button3,button4,button5,button6)
    bot.send_message(chat_id, message,
                     reply_markup=markup)

def show_menu(chat_id,message):
    markup = types.InlineKeyboardMarkup(row_width=2)  # row_width => how many buttons per row
    button1 = types.InlineKeyboardButton("Add_Food", callback_data="add_food")
    button2 = types.InlineKeyboardButton("Generate_Report", callback_data="generate_report")
    button3 = types.InlineKeyboardButton("Show_eaten_food", callback_data="Show_eaten_food")
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
    elif call.data == "generate_report":
        show_reports_categroy(call.message.chat.id, "click on the desired report")


    elif call.data == "Show_eaten_food":
        bot.send_message(call.message.chat.id, "please enter the date to see food eaten in that date")
        user_state[call.message.chat.id] = 'show_food_per_date'

    elif call.data == "report_by_date":
        bot.send_message(call.message.chat.id, "please enter date, in this format dd.mm.yy etc: 03.03.25")
        user_state[call.message.chat.id] = 'waiting_for_date'
    elif call.data == "reportr_by_categroy":
        show_reports_nutritions(call.message.chat.id, "click on the desired nutrition")
    elif call.data == "fat" or call.data == "cholesterol" or call.data == "carbohydrate" or call.data == "protein" or call.data == "sodium" or call.data == "potassium":
        bot.send_message(call.message.chat.id, "please enter date, in this format dd.mm.yy etc: 03.03.25")
        user_state[call.message.chat.id] = 'waiting_for_date_for_category_'+call.data



@bot.message_handler(func=lambda message: message.chat.id in user_state and user_state[message.chat.id] == 'waiting_for_food_name')
def add_food(message: telebot.types.Message):
    try:
        result=api_manager.get_info_by_api(message.text)

        if result==None:
            bot.send_message(message.chat.id, "please enter a valid food")
        else:
            dao.add_food(food_name=message.text,food_item= result, user_id=message.from_user.id, date=datetime.now())
            bot.send_message(message.chat.id, f"added food successfully : {message.text}")
            user_state[message.chat.id] = None
            show_menu(message.chat.id,"Choose an option below:")
    except Exception:
        bot.send_message(message.chat.id, "please enter what you have eaten.")


@bot.message_handler(func=lambda message: message.chat.id in user_state and user_state[message.chat.id] == 'show_food_per_date')
def fetch_eaten_food_info(message):
    """Step 2: Retrieve food information from the database."""
    date = message.text

    food_info = dao.get_foods_by_user_and_date(message.chat.id, date)

    if food_info:
        response = f"🍏 Food: {food_info['name']}\n📌 Category: {food_info['category']}\n🔥 Calories: {food_info['calories']} kcal"
    else:
        response = "⚠️ Food not found in the database."

    bot.reply_to(message, response)
    user_states.pop(message.chat.id, None)



@bot.message_handler(func=lambda message: message.chat.id in user_state and user_state[message.chat.id] == 'waiting_for_date')
def generate_report_by_date(message: telebot.types.Message):
    try:
        datetime.strptime(message.text, "%d.%m.%y") #checks if the date is in the correct format
        user_history_db = dao.get_foods_by_user_and_date(message.from_user.id, message)
        report = report_controller.generate_report_by_date(message, user_history_db)
        if not report:
            bot.send_message(message.chat.id, "there is no data for the given date.")
        else:
            bot.send_message(message.chat.id, report)

    except ValueError:
        bot.reply_to(message, "the given date is in a wrong format, please enter in this format : dd.mm.yy")

    finally:
        user_state[message.chat.id] = None
        show_menu(message.chat.id, "Choose an option below:")


@bot.message_handler(func=lambda message: message.chat.id in user_state and user_state[message.chat.id] and user_state[message.chat.id].find('waiting_for_date_for_category')!=-1 )
def generate_report_by_category(message: telebot.types.Message):
    try:
        nutrition = user_state[message.chat.id].split('_')[-1]
        datetime.strptime(message.text, "%d.%m.%y")  # checks if the date is in the correct format
        user_history_db = dao.get_foods_by_user_and_date(message.from_user.id, message)
        report = report_controller.generate_report_by_category(message, user_history_db,nutrition)
        if not report:
            bot.send_message(message.chat.id, "there is no data for the given date.")
        else:
            bot.send_message(message.chat.id, report)

    except ValueError:
        bot.reply_to(message, "the given date is in a wrong format, please enter in this format : dd.mm.yy")

    finally:
        user_state[message.chat.id] = None
        show_menu(message.chat.id, "Choose an option below:")




bot.infinity_polling()

