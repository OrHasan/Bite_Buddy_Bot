import logging
import bot_secrets
import telebot
from telebot import types
from DAO.dao_controller import DaoController
from business_logic.api_manager import API_Manager


bot = telebot.TeleBot(bot_secrets.TOKEN)
user_states = {}
bot = telebot.TeleBot(bot_secrets.TOKEN)
api_manager=API_Manager()
user_state = {}


@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)  # row_width => how many buttons per row
    button1 = types.InlineKeyboardButton("Add_Food", callback_data="add_food")
    button2 = types.InlineKeyboardButton("Generate_Report", callback_data="view_stats")
    button3 = types.InlineKeyboardButton("Show_eaten_food", callback_data="help")

    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Welcome to Bite Buddy, your nutrition tracker! Choose an option below:",
                     reply_markup=markup)

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
    except Exception:
        bot.send_message(message.chat.id, "please enter what you have eaten.")



@bot.message_handler(commands=["show_food"])
def ask_for_food_name(message):
    """Step 1: Ask the user for the food name."""
    bot.reply_to(message, "🍽️ Please enter the food name you want to search:")
    user_states[message.chat.id] = "waiting_for_food_name"


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_food_name")
def fetch_eaten_food_info(message):
    """Step 2: Retrieve food information from the database."""
    food_name = message.text
    dao = DaoController()
    food_info = dao.get_foods_by_user_and_date(message.chat.id, food_name)

    if food_info:
        response = f"🍏 Food: {food_info['name']}\n📌 Category: {food_info['category']}\n🔥 Calories: {food_info['calories']} kcal"
    else:
        response = "⚠️ Food not found in the database."

    bot.reply_to(message, response)
    user_states.pop(message.chat.id, None)


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_food_name")
def fetch_food_info(message):
    """Step 2: Retrieve food information from the database."""
    food_name = message.text
    api_maneger = API_Manager()
    food_info = api_maneger.get_info_by_api(food_name)

    if food_info:
        response = f"🍏 Food: {food_info['name']}\n📌 Category: {food_info['category']}\n🔥 Calories: {food_info['calories']} kcal"
    else:
        response = "⚠️ Food not found in the database."

    bot.reply_to(message, response)
    user_states.pop(message.chat.id, None)


@bot.message_handler(func=lambda m: True)
def echo_all(message: telebot.types.Message):

    bot.reply_to(message, f"You said: {message.text}")




bot.infinity_polling()

