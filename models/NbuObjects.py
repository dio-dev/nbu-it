from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from base import Base


class NbuObject(Base):
    __tablename__ = 'nbu'
    id = Column(Integer, primary_key=True)
    type = Column('type', String(32))
    name = Column('name', String(32))
    adress_id = Column(Integer, ForeignKey('locations.id'))
    address = relationship("Location", backref="nbu")
    gps_longitude = Column('gps_longitude', String(32))
    gps_latitude = Column('gps_latitude', String(32))
    open_hours = Column('open_hours', String(32))
    open_days = Column('open_days', String(32))