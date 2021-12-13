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

        import requests
        auth_token = 'NgF35-znpIaEKTTtAlOqdtY_iBoXM7XnRo2qaYY1uXlyCga7-hltIEGO-qtUsdzAS8ks8VXUBUsU-a22Tqc4Dn3LmOkp0smZH-sTzSFovpYr-xnLeCfshtwM2yC2YXYx'
        hed = {'Authorization': 'Bearer ' + auth_token}

        # data = '{"location": "paris", "term": "restaurant"}'

        import json

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
        
        restrnts = '\n '.join(str(data['businesses'].index(e))+" "+str(e['name']) for e in data['businesses'])
        dispatcher.utter_message(text=restrnts)

        return []


class ActionGetItinerary(Action):

    def name(self) -> Text:
        return "action_get_itinerary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import requests

        QrCodeApi = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="

        depart = "339 Chem. des Meinajaries, 84000 Avignon"
        arrivee = "2 Impasse de l'Epi, 84000 Avignon"
        GoogleMapsItinerary = "https://www.google.fr/maps/dir/"+depart+"/"+arrivee+"/"

        CompletQrCodeLink = QrCodeApi+GoogleMapsItinerary
        import json

        response = requests.get(CompletQrCodeLink)
        print(response)
        # print(response.json())

        # data = response.json()

        # print(data)
        # for res in data['businesses']:
        #  print(res['name'])

        # dispatcher.utter_message(text=data, image = image)
        dispatcher.utter_message(text="got this link : "+CompletQrCodeLink)

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
