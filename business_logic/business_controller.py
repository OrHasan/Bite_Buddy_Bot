import logging
import bot_secrets
import telebot

from datetime import datetime
from telebot import types
from DAO.dao_controller import DaoController
from business_logic.api_manager import API_Manager



bot = telebot.TeleBot(bot_secrets.TOKEN)
user_states = {}
api_manager=API_Manager()
dao = DaoController()
user_state = {}

def show_reports_categroy(chat_id, message):
    markup = types.InlineKeyboardMarkup(row_width=2)  # row_width => how many buttons per row
    button1 = types.InlineKeyboardButton("daily report", callback_data="report_by_date")
    button2 = types.InlineKeyboardButton("report by categroy", callback_data="reportr_by_categroy")
    markup.add(button1, button2)
    bot.send_message(chat_id, message,
                     reply_markup=markup)


def show_menu(chat_id,message):
    markup = types.InlineKeyboardMarkup(row_width=2)  # row_width => how many buttons per row
    button1 = types.InlineKeyboardButton("Add_Food", callback_data="add_food")
    button2 = types.InlineKeyboardButton("Generate_Report", callback_data="generate_report")
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
    elif call.data == "generate_report":
        show_reports_categroy(call.message.chat.id, "click on the desired report")


    elif call.data == "Show_eaten_food":
        bot.send_message(call.message.chat.id, "please enter the date to see food eaten in that date")
        user_state[call.message.chat.id] = 'show_food_per_date'

    elif call.data == "report_by_date":
        bot.send_message(call.message.chat.id, "please enter date.")
        user_state[call.message.chat.id] = 'waiting_for_date'


@bot.message_handler(func=lambda message: message.chat.id in user_state and user_state[message.chat.id] == 'waiting_for_food_name')
def add_food(message: telebot.types.Message):
    try:
        result=api_manager.get_info_by_api(message.text)

        if result==None:
            bot.send_message(message.chat.id, "please enter a valid food")
        else:
            dao.add_food(food_item= result, user_id=message.chat.id, date=message.date)
            bot.reply_to(message, f"added food successfuly : {message.text}")
            user_state[message.chat.id] = None
            show_menu(message.chat.id,"Choose an option below:")
    except Exception:
        bot.send_message(message.chat.id, "please enter what you have eaten.")


@bot.message_handler(func=lambda message: message.chat.id in user_state and user_state[message.chat.id] == 'Show_eaten_food')
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
def generate_report(message: telebot.types.Message):
    # logger.info(f"generate report for #{message.chat.id}")
    # print(datetime.datetime([:6], tzinfo=datetime.timezone.utc))
    # ToDo: Delete the simulation DB data
    user_history_db = [{
        'date': "02.03.25 13:45",
        'name': "Hamburger",
        'data': {
            'Calories': 3000,
            'Healthy': "Yes!!",
            'Amount': 5
        }
    },
    {
        'date': "03.03.25 16:00",
        'name': "Pizza",
        'data': {
            'Calories': 384.36,
            'Healthy': "Maybe 😉",
            'Amount': 12
        }
    },
    {
        'date': "03.03.25 11:43",
        'name': "air",
        'data': {
            'Calories': 9999.99,
            'Healthy': "NNOOO",
            'Amount': 240
        }
    }]

    last_date = ""
    report = ""
    # _, *date = message.text.split()
    date = message.text


    # ToDo: Return the MongoDB find() function
    # for food in user_history_db.find():
    for food in user_history_db:
        food_date = datetime.strptime(food['date'], "%d.%m.%y %H:%M").strftime("%d.%m.%y")

        # if not date or food_date == date[0]:
        if not date or food_date == date:
            if last_date != food_date:
                report += f"\n{food_date}\n\n"
                last_date = food_date
            report += f"{food['name']}:"

            for data_name, data_info in food['data'].items():
                report += f"\n{data_name}: {data_info}"

            report += "\n\n"

    if date and not report:
        bot.reply_to(message, "This date isn't exist in your history or been written in the wrong format"
                              ", please choice another date")
    else:
        bot.reply_to(message, report)
    show_menu(message.chat.id,"Choose an option below:")



@bot.message_handler(func=lambda m: True)
def echo_all(message: telebot.types.Message):

    bot.reply_to(message, f"You said: {message.text}")




bot.infinity_polling()

