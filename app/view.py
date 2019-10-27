import pymysql
from config import mysql
from app import app,api
from flask import jsonify, make_response
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'qwerty':
        return 'qwerty'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

class BankWatchYou(Resource):
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

api.add_resource(BankWatchYou, '/')

if __name__ == "__main__":
    app.run()

