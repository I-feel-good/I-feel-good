import os
import psycopg2
import sqlalchemy
import pandas as pd
import logging as lg
import streamlit_authenticator as stauth

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv(override=True)

lg.info('Connection à la base de donnée')

# SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace('postgres://','postgresql://')
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL1").replace('postgres://','postgresql://')
SQLALCHEMY_TRACK_MODIFICATIONS = False
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Sessions = sessionmaker(bind=engine)
db = Sessions()

Base = declarative_base()

class Users(Base):
    lg.info('Class Users')
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    fonction = Column(String, nullable=False)
    
    
    # def __init__(self, first_name, last_name, username, password, fonction):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.username = username
    #     self.password = password
    #     self.fonction = fonction
        
    # def __repr__(self):
    #     return " l'utilisateur est {} ".format(self.username)

    
    def save_to_db(self):
        lg.info('Class Users save')
        db.add(self)
        db.commit()
        
    def delete_from_db(self):
        lg.info('Class Users delete')
        db.delete(self)
        db.commit()
        
    @classmethod
    def get_list_users_patient(cls):
        lg.info('get_list_users_patient :')
        list_users = sqlalchemy.select([Users.id_user, Users.first_name, Users.last_name, Users.username]).where(Users.fonction == 'patient')
        lg.info(list_users)
        return  list_users
    
    @classmethod
    def get_list_users_patient_(cls):
        lg.info('get_list_users_patient :')
        full_list = db.query(cls).all()
        return full_list
    
    @classmethod
    def get_list_by_user(cls,username):
        lg.info('get_list_users_patient :')
        list_users = sqlalchemy.select([Users.id_user, Users.first_name, Users.last_name,  Users.username, Users.password ]).where(Users.fonction == 'patient',Users.username == username)
        return  list_users
    
    @classmethod
    def get_list_users_docteur(cls):
        lg.info('get_list_users_docteur :')
        list_users = sqlalchemy.select([Users.id_user, Users.first_name, Users.last_name, Users.username,  Users.password,  Users.fonction]).where(Users.fonction == 'docteur')
        return  list_users
      
    @classmethod
    def get_list_users(cls):
        lg.warning('get_list_users : {Users.id}, {Users.first_name}')
        full_list = db.query.join(Users).with_entities(Users.id_user, Users.first_name, Users.last_name, Users.username,  Users.password,  Users.fonction).all()
        return full_list

    @classmethod
    def get_user(cls, Username):#, password
        lg.warning('get_list_users : {Users.id}, {Users.first_name}')
        # password_hash = stauth.Hasher(password).generate()
        user = db.query(Users).filter_by(username=Username).first()#, password=password
        return user

    
    
class Informations(Base):
    lg.info('Class Informations')
    __tablename__ = 'informations'
    id_informations = Column(Integer, primary_key=True)
    dateofcreation = Column(DateTime)
    last_updated = Column(DateTime)
    emotion = Column(String)
    text = Column(String)
    user_id = Column(Integer, ForeignKey('users.id_user'))
    
    # def __init__(self,id_informations, dateofcreation, last_updated, emotion, text, user_id):
    #     self.id_informations = id_informations
    #     self.dateofcreation = dateofcreation
    #     self.last_updated = last_updated
    #     self.emotion = emotion
    #     self.text = text
    #     self.user_id = user_id
        
    # def __repr__(self):
    #     return "L'infomration est".format(self.dateofcreation)
    
    def save_to_db(self):
        lg.info('Class Informations save')
        db.add(self)
        db.commit()
        
    def delete_from_db(self):
        lg.info('Class Informations delete')
        db.delete(self)
        db.commit()
        
    # def supprimer_to_db(self, id):
    #     db.query().filter(Informations.id_informations == i["id_informations"]).one()
    #     db

    @classmethod
    def get_list_une_informations(cls,id):
        lg.info('get_list_une_informations :{} '.format(id))
        full_list = db.query(cls).where(cls.id_informations==id).all()
        print(full_list)
        return full_list
    

    @classmethod
    def get_list_informations(cls):
        lg.info('get_list_informations : {Informations.id_informations}, {Informations.dateofcreation}')
        # full_list = db.query(Users, Informations).join(Informations).first()
        full_list = sqlalchemy.select([Users.first_name,
                                       Users.last_name,
                                       Users.username,
                                       Informations.id_informations,
                                       Informations.dateofcreation,
                                       Informations.last_updated, 
                                       Informations.emotion,
                                       Informations.text
                                     ]).join(Informations)#.filter_by(username=user.username)
        return full_list  


    @classmethod
    def get_list_informations_username(cls, username):
        lg.info(f'get_list_informations : {username}')
        full_list = sqlalchemy.select([Users.id_user, Users.first_name, Users.last_name, Users.username, Users.fonction, Informations.id_informations,
                                           Informations.dateofcreation,Informations.last_updated, Informations.emotion, Informations.text, 
                                           ]).where(Users.id_user == Informations.user_id, Users.username==username)
        return full_list


    @classmethod
    def get_list_informations_by_users(cls, user):
        full_list = sqlalchemy.select([Users.first_name,
                                       Users.last_name,
                                       Users.username,Informations.id_informations,
                                       Informations.dateofcreation,
                                       Informations.last_updated, 
                                       Informations.emotion,
                                       Informations.text
                                     ]).filter_by(username=user.username).join(Informations)
        return full_list

    @classmethod
    def get_list_informations_by_id(cls, id):
        informations = sqlalchemy.select([Informations.id_informations,
                                       Informations.dateofcreation,
                                       Informations.last_updated, 
                                       Informations.emotion,
                                       Informations.text,
                                       Informations.user_id
                                     ]).where(Informations.id_informations==id)
        return informations   
        
# Function to create db and populate it
def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    for i in range(1,11):
        Users(first_name = 'toto' + str(i),last_name='toto' + str(i),username='toto' + str(i), password=123, fonction='patient').save_to_db()
    Users(first_name = 'tata',last_name='tata',username='tata', password=123, fonction='docteur').save_to_db()

    lg.info('Ouverture du fichier CSV Informations')
    df_test = pd.read_csv('static/df_test_kaggle.csv')
    lg.info('Debut enregistrement information')
    df_test.to_sql('informations', con = engine, if_exists='append', index=False)
    lg.info('Database initialized!')
        
if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    init_db()
    lg.info('Base de donnée à été créer')
