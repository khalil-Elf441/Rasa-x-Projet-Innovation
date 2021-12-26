# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
import pprint

places_db = {}

YELP_BUSSINESS_SEARCH_LINK = 'https://api.yelp.com/v3/businesses/search'
YELP_BUSSINESS_DETAILS_LINK = "https://api.yelp.com/v3/businesses/"

class ActionCheckRestaurants(Action):

    def name(self) -> Text:
        return "action_check_restaurants"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        auth_token = 'NgF35-znpIaEKTTtAlOqdtY_iBoXM7XnRo2qaYY1uXlyCga7-hltIEGO-qtUsdzAS8ks8VXUBUsU-a22Tqc4Dn3LmOkp0smZH-sTzSFovpYr-xnLeCfshtwM2yC2YXYx'
        hed = {'Authorization': 'Bearer ' + auth_token}

        # data = '{"location": "paris", "term": "restaurant"}'



        data = {}
        data['location'] = 'avignon'
        data['term'] = 'restaurant'
        json_data = json.dumps(data)

        url = 'https://api.yelp.com/v3/businesses/search'
     
        response = requests.get(url, params=json.loads(json_data), headers=hed)
        #  print(response)
        #  print(response.json())

        data = response.json()
        # for res in data['businesses']:
        #  print(res['name'])
        

        # fill db places :
        for e in data['businesses']:
         places_db[str(data['businesses'].index(e))] = str(e['name'])
        
        # # return only one restaurant ####### Last robot test
        # dispatcher.utter_message(text="the restaurant is "+data['businesses'][0]['name'])
        # return []

        # group all businesses_places in one String
        # businesses_places = '\n '.join(str(data['businesses'].index(e))+" - "+str(e['name']) for e in data['businesses'])

        businesses_places = ' '.join(str(data['businesses'].index(e))+" "+str(e['name']) for e in data['businesses'])

        businesses_places = "here are the restaurants around \n "+businesses_places
        dispatcher.utter_message(text=businesses_places)
        # return [SlotSet("businesses_places", businesses_places)]
        return []


t