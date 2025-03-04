from pprint import pprint
import requests
import logging

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


from bot_secrets import nutrition_x_api,nutrition_x_app_id


class API_Manager:
    def get_info_by_api(self,food_name):
        API_URL = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
        headers = {
            'x-app-id': nutrition_x_app_id,
            'x-app-key': nutrition_x_api,
            'Content-Type': 'application/json'
        }

        data = {
            "query": food_name
        }

        response = requests.post(API_URL, headers=headers, json=data)
        nutritions_dict = {}

        if response.status_code == 200:
            nutrition_data = response.json()['foods'][0]

            nutritions_dict['calories'] = str(nutrition_data['nf_calories']) if nutrition_data['nf_calories'] is not None else '0'
            nutritions_dict['total_fat'] = str(nutrition_data['nf_total_fat'])+' gr' if nutrition_data['nf_total_fat'] is not None else '0 gr'
            nutritions_dict['cholesterol'] = str(nutrition_data['nf_cholesterol'])+' mg' if nutrition_data['nf_cholesterol'] is not None else '0 mg'
            nutritions_dict['sodium'] = str(nutrition_data['nf_sodium'])+' mg' if nutrition_data['nf_sodium'] is not None else '0 mg'
            nutritions_dict['total_carbohydrate'] = str(nutrition_data['nf_total_carbohydrate'])+' gr' if nutrition_data['nf_total_carbohydrate'] is not None else '0 gr'
            nutritions_dict['potassium'] = str(nutrition_data['nf_potassium'])+' mg' if nutrition_data['nf_potassium'] is not None else '0 mg'
            nutritions_dict['protein'] = str(nutrition_data['nf_protein'])+' gr' if nutrition_data['nf_protein'] is not None else '0 gr'
            nutritions_dict['sugars'] = str(nutrition_data['nf_sugars']) + ' gr' if nutrition_data['nf_sugars'] is not None else '0 gr'




        return nutritions_dict

        # logger.info(f"[getting info using the api.]")
        #
        # # TODO - uncomment
        # params = {
        #     "q": food_name,
        #     "api_key": api_key
        # }
        # search = GoogleSearch(params)
        # results = search.get_dict()
        # nutrition_information = results["knowledge_graph"]['list']
        # return nutrition_information

