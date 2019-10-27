import pymysql
from config import mysql
from app import app,api
from flask import request
from flask import jsonify, make_response
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
import googlemaps
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

import os
api_key = os.getenv("API_KEY_GOOGLE")

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'qwerty':
        return 'qwerty'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

class GetAll(Resource):
    @auth.login_required
    def get(self):
        try:
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute('select * from NBU;')
            rows = cur.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

def culc_distances(my_loc, place_loc):
    """
    :param my_loc: list of two coordinates
    :param place_loc: list of two coordinates
    :return: distanse in str
    """
    myloc = "{},{}".format(my_loc[0], my_loc[1])
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


class CalcDistances(Resource):
    """
    http://127.0.0.1:5000/dist?type=bank&name=privatbank&lat=50.4052484&lng=30.36977
    """
    @auth.login_required
    def get(self):
        try:
            place_type = request.args.get('type', default='bank', type=str)
            place_name = request.args.get('name', default= None, type=str)
            my_lat = request.args.get('lat', default=None, type=float)
            my_lng = request.args.get('lng', default=None, type=float)

            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            if place_name == None:
                sql = 'select * from NBU where type = ' + "'" + place_type + "'"
            else:
                sql = 'select * from NBU where type = ' + "'" + place_type + "'" + ' and name = ' + "'" + place_name + "'"

            cur.execute(sql)
            rows = cur.fetchall()

            distances = []
            for item in rows:
                id = item['id']
                latitude = item['gps_latitude']
                longitude = item['gps_longitude']
                res = culc_distances([ my_lat, my_lng ], [longitude, latitude])
                res = res.split(" ")

                distances.append({'id':id, 'distance':res[0]})

            def get_dict(dictionary):
                res = dictionary['distance'].split(' ')
                return res[0]

            distances = sorted(distances, key=get_dict)

            list_id = []
            for item in distances:
                list_id.append(item['id'])
            list_id = ', '.join(str(e) for e in list_id)
            sql = 'select * from NBU where id in ' + "(" + list_id + ")"
            cur.execute(sql)
            rows = cur.fetchall()
            for i in distances:
                for j in rows:
                    if i['id'] == j['id']:
                        j['distance'] = i['distance']

            rows = sorted(rows, key=get_dict)
            return rows



        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

#http://127.0.0.1:5000/dist/0/0/bank

api.add_resource(GetAll, '/')
api.add_resource(CalcDistances, '/dist')

if __name__ == "__main__":
    app.run()

