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

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace('postgres://','postgresql://')
SQLALCHEMY_TRACK_MODIFICATIONS = False


Base = declarative_base()


class Users(Base):
    lg.warning('UsersClass Users')
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    username = Column(String)
    password = Column(String)
    fonction = Column(String)

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
        full_list = cls.query.join(Users).with_entities(Users.id, Users.first_name, Users.last_name, Users.username,  Users.password,  Users.fonction).all()
        return full_list

    @classmethod
    def get_user(cls, Username, password):
        lg.warning('get_list_users : {Users.id}, {Users.first_name}')
        password_hash = stauth.Hasher(password).generate()
        user = cls.query.filter_by(username=Username, password=password_hash).first()
        return user
    
class Informations(Base):
    # lg.warning('Class Information')
    __tablename__ = 'informations'
    id_informations = Column(Integer, primary_key=True)
    dateofcreation = Column(DateTime)
    last_updated = Column(DateTime)
    text_informations = Column(String)
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
        lg.warning('get_list_users : {Informations.id_informations}, {Informations.dateofcreation}')
        full_list = cls.query.join(Users).with_entities(Informations.id_informations, Informations.dateofcreation, 
                                                        Informations.last_updated, Informations.text_informations,  
                                                        Informations.user_id).all()
        return full_list
        
    @classmethod
    def get_list_informations_by_users(cls):
        full_list = cls.query.join(Users).with_entities(Informations.id_informations, Informations.dateofcreation, 
                                                        Informations.last_updated, Informations.text_informations,  
                                                        Informations.user_id).all()
        return full_list    
        
        
if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)