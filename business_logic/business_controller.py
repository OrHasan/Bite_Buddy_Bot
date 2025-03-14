import logging
# from collections import defaultdict
import telebot
from datetime import datetime
from telebot import types

import bot_secrets
from DAO.dao_controller import DaoController
from business_logic.report_controller import ReportController
from business_logic.api_manager import APIManager
from business_logic.graph_controller import GraphController
from business_logic.gemini_controller import GeminiController


logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(bot_secrets.BOT_TOKEN)
api_manager=APIManager()
dao = DaoController()
users_states = {}
users_selections = {}
report_controller=ReportController()


def show_reports_categroy(chat_id,username, message):
    logger.info(f"[showing report categories for user: {username!r}]")

    markup = types.InlineKeyboardMarkup(row_width=2)  # row_width => how many buttons per row
    button1 = types.InlineKeyboardButton("daily report", callback_data="report_by_date")
    button2 = types.InlineKeyboardButton("report by category", callback_data="report_by_category")
    markup.add(button1, button2)
    bot.send_message(chat_id, message, reply_markup=markup)


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


def show_charts_categroy(chat_id,username, message):
    logger.info(f"[showing chart report categories for user: {username!r}]")

    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("Pie-Chart", callback_data="pie_chart_report")
    button2 = types.InlineKeyboardButton("Bar-Chart", callback_data="bar_chart_report")
    markup.add(button1, button2)
    bot.send_message(chat_id, message, reply_markup=markup)


def show_ai_categroy(chat_id,username, message):
    logger.info(f"[showing AI categories for user: {username!r}]")

    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("Get Motivation!", callback_data="ai_motivation")
    button2 = types.InlineKeyboardButton("Get Advice", callback_data="ai_advice")
    button3 = types.InlineKeyboardButton("Ask Question", callback_data="ai_question")
    markup.add(button1, button2, button3)
    bot.send_message(chat_id, message, reply_markup=markup)


def show_menu(user_id,username,message):
    logger.info(f"[showing menu for user: {username!r}]")

    markup = types.InlineKeyboardMarkup(row_width=2)  # row_width => how many buttons per row
    button1 = types.InlineKeyboardButton("Add Food", callback_data="add_food")
    button2 = types.InlineKeyboardButton("Generate Report", callback_data="generate_report")
    button3 = types.InlineKeyboardButton("Generate Chart", callback_data="chart_report")
    button4 = types.InlineKeyboardButton("Get Food Info", callback_data="get_food_info")
    button5 = types.InlineKeyboardButton("Ask AI", callback_data="ai_advisor")
    markup.add(button1, button2, button3, button4, button5)
    bot.send_message(user_id, message, reply_markup=markup)


@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message):
    global users_states
    users_states=dao.get_user_states()

    show_menu(message.chat.id,message.chat.first_name,"Welcome to Bite Buddy, your nutrition tracker!"
                                                      " Choose an option below:")


