class Report_Controller:
    def generate_report_by_date(self, message,user_history_db):
        # logger.info(f"generate report for #{message.chat.id}")
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

    def generate_report_by_category(self, message, user_history_db, nutrition):
        last_date = ""
        report = ""
        date = message.text
        if nutrition=="fat" or nutrition=="carbohydrate":
            nutrition="total_"+nutrition
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
                    if data_name == "name" or data_name == "date" or data_name == "user_id" or data_name == "_id" or data_name != nutrition:
                        continue
                    data_name=data_name.split('_')[-1] # this is to treat the total_Fat and total_carbs case
                    report += f"\n{data_name}: {data_info}"

                report += "\n\n"
        return report
