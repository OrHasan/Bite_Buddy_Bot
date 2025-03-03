from pprint import pprint

from serpapi import GoogleSearch
from bot_secrets import api_key



class API_Manager:
    def get_info_by_api(self,food_name):
        params = {
            "q": food_name,
            "api_key": api_key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        nutrition_information = results["knowledge_graph"]['list']
        return nutrition_information