def update_buttons(call):
    markup = types.InlineKeyboardMarkup(row_width=3)
    button1 = types.InlineKeyboardButton(
        f"fat {'✅' if 'fat' in users_selections[call.message.chat.id] else '❌'}",
        callback_data="fat")

    button2 = types.InlineKeyboardButton(
        f"cholesterol {'✅' if 'cholesterol' in users_selections[call.message.chat.id] else '❌'}",
        callback_data="cholesterol")

    button3 = types.InlineKeyboardButton(
        f"carbohydrate {'✅' if 'carbohydrate' in users_selections[call.message.chat.id] else '❌'}",
        callback_data="carbohydrate")

    button4 = types.InlineKeyboardButton(
        f"protein {'✅' if 'protein' in users_selections[call.message.chat.id] else '❌'}",
        callback_data="protein")

    button5 = types.InlineKeyboardButton(
        f"sodium {'✅' if 'sodium' in users_selections[call.message.chat.id] else '❌'}",
        callback_data="sodium")

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
        show_reports_categroy(call.message.chat.id, call.message.chat.first_name, "click on the desired report")

    elif call.data == "get_food_info":
        bot.send_message(call.message.chat.id, "please enter a food name to get information about it.")
        users_states[call.message.chat.id] = 'get_food_info'
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: get_food_info.]")

    elif call.data == "report_by_date":
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: report_by_date.]")
        bot.send_message(call.message.chat.id, "please enter date, in this format dd.mm.yy etc: 03.03.25")
        users_states[call.message.chat.id] = 'waiting_for_date'
        dao.save_users_state(users_states)

    elif call.data == "report_by_category":
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: report_by_category.]")
        show_reports_nutritions(call.message.chat.id, call.message.chat.first_name,
                                "Please select the desired nutritions. Click 'Done' when finished.")

    elif call.data == "chart_report":
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: chart_report.]")
        show_charts_categroy(call.message.chat.id, call.message.chat.first_name, "Please select the chart type")

    elif call.data == "pie_chart_report":
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: pie_chart_report.]")
        bot.send_message(call.message.chat.id, "Please enter date, in this format dd.mm.yy etc: 03.03.25")
        users_states[call.message.chat.id] = 'waiting_for_pie_chart_data'
        dao.save_users_state(users_states)

    elif call.data == "bar_chart_report":
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: bar_chart_report.]")
        bot.send_message(call.message.chat.id, "Please enter date, in this format dd.mm.yy etc: 03.03.25")
        users_states[call.message.chat.id] = 'waiting_for_bar_chart_data'
        dao.save_users_state(users_states)

    elif call.data == "ai_advisor":
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: ai_advisor.]")
        show_ai_categroy(call.message.chat.id, call.message.chat.first_name, "Please select an option")

    elif call.data == "ai_motivation":
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: ai_motivation.]")
        motivation_message = GeminiController().motivational_message()
        bot.send_message(call.message.chat.id, motivation_message)
        logger.info(f"[user: {call.message.chat.first_name!r}]"
                    f" got the following motivational message: {motivation_message!r}")

    elif call.data == "ai_advice":
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: ai_advice.]")
        bot.send_message(call.message.chat.id, "Please enter date for the advice,"
                                               " in this format dd.mm.yy etc: 03.03.25")
        users_states[call.message.chat.id] = 'waiting_for_date_for_advice'
        dao.save_users_state(users_states)
        # bot.send_message(call.message.chat.id, GeminiController().improvement_advice(call.message.from_user.id))

    elif call.data == "ai_question":
        logger.info(f"[user: {call.message.chat.first_name!r} clicked: ai_question.]")
        bot.send_message(call.message.chat.id, "Please enter your question (relevant questions only)")
        users_states[call.message.chat.id] = 'waiting_for_user_question'
        dao.save_users_state(users_states)

    elif (call.data == "fat" or call.data == "cholesterol" or call.data == "carbohydrate" or call.data == "protein"
          or call.data == "sodium" or call.data == "potassium"):
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


@bot.message_handler(func=lambda message: message.chat.id in users_states
                                          and users_states[message.chat.id] == 'waiting_for_food_name')
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
        bot.send_message(message.chat.id, "an error occurred during adding food.")
        show_menu(message.chat.id, message.chat.first_name, "Choose an option below:")


@bot.message_handler(func=lambda message: message.chat.id in users_states
                                          and users_states[message.chat.id] == 'get_food_info')
def get_food_info(message: telebot.types.Message):
    try:
        nutrition_info=api_manager.get_info_by_api(message.text)
        if nutrition_info== {}:
            logger.warning(f"[user: {message.chat.first_name!r} entered invalid food]")
            bot.send_message(message.chat.id, "please enter a valid food")
        else:
            nutrition_message = (
                "🍽 Nutritional Information:\n"
                f"🔥 Calories: {nutrition_info['calories']} kcal\n"
                f"🍗 Protein: {nutrition_info['protein']}\n"
                f"🥔 Carbohydrates: {nutrition_info['total_carbohydrate']}\n"
                f"🥑 Total Fat: {nutrition_info['total_fat']}\n"
                f"🧂 Sodium: {nutrition_info['sodium']}\n"
                f"🍌 Potassium: {nutrition_info['potassium']}\n"
                f"🫀 Cholesterol: {nutrition_info['cholesterol']}\n"
                f"🍬 Sugars: {nutrition_info['sugars']}\n"
            )
            bot.send_message(message.chat.id, f"{message.text} have:\n {nutrition_message}")
            users_states[message.chat.id] = None
            show_menu(message.chat.id, message.chat.first_name, "Choose an option below:")
    except Exception:
        bot.send_message(message.chat.id, "an error occurred during adding food.")
        show_menu(message.chat.id, message.chat.first_name, "Choose an option below:")


@bot.message_handler(func=lambda message: message.chat.id in users_states
                                          and users_states[message.chat.id] == 'waiting_for_date')
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


@bot.message_handler(func=lambda message: message.chat.id in users_states and users_states[message.chat.id]
                                          and users_states[message.chat.id] == "waiting_for_date_for_category")
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


