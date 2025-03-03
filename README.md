# Bite Buddy Bot (BBB)

## The Team
- Bayan kassem
- Or Hasan
- Muhammad Imad

## About this bot

Bite Buddy Bot (BBB) is a nutrition tracker Telegram bot designed to help users keep track of their daily food intake and generate reports based on their eating habits. The bot allows users to add food items, view their eating history, and generate reports by date or category.

https://web.telegram.org/k/#@Bite_Buddy_Bot

🚧 ADD SCREENSHOTS/GIFS/SCREENCAST HERE (REFER TO MARKDOWN'S SYNTAX FOR HELP ON DISPLAYING IMAGES)
 
## About this bot

Add Food: Users can add food items they have eaten, including details such as calories, healthiness, and amount.  
Generate Reports: Users can generate reports based on specific dates or categories to analyze their eating habits.  
View Eaten Food: Users can view the food items they have eaten on a specific date.  

## Technologies Used

**Python**: The primary programming language used for the bot.  
**pyTelegramBotAPI**: A Python wrapper for the Telegram Bot API.  
**MongoDB**: Used for storing user data and food history.  
**Google Search Results API**: Used for fetching food information.  

## Usage
**Start the bot**: Send /start to the bot to see the main menu.  
**Add Food**: Select "Add_Food" from the menu and enter the food item you have eaten.  
**Generate Report**: Select "Generate_Report" and choose the type of report you want to generate.  
**View Eaten Food**: Select "Show_eaten_food" and enter the date to view the food items eaten on that date.

## Instructions for Developers 
### Prerequisites
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- (uv van install python for you)
- MongoDB (PyMongo)
- Telegram API (pyTelegramBotAPI)
- Google Search Results API (google-search-results)

### Setup
- git clone this repository 
- cd into the project directory
- Get an API Token for a bot via the [BotFather](https://telegram.me/BotFather)
- Create a `bot_secretes.py` file with your bot token:

      BOT_TOKEN = 'xxxxxxx'
  
### Running the bot        
- Run the bot (This will also install Python 3.13 and all dependencies):

      uv run bot.py
