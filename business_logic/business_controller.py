import logging

import bot_secrets
import telebot

from DAO.dao_controller import DaoController
from business_logic.api_manager import API_Manager

bot = telebot.TeleBot(bot_secrets.TOKEN)
user_states = {}


@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message):
    bot.reply_to(message, "🤖 Welcome! 🤖")



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

