# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionCheckRestaurants(Action):

    def name(self) -> Text:
        return "action_check_restaurants"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="all the restaurants : r1, r2!")

        import requests
        auth_token = 'NgF35-znpIaEKTTtAlOqdtY_iBoXM7XnRo2qaYY1uXlyCga7-hltIEGO-qtUsdzAS8ks8VXUBUsU-a22Tqc4Dn3LmOkp0smZH-sTzSFovpYr-xnLeCfshtwM2yC2YXYx'
        hed = {'Authorization': 'Bearer ' + auth_token}

        # data = '{"location": "paris", "term": "restaurant"}'

        import json

        data = {}
        data['location'] = 'paris'
        data['term'] = 'restaurant'
        json_data = json.dumps(data)

        url = 'https://api.yelp.com/v3/businesses/search'
     
        response = requests.get(url, params=json.loads(json_data), headers=hed)
        print(response)
        print(response.json())

        return []
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
