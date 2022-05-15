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

from dashboard import liquid_plot, radar_factory
import matplotlib.pyplot as plt
from streamlit_echarts import st_pyecharts
from pyecharts import options as opts
from pyecharts.charts import Liquid, Polar
from pyecharts.globals import SymbolType

from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
from streamlit_lottie import st_lottie
import time

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

elif (selected == 'Dashboard'):
    if st.session_state['fonction'] == 'docteur':
        pass
    elif st.session_state['fonction'] == 'patient':
        radar_box = st.container()
        table_box = st.container()

        user = Users.get_user(st.session_state['user_name'])
        query_full_informations_user = Informations.get_list_informations_by_users(user)
        df = pd.read_sql_query(
             sql = query_full_informations_user,
             con = engine
             )
        # AgGrid(df)
        # st.info(dict(values=[df['first_name']]))
        df_head = df.head()
        with radar_box:
            st.header('Select a date interval')
            early_date_col, late_date_col = st.columns(2)
            early_date = early_date_col.date_input(label='Select early date')
            late_date = late_date_col.date_input(label='Select late date')
            last_updated_datetime = pd.to_datetime(df['last_updated']).dt.date
            if early_date == late_date:
                df_date = df.loc[(last_updated_datetime == early_date)]
            else:
                df_date = df.loc[(last_updated_datetime >= early_date) & (last_updated_datetime <= late_date)]

            df_emotion = pd.DataFrame(df_date['emotion'].value_counts()).reset_index() \
                                        .rename(columns={'index':'Emotion','emotion':'proportion'})
            df_emotion['proportion'] /= df_emotion['proportion'].sum()

            if  early_date or late_date:
                if (early_date <= late_date):
                    if df_emotion.empty:
                        st.subheader('No post for this period.')
                    else:

                        list_emotions = ['happy', 'love', 'sadness', 'anger', 'fear', 'surprise']
                        for emotion in list_emotions:
                            if emotion not in df_emotion['Emotion'].values:
                                df_emotion = df_emotion.append({'Emotion': emotion, 'proportion': 0}, ignore_index=True)
                        # Wheel of emotions (radar plot)
                        theta = radar_factory(6,'polygon')
                        fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(projection='radar'))
                        ax.plot(theta, df_emotion['proportion'], color='r')
                        ax.fill(theta, df_emotion['proportion'], facecolor='r', alpha=0.25)
                        ax.set_varlabels(df_emotion['Emotion'].values.tolist())
                        fig.text(0.5, 0.965, 'Wheel of emotions',
                        horizontalalignment='center', color='black', weight='bold',
                        size='xx-large')

                        # Liquid plot
                        happy_proportion = df_emotion['proportion'][df_emotion['Emotion']=='happy'].values
                        love_proportion = df_emotion['proportion'][df_emotion['Emotion']=='love'].values
                        sadness_proportion = df_emotion['proportion'][df_emotion['Emotion']=='sadness'].values
                        anger_proportion = df_emotion['proportion'][df_emotion['Emotion']=='anger'].values
                        fear_proportion = df_emotion['proportion'][df_emotion['Emotion']=='fear'].values
                        surprise_proportion = df_emotion['proportion'][df_emotion['Emotion']=='surprise'].values

                        happy= liquid_plot(data=happy_proportion[0], title='Happy', liquid_color='#990000', shape=None)
                        love= liquid_plot(data=love_proportion[0], title='Love', liquid_color='#FF0099', shape=SymbolType.ROUND_RECT)
                        sadness= liquid_plot(data=sadness_proportion[0], title='Sadness', liquid_color='#0000FF', shape=SymbolType.RECT)
                        anger= liquid_plot(data=anger_proportion[0], title='Anger', liquid_color='#FF0000', shape=SymbolType.DIAMOND)
                        fear= liquid_plot(data=fear_proportion[0], title='Fear', liquid_color='#00FF00', shape=SymbolType.ARROW)
                        surprise= liquid_plot(data=surprise_proportion[0], title='Surprise', liquid_color='#990099', shape=SymbolType.TRIANGLE)

                        st.pyplot(fig)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st_pyecharts(happy)
                            st_pyecharts(love)
                        with col2:
                            st_pyecharts(sadness)
                            st_pyecharts(anger)
                        with col3:
                            st_pyecharts(fear)
                            st_pyecharts(surprise)
                else:
                    st.error('The early date must be earliest than the late date !')

        with table_box:
            # fig = go.Figure(data=go.Table(
            #                     columnwidth = [1,1,1,2,2,1,3],
            #                     header=dict(values=list(['firstname','lastname','username','date of creation','last update', 'emotion', 'text']),
            #                     fill_color = '#ff6622',
            #                     align='center'),
            #                     cells=dict(values=[df_head.first_name,df_head.last_name,df_head.username,
            #                                     df_head.dateofcreation,df_head.last_updated,df_head.emotion,df_head.text],
            #                     fill_color="#eeeeee",
            #                     align='left')
            #                     ))
            # fig.update_layout(margin=dict(l=0,r=0,t=0,b=0))
            # st.write(fig)
            st.header('Select the date of your post.')
            date = st.date_input(label='Select a date')
            st.markdown('***Your text of date {}***'.format(date))
            if 'choose_date' not in st.session_state:
                st.session_state['choose_date'] = False

            if date or st.session_state['choose_date']:
                st.session_state['choose_date'] = True
                text = df['text'][pd.to_datetime(df['last_updated']).dt.date == date]
                df_text = df[['dateofcreation', 'last_updated','text']][pd.to_datetime(df['last_updated']).dt.date == date]
                if df_text.empty:
                    st.subheader('No post for this date.')
                else:
                    AgGrid(pd.DataFrame(df_text))

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

