import logging

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

class Report_Controller:
    def generate_report_by_date(self, message,user_history_db):
        # logger.info(f"generate report for #{message.chat.id}")
        logger.info(f"[generating daily report for user: {message.chat.first_name!r}.]")
        date=message.text


        last_date = ""
        report = ""
        # ToDo: Return the MongoDB find() function
        # for food in user_history_db.find():
        for food in user_history_db:
            food_date = food['date'].strftime("%d.%m.%y")

            # if not date or food_date == date[0]:
            if not date or food_date == date:
                if last_date != food_date:
                    report += f"\n{food_date}\n\n"
                    last_date = food_date
                report += f"{food['name']}:"

                for data_name, data_info in food.items():
                    if data_name == "name" or data_name == "date" or data_name == "user_id" or data_name == "_id":
                        continue
                    data_name = data_name.split('_')[-1]  # this is to treat the total_Fat and total_carbs case
                    report += f"\n{data_name}: {data_info}"

                report += "\n\n"

            return report

    def generate_report_by_category(self, message, user_history_db, nutritions):
        logger.info(f"[generating category report for user: {message.chat.first_name!r}.]")
        last_date = ""
        report = ""
        date = message.text
        for i in range(len(nutritions)):
            if nutritions[i]=="fat" or nutritions[i]=="carbohydrate":
                nutritions[i]="total_"+nutritions[i]
        # ToDo: Return the MongoDB find() function
        # for food in user_history_db.find():
        for food in user_history_db:
            food_date = food['date'].strftime("%d.%m.%y")

            # if not date or food_date == date[0]:
            if not date or food_date == date:
                if last_date != food_date:
                    report += f"\n{food_date}\n\n"
                    last_date = food_date
                report += f"{food['name']}:"

                for data_name, data_info in food.items():
                    if data_name == "name" or data_name == "date" or data_name == "user_id" or data_name == "_id" or data_name not in nutritions:
                        continue
                    data_name=data_name.split('_')[-1] # this is to treat the total_Fat and total_carbs case
                    report += f"\n{data_name}: {data_info}"

                report += "\n\n"
        return report
