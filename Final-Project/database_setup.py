import os
import sys
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250))
    password = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'email':self.email,
            'password':self.password,
            'id': self.id,
        }


class Events(Base):
    __tablename__ = 'events'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    category = Column(String(250))
    fee = Column(String(8))
    date = Column(Date)
    time = Column(Time)
    register_id = Column(Integer, ForeignKey('users.id'))
    users = relationship(Users)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'date': self.date,
            'time': self.time,
            'id': self.id,
        }


engine = create_engine('sqlite:///handler.db')


Base.metadata.create_all(engine)
