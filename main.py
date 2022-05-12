from model import *
import streamlit as st
import streamlit_authenticator as stauth
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from streamlit_option_menu import option_menu
import logging as lg
from dotenv import load_dotenv
import os
from st_aggrid import AgGrid
import pandas as pd
from st_aggrid.grid_options_builder import GridOptionsBuilder
load_dotenv(override=True)

# Database initialization
# lg.info('Connection à la base de donnée')
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL1").replace('postgres://','postgresql://')
SQLALCHEMY_TRACK_MODIFICATIONS = False
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Sessions = sessionmaker(bind=engine)
db = Sessions()

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password and username entered by the user is correct."""
        user = db.query(Users).filter_by(username=st.session_state['username'],
                                         password=st.session_state['password']).first()
        if user == None:
            st.session_state["password_correct"] = False
        elif (
             (user.username == st.session_state["username"]) and
             (user.password == st.session_state["password"])#stauth.Hasher(st.session_state["password"]).generate()
           ):
            st.success(user.username == st.session_state["username"])
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False
            

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False

    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")#(username, password)
        st.text_input("Password", type="password", on_change=password_entered, key="password")#(username, password)
        st.error("User not known or password incorrect")
        return False
        
    else:
        # Password correct.
        return True

with st.sidebar:

    if 'password_correct' not in st.session_state:
        connected = False
    elif st.session_state['password_correct'] == False:
        connected = False
    else:
        connected = True

    if connected:
        lg.info(f'Connection : {connected}')
        selected =  option_menu("Main Menu", ["Home", "Patient", "Information", 'Settings', 'Logout'], icons=['house', 'file-earmark-person', 'card-text','gear','door-open'], menu_icon="cast", default_index=1)
    else:
        lg.info(f'Connection : {connected}')
        selected =  option_menu("Main Menu", ["Home","Sign-in", "Sign-up"], icons=['house', "person", "pen"], menu_icon="cast", default_index=1)

if selected == 'Home':
    st.title('coucou home')
    st.balloons()
    
elif (selected == 'Patient'):
    st.title('Patients')

    fonction = st.selectbox('Fonction',('Ajouter un patient', 'Liste des patients'))

    if fonction == "Ajouter un patient":
        with st.form("form1"):
            first_name = st.text_input('Saisir le prénom')
            last_name = st.text_input('Saisir le Nom')
            username = st.text_input('Saisir le Surnom')
            password = st.text_input('Saisir le Mot de passe')
            fonction = st.selectbox('Fonction',('Patient', 'Docteur'))
            submit_add_patient = st.form_submit_button('Ajouter')
        
        if submit_add_patient:
            Users(first_name = first_name,last_name=last_name,username=username, password=password, fonction=fonction).save_to_db()
            st.success(f' Bienvenue  {username}')        
    elif fonction == "Liste des patients":
        liste_des_patients = Users.get_list_users_patient()
        df = pd.read_sql_query(
             sql = liste_des_patients,
             con = engine
        )
        AgGrid(df)
        # gb = GridOptionsBuilder.from_dataframe(df_test)
        # gb.configure_pagination()
        # gridOptions = gb.build()
        

        st.error('pas bon')
    
elif (selected == 'Information'):
    st.title('Information')
    fonction = st.selectbox('Fonction',('Ajouter une informations', 'Liste des informations'))
    
    if fonction == "Ajouter une informations":
        form = st.form("my_st")
        form.slider("Inside the st")
        form.slider("Outside the st")

        # Now add a submit button to the st:
        # form.form_submit_button("Submit")
        with form.form_submit_button("Submit"):
            st.write("TROU DE BALL ")
            st.stop()
    elif fonction == 'Liste des informations':
        query_full_informations = Informations.get_list_informations()
        df = pd.read_sql_query(
             sql = query_full_informations,
             con = engine
        )
        AgGrid(df)

elif (selected == 'Sign-in'):# & (connected==False):  
    st.title("Login")
    if check_password():
        pass
    
elif (selected == 'Sign-up'):# & (connected==False):
    st.title("Sign up")
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm password', type='password')
    signup = st.button('Sign up', key="signup_page_button")

    if signup:
        if (password == confirm_password) and username:
            hashed_password = stauth.Hasher(password).generate()
            Users(username=username, password= hashed_password, fonction='patient').save_to_db()
            st.success('You have successfully registered. You can now sign-in.')

elif (selected == 'Logout'):
    st.title('Click to log out')
    logout = st.button('Log out')
    if logout:
        st.session_state['password_correct'] = False
        st.experimental_rerun()

