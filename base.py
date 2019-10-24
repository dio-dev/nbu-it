from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db
from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
engine = db.create_engine('mysql+pymysql://{0}:{1}@{2}:3306/{3}'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB))
Session = sessionmaker(bind=engine)
Base = declarative_base()