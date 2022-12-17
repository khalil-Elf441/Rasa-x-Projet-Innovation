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
        # dispatcher.utter_message(text=msg)
        # dispatcher.utter_image_url(image=response)
        # dispatcher.utter_message(image=CompletQrCodeLink)

        return []


# action_get_restaurant_from_index

class ActionGetRestaurantFromIndex(Action):

    def name(self) -> Text:
        return "action_get_restaurant_from_index"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        destination_place_index = next(tracker.get_latest_entity_values("businesses_places_index"), None)

        if not destination_place_index:
            msg = "Can you give me your destination index ?"
            dispatcher.utter_message(text=msg)
            return []

        name_of_place = places_db.get(destination_place_index, None)
        if not destination_place_index:
            msg = f"I didnt recognize {name_of_place} .Can you try again ?"
            dispatcher.utter_message(text=msg)
            return []

        msg = f"Is your destination the restaurant : {name_of_place}?"
        dispatcher.utter_message(text=msg)

        return []


class ActionGetCategoriesFromTerm(Action):

    def name(self) -> Text:
        return "action_propose_term_categories"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # auth_token = 'NgF35-znpIaEKTTtAlOqdtY_iBoXM7XnRo2qaYY1uXlyCga7-hltIEGO-qtUsdzAS8ks8VXUBUsU-a22Tqc4Dn3LmOkp0smZH-sTzSFovpYr-xnLeCfshtwM2yC2YXYx'
        # head = {'Authorization': 'Bearer ' + auth_token}

        user_term = next(tracker.get_latest_entity_values("term"), None)     
        categories = []
        # Get categories
        url_categories = 'https://www.yelp.com/developers/documentation/v3/all_category_list/categories.json'
        response = requests.get(url_categories)
        categories_json_fetch = response.json()

        # get categories
        for element in categories_json_fetch:
            for parent_term in element["parents"]:
                if parent_term == user_term:
                    categories.append(element['alias'])
        #  print(response)
        # pprint.pprint(response.json())

        # categories = "test"
        # print(response.json())
        # data = response.json()
        categories_as_string = ' or '.join(list(set(str(e) for e in categories))[:5])

        # print(categories)
        msg = f"which fron the {user_term} s categories you prefer {categories_as_string} ?"
        dispatcher.utter_message(text=msg)
        # , SlotSet("Key2", "Value2")

        # for key in slot_keys_values.keys():
        #     slot = SlotSet(key, slot_keys_values[key])
        #     slots.append(slot)
        # return slots
        # , SlotSet("term", user_term)
        return [SlotSet("term_categories", categories)]


class ActionGetUserCategoryChoice(Action):

    def name(self) -> Text:
        return "action_get_user_category_choice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # user_category_choice = next(tracker.get_slot("category"), None)
        user_category_choice = next(tracker.get_latest_entity_values("category"), None)

        print(user_category_choice)

        List_categories = tracker.get_slot("term_categories")

        print(List_categories)

        if not user_category_choice:
            msg = f"I didnt recognize {user_category_choice}. Can you try again ?"
            dispatcher.utter_message(text=msg)
            return[]

        if user_category_choice in List_categories:
            # msg = f"Okey I will remenber your category {user_category_choice} !, Do want it open now now or at specific time ?"
            saved_term = tracker.get_slot("term")

            auth_token = 'NgF35-znpIaEKTTtAlOqdtY_iBoXM7XnRo2qaYY1uXlyCga7-hltIEGO-qtUsdzAS8ks8VXUBUsU-a22Tqc4Dn3LmOkp0smZH-sTzSFovpYr-xnLeCfshtwM2yC2YXYx'
            head = {'Authorization': 'Bearer ' + auth_token}

            # data = '{"location": "paris", "term": "restaurant"}'

            data = {}
            data['location'] = 'avignon'
            data['term'] = saved_term

            # print(saved_term)

            data['categories'] = user_category_choice

            json_data = json.dumps(data)

            response = requests.get(YELP_BUSSINESS_SEARCH_LINK, params=json.loads(json_data), headers=head)
        #  print(response)
        #  print(response.json())
            data = response.json()

            print(data)
            
            businesses_places = ' '.join(
                list(set(str(e['name']) for e in data['businesses']))[:5])

            print(businesses_places)

            msg = f"Here is the {saved_term} with this category {businesses_places}"
            dispatcher.utter_message(text=msg)
            return [SlotSet("term_category", user_category_choice)]        
        



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
