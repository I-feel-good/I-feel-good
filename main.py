from model import *
import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from streamlit_option_menu import option_menu



engine = create_engine(SQLALCHEMY_DATABASE_URI)
Sessions = sessionmaker(bind=engine)
sess = Sessions()

with st.sidebar:
    connected = False
    if connected:
        print(connected)
        selected = option_menu("Main Menu", ["Home", "Patient", "Information", 'Settings'], icons=['house', '', 'card-text','gear'], menu_icon="cast", default_index=1)
    else:
        print("not connected")
        selected = option_menu("Main Menu", ["Home","Sign-in", "Sign-up"], icons=['house', "person", "pen"], menu_icon="cast", default_index=1)

if selected == 'Home':
    st.title('coucou home')
    st.balloons()
    
elif (selected == 'Patient') & (connected==True):
    st.title('coucou Patient')
    
    
elif (selected == 'Information') & (connected==True):
    st.title('coucou Information')
    
elif (selected == 'Sign-in') & (connected==False):
    st.title("Vous n'etes pas connecté bande de batard")
    
elif (selected == 'Sign-up') & (connected==False):
    st.title("Enregistrer tete d'alien")