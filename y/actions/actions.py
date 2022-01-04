# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
import pprint
import requests




YELP_BUSSINESS_SEARCH_LINK = 'https://api.yelp.com/v3/businesses/search'
YELP_BUSSINESS_DETAILS_LINK = "https://api.yelp.com/v3/businesses/"
QrCodeApi = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="

# temp place db / Deprecated
places_db = {}

# First implemented version of YELP
class ActionCheckRestaurants(Action):

    def name(self) -> Text:
        return "action_check_restaurants"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Send reauest to YELP
        auth_token = 'NgF35-znpIaEKTTtAlOqdtY_iBoXM7XnRo2qaYY1uXlyCga7-hltIEGO-qtUsdzAS8ks8VXUBUsU-a22Tqc4Dn3LmOkp0smZH-sTzSFovpYr-xnLeCfshtwM2yC2YXYx'
        hed = {'Authorization': 'Bearer ' + auth_token}

        data = {}
        data['location'] = 'avignon'
        data['term'] = 'restaurant'
        json_data = json.dumps(data)

        url = 'https://api.yelp.com/v3/businesses/search'
     
        response = requests.get(url, params=json.loads(json_data), headers=hed)

        data = response.json()

        # fill db places :
        for e in data['businesses']:
         places_db[str(data['businesses'].index(e))] = str(e['name'])

        businesses_places = ' '.join(str(data['businesses'].index(e))+" "+str(e['name']) for e in data['businesses'])

        businesses_places = "here are the restaurants around \n "+businesses_places
        dispatcher.utter_message(text=businesses_places)
        return []


#  Deprecated version of get Itenerary
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

        dispatcher.utter_message(text=msg)
        dispatcher.utter_message(image=response)

        return []



# Get the Itinerary from index / first version 
class ActionGetItineraryFromIndex(Action):

    def name(self) -> Text:
        return "action_get_itinerary_from_index"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        # QRCODE QPI
        QrCodeApi = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="

        # Ceri Adress by default
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
        default_city_destination = "84000 Avignon, France"
        GoogleMapsItinerary = "https://www.google.fr/maps/dir/" + default_starting_place_ceri+"/"+str(name_of_place)+" "+default_city_destination+"/"

        CompletQrCodeLink = QrCodeApi+GoogleMapsItinerary
        response = requests.get(CompletQrCodeLink)

        # display CodeQR as link
        # utter_message(image=<image url>)
        msg = msg + " \n " + "find the itinerary from [this link]("+CompletQrCodeLink+") or scan this QR Code"
        dispatcher.utter_message(text=msg)
        # dispatcher.utter_message(text=msg)
        # dispatcher.utter_image_url(image=response)
        # dispatcher.utter_message(image=CompletQrCodeLink)
        return []


# get restaunrants from index / deprecated / restaurants as changed by term to have many options 
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


# list of possible term choices / sync with nlu
parents = ['restaurants','hotels','cafe','bars']

# Propose categories based on the user term
class ActionGetCategoriesFromTerm(Action):

    def name(self) -> Text:
        return "action_propose_term_categories"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the term
        user_term = next(tracker.get_latest_entity_values("term"), None)     
        categories = []

        # Get categories Static Approch
        # url_categories = 'https://www.yelp.com/developers/documentation/v3/all_category_list/categories.json'
        # response = requests.get(url_categories)
        # categories_json_fetch = response.json()

        # # get categories
        # for element in categories_json_fetch:
        #     for parent_term in element["parents"]:
        #         if parent_term == user_term:
        #             categories.append(element['alias'])
        

        #  get categories from neraby approch
        auth_token = 'NgF35-znpIaEKTTtAlOqdtY_iBoXM7XnRo2qaYY1uXlyCga7-hltIEGO-qtUsdzAS8ks8VXUBUsU-a22Tqc4Dn3LmOkp0smZH-sTzSFovpYr-xnLeCfshtwM2yC2YXYx'
        head = {'Authorization': 'Bearer ' + auth_token}

        data = {}
        data['location'] = 'avignon'
        data['term'] = user_term
      
        json_data = json.dumps(data)
        response = requests.get(YELP_BUSSINESS_SEARCH_LINK, params=json.loads(json_data), headers=head)
        data = response.json()

        for term in data['businesses']:
            for term_categories_res in term["categories"]:
                if term_categories_res not in parents:
                    # get the alias / the name of the term in YELP API
                    categories.append(term_categories_res['alias'])
        
        categories = list(set(categories))

        # group all the categories options in one String
        categories_as_string = ' or '.join(
            list(
                set(
                    str(e) for e in categories
                    )
            )[:5]
            )

        msg = f"which fron the {user_term} s categories you prefer {categories_as_string} ?"
        dispatcher.utter_message(text=msg)
        return [SlotSet("term_categories", categories)]

