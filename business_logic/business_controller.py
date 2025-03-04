import logging
from collections import defaultdict

import bot_secrets
import telebot
from datetime import datetime
from telebot import types
from DAO.dao_controller import DaoController
from business_logic.Report_Controller import Report_Controller
from business_logic.api_manager import API_Manager


logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(bot_secrets.TOKEN)
api_manager=API_Manager()
dao = DaoController()
users_states = {}
users_selections = {}
report_controller=Report_Controller()


def show_reports_categroy(chat_id,username, message):
    logger.info(f"[showing report categories for user: {username!r}]")

    markup = types.InlineKeyboardMarkup(row_width=2)  # row_width => how many buttons per row
    button1 = types.InlineKeyboardButton("daily report", callback_data="report_by_date")
    button2 = types.InlineKeyboardButton("report by categroy", callback_data="reportr_by_categroy")
    markup.add(button1, button2)
    bot.send_message(chat_id, message,
                     reply_markup=markup)


def show_reports_nutritions(chat_id, username,message):
    logger.info(f"[showing nutritions for user: {username!r}]")
    markup = types.InlineKeyboardMarkup(row_width=3)
    button1 = types.InlineKeyboardButton("fat ❌", callback_data="fat")
    button2 = types.InlineKeyboardButton("cholesterol ❌", callback_data="cholesterol")
    button3 = types.InlineKeyboardButton("carbohydrate ❌", callback_data="carbohydrate")
    button4 = types.InlineKeyboardButton("protein ❌", callback_data="protein")
    button5 = types.InlineKeyboardButton("sodium ❌", callback_data="sodium")
    button6 = types.InlineKeyboardButton("potassium ❌", callback_data="potassium")
    done_button = types.InlineKeyboardButton("Done", callback_data="done_selecting_nutritions_for_report")
    markup.add(button1, button2, button3, button4, button5, button6, done_button)
    bot.send_message(chat_id, message, reply_markup=markup)



def show_menu(user_id,username,message):
    logger.info(f"[showing menu for user: {username!r}]")

    markup = types.InlineKeyboardMarkup(row_width=2)  # row_width => how many buttons per row
    button1 = types.InlineKeyboardButton("Add_Food", callback_data="add_food")
    button2 = types.InlineKeyboardButton("Generate_Report", callback_data="generate_report")
    markup.add(button1, button2)
    bot.send_message(user_id, message,
                     reply_markup=markup)


@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message):
    global users_states
    users_states=dao.get_user_states()

    show_menu(message.chat.id,message.chat.first_name,"Welcome to Bite Buddy, your nutrition tracker! Choose an option below:")


def update_buttons(call):
    markup = types.InlineKeyboardMarkup(row_width=3)

    button1 = types.InlineKeyboardButton(f"fat {'✅' if 'fat' in users_selections[call.message.chat.id] else '❌'}",
                                         callback_data="fat")
    button2 = types.InlineKeyboardButton(
        f"cholesterol {'✅' if 'cholesterol' in users_selections[call.message.chat.id] else '❌'}",
        callback_data="cholesterol")
    button3 = types.InlineKeyboardButton(
        f"carbohydrate {'✅' if 'carbohydrate' in users_selections[call.message.chat.id] else '❌'}",
        callback_data="carbohydrate")
    button4 = types.InlineKeyboardButton(
        f"protein {'✅' if 'protein' in users_selections[call.message.chat.id] else '❌'}", callback_data="protein")
    button5 = types.InlineKeyboardButton(
        f"sodium {'✅' if 'sodium' in users_selections[call.message.chat.id] else '❌'}", callback_data="sodium")
    button6 = types.InlineKeyboardButton(
        f"potassium {'✅' if 'potassium' in users_selections[call.message.chat.id] else '❌'}",
        callback_data="potassium")

    done_button = types.InlineKeyboardButton("Done", callback_data="done_selecting_nutritions_for_report")

    markup.add(button1, button2, button3, button4, button5, button6, done_button)
    return markup


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: types.CallbackQuery):
    if call.data == "add_food":
        bot.send_message(call.message.chat.id, "please enter what you have eaten.")
        users_states[call.message.chat.id] = 'waiting_for_food_name'
        dao.save_users_state(users_states)
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: add_food.]")
    elif call.data == "generate_report":
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: generate_report.]")
        show_reports_categroy(call.message.chat.id,call.message.chat.first_name, "click on the desired report")

    elif call.data == "report_by_date":
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: report_by_date.]")
        bot.send_message(call.message.chat.id, "please enter date, in this format dd.mm.yy etc: 03.03.25")
        users_states[call.message.chat.id] = 'waiting_for_date'
        dao.save_users_state(users_states)
    elif call.data == "reportr_by_categroy":
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: reportr_by_categroy.]")
        show_reports_nutritions(call.message.chat.id,call.message.chat.first_name, "Please select the desired nutritions. Click 'Done' when finished.")
    elif call.data == "fat" or call.data == "cholesterol" or call.data == "carbohydrate" or call.data == "protein" or call.data == "sodium" or call.data == "potassium":
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: {call.data!r}]")
        if call.message.chat.id not in users_selections:
            users_selections[call.message.chat.id] = []
        # toggle the selection for the clicked category
        if call.data not in users_selections[call.message.chat.id]:
            users_selections[call.message.chat.id].append(call.data)
        else:
            users_selections[call.message.chat.id].remove(call.data)

        markup=update_buttons(call)


        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Please select the desired nutritions. Click 'Done' when finished.",
            reply_markup=markup
        )

    elif call.data == "done_selecting_nutritions_for_report":
        if call.message.chat.id not in users_selections or not users_selections[call.message.chat.id]:
            bot.send_message(call.message.chat.id, "No selection made, please select at least 1 nutrition")

        else:
            bot.send_message(call.message.chat.id, "please enter date, in this format dd.mm.yy etc: 03.03.25")
            users_states[call.message.chat.id] = 'waiting_for_date_for_category'
            dao.save_users_state(users_states)




