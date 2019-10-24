import pymysql.cursors
import sys

############################################################################################################

def read(type):
    connection = pymysql.connect(host='dio-tech.top',
                             user='qwerty_team',
                             password='12345678',
                             db='hackathon',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "SELECT `gps.longitude`, `gps.latitude` FROM `NBU` WHERE `type` = %s"
            cursor.execute(sql, (type))
            result = cursor.fetchone()
            print(result)
            connection.commit()
    except Exception:
        print(sys.exc_info())

    connection.close()

