from google import genai
from google.genai import types

import bot_secrets


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
        return response

    def improvement_advice(self, history:str):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=self.sys_instruct),
            contents=["Tell the user how he can improve his diet according to the following eating history "
                      "(day average):\n" + history]
        )
        return response.text

    def user_question(self, question:str):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=self.sys_instruct),
            contents=["Answer the following user question (please make sure the user asks only relevant questions"
                      "to this bot topic):\n" + question]
        )
        return response.text
