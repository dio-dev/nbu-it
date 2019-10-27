from app import app
from flaskext.mysql import MySQL
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'worker'
app.config['MYSQL_DATABASE_PASSWORD'] = 'TXWs^18#Nd17'
app.config['MYSQL_DATABASE_DB'] = 'hackathon'
app.config['MYSQL_DATABASE_HOST'] = '176.36.240.68'
mysql.init_app(app)