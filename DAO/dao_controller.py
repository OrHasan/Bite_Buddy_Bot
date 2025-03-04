import logging

from pymongo import MongoClient
from datetime import datetime
logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
class DaoController:

    def __init__(self, db_name="food_info_db", uri="mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]


    def add_food(self,food_name, food_item, user_id, date):
        """Adds a new food item to the database."""
        self.collection = self.db["foods"]
        logger.info(f"[adding food to the database for the user: {user_id!r}.]")
        food_item["user_id"] = user_id
        food_item["date"] = date
        food_item["name"] = food_name

        try:
            result = self.collection.insert_one(food_item)
        except Exception as e:
            # Code to handle the exception
            logger.error(f"[an error occurred inside add_food func, error:{e}.]")
            raise e
        logger.info(f"[adding food for the user: {user_id!r} , result={result.acknowledged} .]")
        return result.inserted_id

    def get_user_states(self):
        self.collection = self.db["users_states"]
        user_states_cursor = self.collection.find()
        user_states = {user_state["user_id"]: user_state["state"] for user_state in user_states_cursor}
        return user_states

    def save_users_state(self,users_states):
        logger.info(f"[saving users states to the database.]")
        self.collection = self.db["users_states"]
        for user_id,user_state in users_states.items():
            self.collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "state": user_state
                    }
                },
                upsert=True
            )
            logger.info(f"User state saved/updated/removed for user_id: {user_id}")

    def get_foods_by_user_and_date(self, user_id, message):
        """Retrieves all foods eaten by a specific user on a specific date."""
        self.collection = self.db["foods"]
        logger.info(f"[extracting data from DB for the user: {user_id!r}, inside the function get_foods_by_user_and_date.]")
        date = datetime.strptime(message.text, "%d.%m.%y")
        start_of_day = datetime(date.year, date.month, date.day)  # start of the given day
        end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59, 999999)  # end of the given day

        # Query the database
        result = self.collection.find({
            "user_id": user_id,
            "date": {"$gte": start_of_day, "$lte": end_of_day}
        })
        return list(result)