@bot.message_handler(func=lambda message: message.chat.id in users_states and users_states[message.chat.id]
                                          and users_states[message.chat.id] == "waiting_for_pie_chart_data")
def generate_pie_chart(message: telebot.types.Message):
    try:
        datetime.strptime(message.text, "%d.%m.%y") #checks if the date is in the correct format
        logger.info(f"[user: {message.chat.first_name!r}] gave the date: {message.text!r} for the pie chart")
        buffer = GraphController().pie_chart(message.from_user.id, message)

        if not buffer:
            bot.send_message(message.chat.id, "there is no data for the given date.")
            logger.info(f"[there is no data for the given date,"
                        f" pie chart not created for user: {message.chat.first_name!r}]")
        else:
            bot.send_photo(message.chat.id, buffer)
            logger.info(f"[Pie chart created successfully for user: {message.chat.first_name!r}]")
            buffer.close()

        users_states[message.chat.id] = None
        show_menu(message.chat.id, message.chat.first_name, "Choose an option below:")

    except ValueError:
        logger.warning(f"[user: {message.chat.first_name!r} entered wrong date format]")
        bot.reply_to(message, "the given date is in a wrong format, please enter in this format : dd.mm.yy")


@bot.message_handler(func=lambda message: message.chat.id in users_states and users_states[message.chat.id]
                                          and users_states[message.chat.id] == "waiting_for_bar_chart_data")
def generate_bar_chart(message: telebot.types.Message):
    try:
        datetime.strptime(message.text, "%d.%m.%y")  # checks if the date is in the correct format
        logger.info(f"[user: {message.chat.first_name!r}] gave the date: {message.text!r} for the bar chart")
        buffer = GraphController().bar_chart(message.from_user.id, message)

        if not buffer:
            bot.send_message(message.chat.id, "there is no data for the given date.")
            logger.info(f"[there is no data for the given date,"
                        f" bar chart not created for user: {message.chat.first_name!r}]")
        else:
            bot.send_photo(message.chat.id, buffer)
            logger.info(f"[Bar chart created successfully for user: {message.chat.first_name!r}]")
            buffer.close()

        users_states[message.chat.id] = None
        show_menu(message.chat.id, message.chat.first_name, "Choose an option below:")

    except ValueError:
        logger.warning(f"[user: {message.chat.first_name!r} entered wrong date format]")
        bot.reply_to(message, "the given date is in a wrong format, please enter in this format : dd.mm.yy")


@bot.message_handler(func=lambda message: message.chat.id in users_states and users_states[message.chat.id]
                                          and users_states[message.chat.id] == "waiting_for_date_for_advice")
def generate_ai_advice(message: telebot.types.Message):
    try:
        datetime.strptime(message.text, "%d.%m.%y")  # checks if the date is in the correct format
        logger.info(f"[user: {message.chat.first_name!r}] gave the date: {message.text!r} for an AI advice")

        advice = GeminiController().improvement_advice(message.from_user.id, message)

        bot.send_message(message.chat.id, advice)
        logger.info(f"[user: {message.chat.first_name!r}] got the following advice: {advice!r}")
        users_states[message.chat.id] = None
        show_menu(message.chat.id, message.chat.first_name, "Choose an option below:")

    except ValueError:
        logger.warning(f"[user: {message.chat.first_name!r} entered wrong date format]")
        bot.reply_to(message, "the given date is in a wrong format, please enter in this format : dd.mm.yy")


@bot.message_handler(func=lambda message: message.chat.id in users_states and users_states[message.chat.id]
                                          and users_states[message.chat.id] == "waiting_for_user_question")
def generate_ai_answer(message: telebot.types.Message):
    logger.info(f"[user: {message.chat.first_name!r}] gave the following question for the ai: {message.text!r}")
    answer = GeminiController().user_question(message)
    bot.send_message(message.chat.id, answer)
    logger.info(f"[user: {message.chat.first_name!r}] got the following AI answer: {answer!r}")
    users_states[message.chat.id] = None
    show_menu(message.chat.id, message.chat.first_name, "Choose an option below:")


@bot.message_handler(func=lambda message: message.chat.id not in users_states or users_states[message.chat.id] is None)
def handle_random_message(message: telebot.types.Message):
    # If the user is not in any expected state (i.e., None), send the menu again
    bot.send_message(message.chat.id, "I didn't quite get that."
                                      " Please choose one of the options from the menu below:")
    show_menu(message.chat.id, message.chat.first_name, "Choose an option below:")


logger.info("> Starting bot")
bot.infinity_polling()
logger.info("< terminating bot!")
