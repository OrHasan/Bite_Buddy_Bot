import telebot
from google import genai
from google.genai import types

import bot_secrets
from DAO.dao_controller import DaoController as Dao
# from datetime import datetime


# ToDo: Add try-except in case of api-connection error
class GeminiController:
    def __init__(self):
        self.client = genai.Client(api_key=bot_secrets.gemini_api)
        self.sys_instruct=("You are an advisor of a nutrition tracker Telegram app named Bite Buddy"
                           "(or BBB - Bite Buddy Bot)."
                           "Your advices need to be short and concise (single line as the maximum length),"
                           "and should be tailored to the user's needs."
                           "You can use emojis and fun tone to make the advice more engaging."
                           "You get as input the instructions, that can include data about the user's eating history,"
                           "and you need to generate a message or advice to that user according to that input."
                           "The user can be a beginner or an advanced user, and can have different goals"
                           "(e.g., weight loss, muscle gain)."
                           "You need to generate a message that is suitable for the user's level and goal."
                           "The user can also have different dietary restrictions (e.g., vegan, gluten-free).")

        # Continues chat version: (not working with the instructions right now, and AIs suggestions are wrong)
        # self.chat = self.client.chats.create(
        #     model="gemini-2.0-flash",
        #     history=[]
        # )
        # self.chat.send_message(types.Part.from_text(self.sys_instruct))

    def motivational_message(self):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=self.sys_instruct),
            contents=["Give the user a motivational message to keep them on track with their diet."]
        )
        # response = self.chat.send_message("Give the user a motivational message to keep them on track with their diet.")
        # response = self.chat.send_message(types.Part.from_text("Give the user a motivational message to keep them on track with their diet."))
        return response.text

    def improvement_advice(self, user_id:int, date:telebot.types.Message):
        # data = Dao().get_foods_by_user_and_date(user_id, datetime.now().date().strftime("%d.%m.%y"))
        data = Dao().get_foods_by_user_and_date(user_id, date)

        labels = ['calories', 'total_fat', 'cholesterol', 'sodium',
                  'total_carbohydrate', 'potassium', 'protein', 'sugars']
        details = {}
        history = ''

        for label in labels:
            details[label] = .0

        for food in data:
            details['calories'] += float(food['calories'].split()[0])
            details['total_fat'] += float(food['total_fat'].split()[0])
            details['cholesterol'] += float(food['cholesterol'].split()[0])
            details['sodium'] += float(food['sodium'].split()[0])
            details['total_carbohydrate'] += float(food['total_carbohydrate'].split()[0])
            details['potassium'] += float(food['potassium'].split()[0])
            details['protein'] += float(food['protein'].split()[0])
            details['sugars'] += float(food['sugars'].split()[0])

        details['calories'] = str(details['calories'])
        details['total_fat'] = str(details['total_fat'] + ' gr')
        details['cholesterol'] = str(details['cholesterol'] + ' mg')
        details['sodium'] = str(details['sodium'] + ' mg')
        details['total_carbohydrate'] = str(details['total_carbohydrate'] + ' gr')
        details['potassium'] = str(details['potassium'] + ' mg')
        details['protein'] = str(details['protein'] + ' gr')
        details['sugars'] = str(details['sugars'] + ' gr')

        for key, value in details.items():
            history += key + ': ' + value + '\n'

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=self.sys_instruct),
            contents=["Tell the user how he can improve his diet according to the following eating history "
                      "(day average):\n" + history]
        )
        return response.text

    def user_question(self, question:telebot.types.Message) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=self.sys_instruct),
            contents=["Answer the following user question (please make sure the user asks only relevant questions"
                      "to this bot topic):\n" + question.text]
        )
        return response.text