# temp bussness places / Deprecated
businesses_places_global = []

# EXtract the category and propose it to the user
class ActionGetUserCategoryChoice(Action):

    def name(self) -> Text:
        return "action_get_user_category_choice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # user_category_choice = next(tracker.get_slot("category"), None)
        user_category_choice = next(tracker.get_latest_entity_values("category"), None)

        # print(user_category_choice)

        List_categories = tracker.get_slot("term_categories")

        # print(List_categories)

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
            data['categories'] = user_category_choice

            print("request")
            print(data)

            json_data = json.dumps(data)

            response = requests.get(YELP_BUSSINESS_SEARCH_LINK, params=json.loads(json_data), headers=head)
        #  print(response)
        #  print(response.json())
            data = response.json()

            print(data)
            
            businesses_places = []
            # businesses_places_global = []
            
            index = 0
            for place in data['businesses']:
                index = index + 1
                place_entry = str(index)+" "+str(place['name'])
                businesses_places.append(place_entry)
                businesses_places_global.append(
                    str(index)+" "+str(place['id']))
            
            businesses_places_as_string = ' '.join(businesses_places[:5])
            # businesses_places_global = businesses_places

            print(businesses_places_as_string)

            # propose catogies to the user
            msg = f"Here is the {saved_term} with this category {businesses_places_as_string} What term's number will you choose? "
            dispatcher.utter_message(text=msg)
            return [SlotSet("term_category", user_category_choice)]    

# temp varible to store the place details
target_term_data_details = ""

# Extract the the user term choice / the term is a name exemple hotel ibis
class ActionPointTerm(Action):

    def name(self) -> Text:
        return "action_point_term"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        term_index = next(tracker.get_latest_entity_values("term_index"), None)

        print(f" The term index 1 : {term_index}")

        if not term_index:
            msg = "I couldn't recognise the term index can you try again ?"
            dispatcher.utter_message(text=msg)
            return[]

        # concertion index from name to number
        if term_index == "one":
            term_index = "1"
        
        if term_index == "two":
            term_index = "2"
        
        if term_index == "three":
            term_index = "3"

        if term_index == "four":
            term_index = "4"
        
        if term_index == "five":
            term_index = "5"
        
        print(f" The term index 2 : {term_index}")


        targetId = ""
        data = ""
        # find the id of the term chose by user
        if businesses_places_global:
            print(businesses_places_global)
            for indexId in businesses_places_global:
                index,id = indexId.split()
                print(f"index {index} , id {id}")
                if index == term_index:
                    targetId = id
                    break
            
            # print(f"target Id {targetId}")

            # launch get request to the endpoint bussiness id
            auth_token = 'NgF35-znpIaEKTTtAlOqdtY_iBoXM7XnRo2qaYY1uXlyCga7-hltIEGO-qtUsdzAS8ks8VXUBUsU-a22Tqc4Dn3LmOkp0smZH-sTzSFovpYr-xnLeCfshtwM2yC2YXYx'
            head = {'Authorization': 'Bearer ' + auth_token}
            term_details_ylp_link = YELP_BUSSINESS_DETAILS_LINK + targetId
            response = requests.get(term_details_ylp_link, headers=head)
            target_term_data_details = response.json()
            data = response.json()

            # print("--> target_term_data_details")
            # print(target_term_data_details)

        msg = "Now that I know your favorite restaurant I can give you more informations"
        dispatcher.utter_message(text=msg)
        # set the hotel id to have many details in the previous actions from YELP BUSSINESS DETAILS
        return [SlotSet("target_term_id", data["id"])]

