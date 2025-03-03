import logging

import bot_secrets
import telebot

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(bot_secrets.TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message):
    logger.info(f"+ Start chat #{message.chat.id} from {message.chat.username}")
    bot.reply_to(message, "🤖 Welcome! 🤖")

@bot.message_handler(commands=["report"])
def generate_report(message: telebot.types.Message):
    logger.info(f"generate report for #{message.chat.id}")

    # ToDo: Delete the simulation DB data
    user_history_db = [{
        'date': "02.03.25",
        'name': "Hamburger",
        'data': {
            'Calories': 3000,
            'Healthy': "Yes!!",
            'Amount': 5
        }
    },
    {
        'date': "03.03.25",
        'name': "Pizza",
        'data': {
            'Calories': 384.36,
            'Healthy': "Maybe 😉",
            'Amount': 12
        }
    },
    {
        'date': "03.03.25",
        'name': "air",
        'data': {
            'Calories': 9999.99,
            'Healthy': "NNOOO",
            'Amount': 240
        }
    }]

    last_date = ""
    report = ""
    _, *date = message.text.split()

    # ToDo: Return the MongoDB find() function
    # for food in user_history_db.find():
    for food in user_history_db:
        if not date or food['date'] == date[0]:
            if last_date != food['date']:
                report += f"\n{food['date']}\n\n"
                last_date = food['date']
            report += f"{food['name']}:"

            for data_name, data_info in food['data'].items():
                report += f"\n{data_name}: {data_info}"

            report += "\n\n"

    if date and not report:
        bot.reply_to(message, "This date isn't exist in your history or been written in the wrong format"
                              ", please choice another date")
    else:
        bot.reply_to(message, report)


@bot.message_handler(func=lambda m: True)
def echo_all(message: telebot.types.Message):
    logger.info(f"[#{message.chat.id}.{message.message_id} {message.chat.username!r}] {message.text!r}")
    bot.reply_to(message, f"You said: {message.text}")


logger.info("> Starting bot")
bot.infinity_polling()
logger.info("< Goodbye!")
