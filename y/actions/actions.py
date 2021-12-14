# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher



places_db = {}


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
        

        # fill db places :
        for e in data['businesses']:
         places_db[str(data['businesses'].index(e))] = str(e['name'])
        
        # group all businesses_places in one String
        businesses_places = '\n '.join(str(data['businesses'].index(e))+" - "+str(e['name']) for e in data['businesses'])
        businesses_places = "here are the restaurants around \n "+businesses_places
        dispatcher.utter_message(text=businesses_places)
        # return [SlotSet("businesses_places", businesses_places)]
        return []


#  Deprecated
class ActionGetItinerary(Action):

    def name(self) -> Text:
        return "action_get_itinerary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import requests

        QrCodeApi = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="

        default_starting_place_ceri = "339 Chem. des Meinajaries, 84000 Avignon"

        destination_place = next(tracker.get_latest_entity_values("businesses_places"), None)

        if not destination_place :
            msg = "Can you give me your destination ?"
            dispatcher.utter_message(text=msg)
            return []

        msg = f"Your destination is {destination_place}"
        dispatcher.utter_message(text=msg)

        destination = "2 Impasse de l'Epi, 84000 Avignon"
        GoogleMapsItinerary = "https://www.google.fr/maps/dir/" + default_starting_place_ceri+"/"+destination+"/"

        CompletQrCodeLink = QrCodeApi+GoogleMapsItinerary
        import json

        response = requests.get(CompletQrCodeLink)
        # print(response)

        # download image
        # img_data = requests.get(CompletQrCodeLink).content

        # with open('QRCode.jpg', 'wb') as handler:
        #     handler.write(img_data)

        # print(response.json())
        # data = response.json()
        # print(data)
        # for res in data['businesses']:
        #  print(res['name'])
        # dispatcher.utter_message(text=data, image = image)

        # utter_message(image=<image url>)

        # msg = f"find the itinerary from this link {response} or scan this QR Code"
        dispatcher.utter_message(text=msg)
        dispatcher.utter_message(image=response)

        return []


class ActionGetItineraryFromIndex(Action):

    def name(self) -> Text:
        return "action_get_itinerary_from_index"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import requests

        QrCodeApi = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="

        # Ceri Adress
        default_starting_place_ceri = "339 Chem. des Meinajaries, 84000 Avignon"

        destination_place_index = next(
            tracker.get_latest_entity_values("businesses_places_index"), None)

        if not destination_place_index:
            msg = "Can you give me your destination index ?"
            dispatcher.utter_message(text=msg)
            return []

        name_of_place = places_db.get(destination_place_index, None)
        if not destination_place_index:
            msg = f"I didnt recognize {name_of_place} .is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []

        msg = f"Your destination is to the restaurant : {name_of_place}"
        # dispatcher.utter_message(text=msg)
        # return []

        # destination = "2 Impasse de l'Epi, 84000 Avignon"
        default_city_destination = "84000 Avignon, France"
        GoogleMapsItinerary = "https://www.google.fr/maps/dir/" + default_starting_place_ceri+"/"+str(name_of_place)+" "+default_city_destination+"/"

        CompletQrCodeLink = QrCodeApi+GoogleMapsItinerary
        # import json
        response = requests.get(CompletQrCodeLink)
        # print(response)
        # print(response.json())
        # data = response.json()
        # print(data)
        # for res in data['businesses']:
        #  print(res['name'])
        # dispatcher.utter_message(text=data, image = image)

        # utter_message(image=<image url>)
        msg = msg + " \n " + "find the itinerary from [this link]("+CompletQrCodeLink+") or scan this QR Code"
        dispatcher.utter_message(text=msg)
        # dispatcher.utter_image_url(image=response)
        # dispatcher.utter_message(image=response)

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
