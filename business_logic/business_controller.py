import logging

import bot_secrets
import telebot




bot = telebot.TeleBot(bot_secrets.TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message):
    bot.reply_to(message, "🤖 Welcome! 🤖")

@bot.message_handler(func=lambda m: True)
def echo_all(message: telebot.types.Message):

    bot.reply_to(message, f"You said: {message.text}")


bot.infinity_polling()