# give the user the contact information of the term 
class ActionGetContact(Action):

    def name(self) -> Text:
        return "action_get_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # print("target_term_data_details <--")
        # print(target_term_data_details)

        requested_term_id = tracker.get_slot("target_term_id")

        # print(requested_term_id)

        if requested_term_id is not None:
            auth_token = 'NgF35-znpIaEKTTtAlOqdtY_iBoXM7XnRo2qaYY1uXlyCga7-hltIEGO-qtUsdzAS8ks8VXUBUsU-a22Tqc4Dn3LmOkp0smZH-sTzSFovpYr-xnLeCfshtwM2yC2YXYx'
            head = {'Authorization': 'Bearer ' + auth_token}
            term_details_ylp_link = YELP_BUSSINESS_DETAILS_LINK + requested_term_id
            response = requests.get(term_details_ylp_link, headers=head)
            data = response.json()
            phone = data["phone"]
            msg = f"You can contact at {phone}"
            dispatcher.utter_message(text=msg)
            return []

        if target_term_data_details:
            phone = target_term_data_details["phone"]
            msg = f"You can contact at {phone}"
            dispatcher.utter_message(text=msg)
            return []

        dispatcher.utter_message(text="ups you should answer some questions before coming to this information")
        return []

#  give the user the term rating from ! to 5 starts depends on yelp DataBase
class ActionGetRating(Action):

    def name(self) -> Text:
        return "action_get_rating"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("target_term_data_details <--")
        print(target_term_data_details)

        requested_term_id = tracker.get_slot("target_term_id")

        print(requested_term_id)

        if requested_term_id is not None:
            auth_token = 'NgF35-znpIaEKTTtAlOqdtY_iBoXM7XnRo2qaYY1uXlyCga7-hltIEGO-qtUsdzAS8ks8VXUBUsU-a22Tqc4Dn3LmOkp0smZH-sTzSFovpYr-xnLeCfshtwM2yC2YXYx'
            head = {'Authorization': 'Bearer ' + auth_token}
            term_details_ylp_link = YELP_BUSSINESS_DETAILS_LINK + requested_term_id
            response = requests.get(term_details_ylp_link, headers=head)
            data = response.json()
            rating = data["rating"]
            msg = f"The rating is {rating}"
            dispatcher.utter_message(text=msg)
            return []

        dispatcher.utter_message(
            text="ups you should answer some questions before coming to this information")
        return []

# genere QrCode itinerary to the place
class ActionGetItineraryFromIndex(Action):

    def name(self) -> Text:
        return "action_get_itinerary_term"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Ceri Adress
        default_starting_place_ceri = "339 Chem. des Meinajaries, 84000 Avignon"
        # term ID
        requested_term_id = tracker.get_slot("target_term_id")

        if not requested_term_id:
            msg = "ups I forget your destination"
            dispatcher.utter_message(text=msg)
            return []
        
        #  launch request for the term DEtails
        auth_token = 'NgF35-znpIaEKTTtAlOqdtY_iBoXM7XnRo2qaYY1uXlyCga7-hltIEGO-qtUsdzAS8ks8VXUBUsU-a22Tqc4Dn3LmOkp0smZH-sTzSFovpYr-xnLeCfshtwM2yC2YXYx'
        head = {'Authorization': 'Bearer ' + auth_token}
        term_details_ylp_link = YELP_BUSSINESS_DETAILS_LINK + requested_term_id
        response = requests.get(term_details_ylp_link, headers=head)
        data = response.json()
        name_of_place = data["name"]

        # print(name_of_place)

        msg = f"Your destination is to the restaurant : {name_of_place}"

        place_adress = data["location"]["address1"]
        # dispatcher.utter_message(text=msg)
        # return []

        # print("Place Adress "+place_adress)

        # destination = "2 Impasse de l'Epi, 84000 Avignon"
        default_city_destination = " 84000 Avignon, France"
        
        #  generate the itinerary based on google maps 
        GoogleMapsItinerary = "https://www.google.fr/maps/dir/" + \
            default_starting_place_ceri+"/" + \
            str(place_adress)+" "+default_city_destination+"/"

        CompletQrCodeLink = QrCodeApi+GoogleMapsItinerary
        response = requests.get(CompletQrCodeLink)

        # give the destination with Qrcode link
        # utter_message(image=<image url>)
        msg = msg + " \n " + "find the itinerary from [this link]("+CompletQrCodeLink+") or scan this QR Code"
        dispatcher.utter_message(text=msg)

        return []

# default example
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
