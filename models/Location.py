from sqlalchemy import Column, String, Integer
from base import Base


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    region = Column('region', String(32))
    city = Column('city', String(32))
    street = Column('street', String(32))
    building_number = Column('building_number', String(32))
    adress_index = Column('adress_index', String(32))

    def __init__(self, region, city, street, building_number, adress_index):
        self.region = region
        self.city = city
        self.street = street
        self.building_number = building_number
        self.adress_index = adress_index