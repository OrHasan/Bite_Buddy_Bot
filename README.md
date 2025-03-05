# Bite Buddy Bot (BBB)

<br />

<div align="center">
  
  ![BBB Avatar][BBB-Icon]
  
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#the-team">The Team</a>
    </li>
    <li>
      <a href="#summary">Summary</a>
    </li>
    <li>
      <a href="#about-this-bot">About this bot</a>
    </li>
    <li>
      <a href="#technologies-used">Technologies Used</a>
    </li>
    <li>
      <a href="#used">Used</a>
    </li>
    <li><a href="#instructions-for-developers">Instructions for Developers</a></li>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#setup">Setup</a></li>
        <li><a href="#running-the-bot">Running the bot</a></li>
      </ul>
  </ol>
</details>

<!-- THE TEAM -->
## The Team

- Bayan kassem
- Or Hasan
- Mohammad Imad

<!-- SUMMARY -->
## Summary

Bite Buddy Bot (BBB) is a nutrition tracker Telegram bot designed to help users keep track of their daily food intake and generate reports and graphs based on their eating habits. The bot allows users to add food items, view their eating history, and generate graphs and reports by date or category.

https://web.telegram.org/k/#@Bite_Buddy_Bot

<div align="center">
  
  ![Main Menu][Main-Menu]
  ![Add Food][Add-Food]
  ![Get Food Info][Get-Food-Info]
  ![Generate Report by Category][Generate-Report-by-Category]
  ![Generate Pie Chart][Generate_Pie_Chart]
  ![Generate Calories Bar Chart][Generate-Calories-Bar-Chart]
  ![AI Advice][AI-Advice]
  ![AI User Question][AI-User-Question]
  
</div>

<!-- ABOUT THIS BOT -->
## About this bot

Add Food: Users can add food items they have eaten, including details such as calories, healthiness, and amount.  
Generate Reports: Users can generate reports based on specific dates or categories to analyze their eating habits.  
Generate charts: Users can generate charts based on specific dates to view the calories and percentages of nutrition values.  
View Food's nutrition values: Users can view nutrition values of a specefic food.

<!-- TECHNOLOGIES USED -->
## Technologies Used

**Python**: The primary programming language used for the bot.  
**pyTelegramBotAPI**: A Python wrapper for the Telegram Bot API.  
**MongoDB**: Used for storing user data and food history.  
**Nutritionix API**: Used for fetching food information.  

<!-- USAGE -->
## Usage
**Start the bot**: Send /start to the bot to see the main menu.  

**Add Food**: Select "Add Food" from the menu and enter the food item you have eaten.  

**Generate Report**: Select "Generate Report" and choose the type of report you want to generate. 

**Generate Chart**: Select "Generate Chart" and choose the type of chart you want to generate. 

**Get Food Info**: Select "Get Food Info" and enter a food that you want to view its nutrition values.

**Ask AI**: Select "Ask AI" to get motivations or advices from an AI.

<!-- INSTRUCTIONS FOR DEVELOPERS -->
## Instructions for Developers 
### Prerequisites
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- (uv van install python for you)
- MongoDB (PyMongo)
- Telegram API (pyTelegramBotAPI)
- Matplotlib
- Google-genai (Gemeni)

### Setup
- git clone this repository 
- cd into the project directory
- Get an API Token for a bot via the [BotFather](https://telegram.me/BotFather)
- Sign Up to Nutritionx https://developer.nutritionix.com/signup to recieve your nutritionx app ID and nutritionx API token.
- Create a `bot_secretes.py` file with your bot token and nutritionx tokens:
- 

      BOT_TOKEN = 'xxxxxxx'
      nutrition_x_api = 'xxxxxxx'
      nutrition_x_app_id = 'xxxxxxx'
  
### Running the bot        
- Run the bot (This will also install Python 3.13 and all dependencies):

      uv run bot.py


<!-- MARKDOWN LINKS & IMAGES -->
[BBB-Icon]: Media/Bite_Buddy_Bot_Profile_Picture_v.2.png
[Main-Menu]: Media/Examples/Main_Menu.png
[Add-Food]: Media/Examples/Add_Food.png
[Not-a-Food]: Media/Examples/Add_Food_-_Not_a_Food.png
[Get-Food-Info]: Media/Examples/Get_Food_Info.png
[Generate-Daily-Report]: Media/Examples/Generate_Daily_Report.png
[Generate-Report-by-Category]: Media/Examples/Generate_Report_by_Category.png
[Generate_Pie_Chart]: Media/Examples/Generate_Daily_Pie_Chart.png
[Generate-Calories-Bar-Chart]: Media/Examples/Generate_Daily_Calories_Bar_Chart.png
[AI-Motivation-Message]: Media/Examples/AI_Motivation_Message.png
[AI-Advice]: Media/Examples/AI_Advice.png
[AI-User-Question]: Media/Examples/AI_User_Question.png