@bot.message_handler(func=lambda message: message.chat.id in users_states and users_states[message.chat.id] == 'waiting_for_food_name')
def add_food(message: telebot.types.Message):
    try:
        result=api_manager.get_info_by_api(message.text)

        if result== {}:
            logger.warning(f"[user: {message.chat.first_name!r} entered invalid food]")
            bot.send_message(message.chat.id, "please enter a valid food")
        else:
            dao.add_food(food_name=message.text,food_item= result, user_id=message.from_user.id, date=datetime.now())
            bot.send_message(message.chat.id, f"added food successfully : {message.text}")
            users_states[message.chat.id] = None
            dao.save_users_state(users_states)
            show_menu(message.chat.id, message.chat.first_name, "Choose an option below:")
    except Exception:
        bot.send_message(message.chat.id, "an error occured during adding food.")



@bot.message_handler(func=lambda message: message.chat.id in users_states and users_states[message.chat.id] == 'waiting_for_date')
def generate_report_by_date(message: telebot.types.Message):
    try:
        datetime.strptime(message.text, "%d.%m.%y") #checks if the date is in the correct format
        user_history_db = dao.get_foods_by_user_and_date(message.from_user.id, message)
        report = report_controller.generate_report_by_date(message, user_history_db)
        if not report:
            bot.send_message(message.chat.id, "there is no data for the given date.")
        else:
            bot.send_message(message.chat.id, report)
        users_states[message.chat.id] = None
        dao.save_users_state(users_states)
        show_menu(message.chat.id, message.chat.first_name, "Choose an option below:")

    except ValueError:
        logger.warning(f"[user: {message.chat.first_name!r} entered wrong date format]")
        bot.reply_to(message, "the given date is in a wrong format, please enter in this format : dd.mm.yy")



@bot.message_handler(func=lambda message: message.chat.id in users_states and users_states[message.chat.id] and users_states[message.chat.id] == "waiting_for_date_for_category")
def generate_report_by_category(message: telebot.types.Message):
    try:

        nutritions =users_selections[message.chat.id]
        datetime.strptime(message.text, "%d.%m.%y")  # checks if the date is in the correct format
        user_history_db = dao.get_foods_by_user_and_date(message.from_user.id, message)
        report = report_controller.generate_report_by_category(message, user_history_db,nutritions)
        if not report:
            bot.send_message(message.chat.id, "there is no data for the given date.")
        else:
            bot.send_message(message.chat.id, report)
        users_states[message.chat.id] = None
        users_selections[message.chat.id] = []
        dao.save_users_state(users_states)
        show_menu(message.chat.id, message.chat.first_name, "Choose an option below:")

    except ValueError:
        logger.warning(f"[user: {message.chat.first_name!r} entered wrong date format]")
        bot.reply_to(message, "the given date is in a wrong format, please enter in this format : dd.mm.yy")




logger.info("> Starting bot")
bot.infinity_polling()
logger.info("< terminating bot!")


