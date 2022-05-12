import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import logging as lg
from dotenv import load_dotenv
import os

import streamlit_authenticator as stauth

load_dotenv(override=True)

lg.warning('Connection à la base de donnée')

# SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace('postgres://','postgresql://')
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL1").replace('postgres://','postgresql://')
SQLALCHEMY_TRACK_MODIFICATIONS = False
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Sessions = sessionmaker(bind=engine)
db = Sessions()

Base = declarative_base()


class Users(Base):
    lg.warning('UsersClass Users')
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    fonction = Column(String, nullable=False)
    
    def save_to_db(self):
        lg.warning('Class Users save')
        db.add(self)
        db.commit()
        
    def delete_from_db(self):
        lg.warning('Class Users delete')
        db.delete(self)
        db.commit()
        
    @classmethod
    def get_list_users(cls):
        lg.warning('get_list_users : {Users.id}, {Users.first_name}')
        full_list = db.query.join(Users).with_entities(Users.id, Users.first_name, Users.last_name, Users.username,  Users.password,  Users.fonction).all()
        return full_list

    @classmethod
    def get_user(cls, Username):#, password
        lg.warning('get_list_users : {Users.id}, {Users.first_name}')
        # password_hash = stauth.Hasher(password).generate()
        user = db.query(Users).filter_by(username=Username).first()#, password=password
        return user

    
class Informations(Base):
    # lg.warning('Class Information')
    __tablename__ = 'informations'
    id_informations = Column(Integer, primary_key=True)
    dateofcreation = Column(DateTime)
    last_updated = Column(DateTime)
    emotion = Column(String)
    text = Column(String)
    user_id = Column(Integer, ForeignKey('users.id_user'))
    
    def save_to_db(self):
        lg.warning('Class Informations save')
        db.add(self)
        db.commit()
        
    def delete_from_db(self):
        lg.warning('Class Informations delete')
        db.delete(self)
        db.commit()
        
    @classmethod
    def get_list_informations(cls):
        # lg.warning('get_list_users : {Informations.id_informations}, {Informations.dateofcreation}')
        full_list = sqlalchemy.select([Users.first_name,
                                       Users.last_name,
                                       Users.username,
                                       Informations.dateofcreation,
                                       Informations.last_updated, 
                                       Informations.emotion,
                                       Informations.text
                                     ])
        return full_list
        
    @classmethod
    def get_list_informations_by_users(cls, user):
        full_list = sqlalchemy.select([Users.first_name,
                                       Users.last_name,
                                       Users.username,
                                       Informations.dateofcreation,
                                       Informations.last_updated, 
                                       Informations.emotion,
                                       Informations.text
                                     ]).filter_by(username=user.username)
        return full_list    
        
        
if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)