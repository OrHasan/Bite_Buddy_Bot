from pymongo import MongoClient


class DaoController:

    def __init__(self, db_name="food_info_db", collection_name="foods", uri="mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def add_food(self, food_item):
        """Adds a new food item to the database."""

        result = self.collection.insert_one(food_item)
        return result.inserted_id

    def get_food(self, name):
        """Retrieves a food item by date."""
        return self.collection.find_one({"name": name})

    def get_foods_by_user_and_date(self, user_id, date):
        """Retrieves all foods eaten by a specific user on a specific date."""
        return list(self.collection.find({"user_id": user_id, "date": date}))

    def get_all_foods(self):
        """Retrieves all food items."""
        return list(self.collection.find())
