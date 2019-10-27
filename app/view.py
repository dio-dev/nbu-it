import pymysql
from config import mysql
from app import app,api
from flask import jsonify
from flask_restful import Resource



class BankWatchYou(Resource):
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

