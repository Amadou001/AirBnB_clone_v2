#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
import models
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", back_populates="state",
                              cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            from models.city import City
            """
            returns the list of City instances with state_id
            equals to the currentState.id => It will be the
            FileStorage relationship between State and City
            """
            return [city for city in models.storage.all(City).values()
                    if City.state_id == self.id]
