import googlemaps
import requests, json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
import urllib.parse

import os
api_key = os.getenv("API_KEY_GOOGLE")


class Google_finder:

    def get_address_by_location(self, lat, lng):
        """
        :param lat:
        :param lng:
        :return: {'street_number': street_number, 'street_name': street_name, 'city': city, 'index':index}
        """
        url ="https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lat)+","+str(lng)+"&key="+api_key
        r = requests.get(url + '&key=' + api_key)
        x = r.json()
        y = x['results']
        street_number = x['results'][0]['address_components'][0]['long_name']
        street_name = x['results'][0]['address_components'][1]['long_name']
        city = x['results'][0]['address_components'][2]['long_name']
        index = x['results'][0]['address_components'][6]['long_name']
        result = {'street_number': street_number, 'street_name': street_name, 'city': city, 'index':index}

        return result

    def find_location(self, my_lat, my_lng, place_type='bank', place_name=None):
        """
        find_location of places near you
        :param query: places what you want to find
        :return: {'Name': name, 'Address': address, 'Status': status, "Distanse": distanse, 'lat': lat, 'lng': lng}
        """
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

        if place_name == None:
            place_name = ""
        query = urllib.parse.quote(f"{str(place_type)+str(place_name)}")

        r = requests.get(url + 'query=' + query + f"&location={my_lat},{my_lng}&language=ru" + '&key=' + api_key)
        x = r.json()
        y = x['results']

        result = []
        for i in range(len(y)):
            name = 'Name : ' + y[i]['name']
            address = 'Адресс : ' + y[i]['formatted_address']

            if 'opening_hours' in y[i].keys():
                status = y[i]['opening_hours']['open_now']

                if status == True:
                    door = "open"
                else:
                    door = "close"
                status = "Status : " + door

            lat = y[i]['geometry']['location']['lat']
            lng = y[i]['geometry']['location']['lng']

            distanse = "Дистанция : " + self.culc_distances([str(my_lat), str(my_lng)], [lat, lng])

            res_dic = {'Name': name, 'Address': address, 'Status': status, "Distanse": distanse, 'lat': lat, 'lng': lng}
            result.append(res_dic)

        return result


    def culc_distances(self, my_loc, place_loc):
        """
        :param my_loc: list of two coordinates
        :param place_loc: list of two coordinates
        :return: distanse in str
        """
        myloc ="{},{}".format(my_loc[0], my_loc[1])
        placeloc = "{},{}".format(place_loc[0], place_loc[1])
        gmaps = googlemaps.Client(key=api_key)
        now = datetime.now()
        direction_result = gmaps.directions(myloc,
                                            placeloc,
                                            mode="driving",
                                            avoid="ferries",
                                            departure_time=now
                                            )
        mi = direction_result[0]['legs'][0]['distance']['text']
        # for miles
        # to_km = mi.split(' ')
        # if to_km[1] == 'mi':
        #     km = round(float(to_km[0].replace(',','.')) * 1.60934,2)
        #     result = km + 'km'
        # result = km + 'm'
        result = mi

        return result
