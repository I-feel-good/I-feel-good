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
import requests
import plotly.express as px
import plotly.graph_objects as go

from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
from streamlit_lottie import st_lottie
import time
from pprint import pprint


load_dotenv(override=True)

# Database initialization
# lg.warning('Connection à la base de donnée')
# SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace('postgres://','postgresql://')
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL1").replace('postgres://','postgresql://')
SQLALCHEMY_TRACK_MODIFICATIONS = False
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Sessions = sessionmaker(bind=engine)
db = Sessions()

hide_menu_style = """
    <style>
    #MainMenu {visibility : hidden;}
    footer {visibility: hidden;}
    </style>
    """

st.markdown(hide_menu_style, unsafe_allow_html=True)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
    
def data_grid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled=True)
    gb.configure_side_bar()
    gb.configure_default_column(editable=True,groupable=True, value=True, enableRowGroup=True)
    gb.configure_selection(selection_mode='multiple', use_checkbox=True, groupSelectsChildren=True)
    gridOptions = gb.build()
    grid_response = AgGrid(df, 
                    gridOptions=gridOptions,
                    enable_enterprise_modules=True,
                    fit_columns_on_grid_load= False,
                    width= '100%',
                    update_mode=GridUpdateMode.SELECTION_CHANGED,
                    height=500,
                    allow_unsafe_jscode=True,
                    theme='light'
                    )
    sel_row =grid_response['selected_rows']
    return df, sel_row

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password and username entered by the user is correct."""
        # user = db.query(Users).filter_by(username=st.session_state['username'],
        #                                  password=st.session_state['password']).first()
        user = Users.get_user(st.session_state['username'])
        if user == None:
            st.session_state["password_correct"] = False
        elif (
             (user.username == st.session_state["username"]) and
             (user.password == st.session_state["password"])#stauth.Hasher(st.session_state["password"]).generate()
           ):
            st.success("You have successfully logged in.")
            st.session_state["password_correct"] = True
            st.session_state['fonction'] = user.fonction
            st.session_state['user_name'] = user.username
            del st.session_state["password"]  # don't store password
            # del st.session_state["username"]


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


    if (connected) and st.session_state['fonction'] == 'docteur':
        lg.warning('Connection : {}'.format("connected as a doctor"))
        selected =  option_menu("Main Menu", ["Home", "Patient", "Information", "Dashboard", 'Settings', 'Logout'], icons=['house', 'file-earmark-person', 'card-text','gear','door-open'], menu_icon="cast", default_index=1)
    elif (connected) and st.session_state['fonction'] == 'patient':
        lg.warning('Connection : {}'.format("connected as a patient"))
        selected =  option_menu("Main Menu", ["Home", "Patient", "Information", "Dashboard", 'Logout'], icons=['house', 'file-earmark-person', 'card-text','door-open'], menu_icon="cast", default_index=1)
    else:
        lg.warning('Connection : {}'.format("disconnected"))

        selected =  option_menu("Main Menu", ["Home","Sign-in", "Sign-up"], icons=['house', "person", "pen"], menu_icon="cast", default_index=1)

if selected == 'Home':
    st.title('Bienvenur sur notre application du bonheur')
    url = 'https://assets8.lottiefiles.com/packages/lf20_bkwin39r.json'
    res_json = load_lottieurl(url)
    st_lottie(res_json)
    
elif (selected == 'Patient'):
    st.title('Patients')
    if st.session_state['fonction'] == 'patient':
        fonction = st.selectbox('Fonction',(['Liste des patients']))
    elif st.session_state['fonction'] == 'docteur':
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
        if st.session_state['fonction'] == 'patient':
            liste_des_patients = Users.get_list_by_user(st.session_state['user_name'])
            print(liste_des_patients)
            df = pd.read_sql_query(
                sql = liste_des_patients,
                con = engine
            )
            df, sel_row = data_grid(df)
            col1, col2= st.columns(2)
            col1.button('Delete')
            col2.button('Save')
            st.write(sel_row)
            # pass get_list_by_user""
        elif st.session_state['fonction'] == 'docteur':
            liste_des_patients = Users.get_list_users_patient()
            df = pd.read_sql_query(
                sql = liste_des_patients,
                con = engine
            )
            df, sel_row = data_grid(df)
            col1, col2= st.columns(2)
            col1.button('Delete')
            col2.button('Save')
            st.write(sel_row)
    
elif (selected == 'Information'):
    st.title('Information')
    fonction = st.selectbox('Fonction',('Ajouter une informations', 'Liste des informations'))
    
    if fonction == "Ajouter une informations":
        os.system('cls')
        with st.form("form2"):
            text = st.text_input('Saisir votre information')
            if st.session_state['fonction'] == 'docteur':
                options = Users.get_list_users_patient()
                df = pd.read_sql_query(
                sql = options,
                con = engine
            )
                fonction = st.selectbox('Username',(df.username.to_list()))
            
            st.form_submit_button("Submit")

    elif fonction == 'Liste des informations':
        os.system('cls')
        if st.session_state['fonction'] == 'docteur':
            query_full_informations = Informations.get_list_informations()
        elif st.session_state['fonction'] == 'patient':
            query_full_informations = Informations.get_list_informations_username(st.session_state['user_name'])
            
        df = pd.read_sql_query(
             sql = query_full_informations,
             con = engine
        )
        df, sel_row = data_grid(df)
        col1, col2= st.columns(2)
        col1.button('Delete')
        col2.button('Save')

elif (selected == 'Dashboard'):
    if st.session_state['fonction'] == 'docteur':
        pass
    elif st.session_state['fonction'] == 'patient':
        user = Users.get_user(st.session_state['user_name'])
        query_full_informations_user = Informations.get_list_informations_by_users(user)
        df = pd.read_sql_query(
             sql = query_full_informations_user,
             con = engine
             )
        # AgGrid(df)
        # st.info(dict(values=[df['first_name']]))
        df = df.head()
        fig = go.Figure(data=go.Table(
                            header=dict(values=list([df[['first_name']].columns]),
                            fill_color = '#ffee22',
                            align='center'),
                            cells=dict(values=[df['first_name']],
                            fill_color="#eeeeee",
                            align='left')
                            ))
        # fig.update_layout(margin=dict(l=0,r=0,t=0,b=0))
#         st.write(fig)
# #,df.last_name,df.username,df.dateofcreation,
#df.last_updated,df.emotion,df.text
 
elif (selected == 'Sign-in'):# & (connected==False):  
    st.title("Login")
    if check_password():
        pass
    
elif (selected == 'Sign-up'):# & (connected==False):
    st.title("Sign up")
    last_name = st.text_input('Last name')
    first_name = st.text_input('First name')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm password', type='password')
    signup = st.button('Sign up', key="signup_page_button")

    if signup:
        if (password == confirm_password) and username:
            hashed_password = stauth.Hasher(password).generate()
            Users(last_name=last_name, first_name = first_name, username=username, password= password, fonction='patient').save_to_db()
            st.success('You have successfully registered. You can now sign-in.')

elif (selected == 'Logout'):
    st.title('Click to log out')
    logout = st.button('Log out')
    url = 'https://assets2.lottiefiles.com/packages/lf20_kd5rzej5.json'
    res_json = load_lottieurl(url)
    st_lottie(res_json)
    if logout:
        st.session_state['password_correct'] = False
        del st.session_state['fonction']
        del st.session_state['user_name']
        st.experimental_rerun()

