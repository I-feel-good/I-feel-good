import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import os
import psycopg2
from dotenv import load_dotenv
import warnings as lg
load_dotenv(override=True)

# Database initialization
# lg('Connection à la base de donnée')
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace('postgres://','postgresql://')
SQLALCHEMY_TRACK_MODIFICATIONS = False

Base = declarative_base()

class UserInput(Base):
    # lg('Class Users')
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    password = Column(String)
    fonction = Column(String)
    
    
class Information(Base):
    # lg('Class Information')
    __tablename__ = 'informations'
    id_informations = Column(Integer, primary_key=True)
    dateofcreation = Column(DateTime)
    last_updated = Column(DateTime)
    text_informations = Column(String)
    user_id = Column(Integer, ForeignKey('users.id_user'))
        
if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)