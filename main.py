from model import *
import streamlit as st
import streamlit_authenticator as stauth
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from streamlit_option_menu import option_menu
import logging as lg
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Database initialization
# lg.warning('Connection à la base de donnée')
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace('postgres://','postgresql://')
SQLALCHEMY_TRACK_MODIFICATIONS = False
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Sessions = sessionmaker(bind=engine)
db = Sessions()


# SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace('postgres://','postgresql://')
# engine = create_engine(SQLALCHEMY_DATABASE_URI)
# # lg.warning(engine)
# lg.warning("START")
# Sessions = sessionmaker(bind=engine)
# db = Sessions()

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
            st.success("You have successfully logged in.")
            st.session_state["password_correct"] = True
            st.session_state['fonction'] = user.fonction
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

    if (connected) and st.session_state['fonction'] == 'docteur':
        lg.warning('Connection : {}'.format("connected as a doctor"))
        selected =  option_menu("Main Menu", ["Home", "Patient", "Information", 'Settings', 'Logout'], icons=['house', 'file-earmark-person', 'card-text','gear','door-open'], menu_icon="cast", default_index=1)
    elif (connected) and st.session_state['fonction'] == 'patient':
        lg.warning('Connection : {}'.format("connected as a patient"))
        selected =  option_menu("Main Menu", ["Home", "Patient", "Information", 'Logout'], icons=['house', 'file-earmark-person', 'card-text','door-open'], menu_icon="cast", default_index=1)
    else:
        lg.warning('Connection : {}'.format("disconnected"))
        selected =  option_menu("Main Menu", ["Home","Sign-in", "Sign-up"], icons=['house', "person", "pen"], menu_icon="cast", default_index=1)


if selected == 'Home':
    st.title('coucou home')
    st.balloons()
    
elif (selected == 'Patient'):

    if st.session_state['fonction'] == 'docteur':
        st.title('List des Patients')

        fonction = st.selectbox('Fonction',('add_Patient', 'Docteur'))

        if fonction == "add_Patient":
            with st.form("form1"):
                first_name = st.text_input('Saisir le prénom')
                last_name = st.text_input('Saisir le Nom')
                username = st.text_input('Saisir le Surnom')
                password = st.text_input('Saisir le Mot de passe')
                
                fonction = st.selectbox('Fonction',('Patient', 'Docteur'))
                submit_button1 = st.form_submit_button('Submit')
            
            if submit_button1:
                user = Users(first_name = first_name,last_name=last_name,username=username, password=password, fonction=fonction)
                os.system('cls')
                print(user.first_name)
                user.save_to_db()
                
                # db.session.add(user)
                # db.commit()
                st.success("oklm")
                st.success(username)        
        elif fonction == "Docteur":
            st.error('pas bon')
    
elif (selected == 'Information'):
    st.title('coucou Information')
    if st.button('Add Information'):
        form = st.form("my_st")
        form.slider("Inside the st")
        form.slider("Outside the st")

        # Now add a submit button to the st:
        # form.form_submit_button("Submit")
        with form.form_submit_button("Submit"):
            st.write("TROU DE BALL ")
            print('ffsffffsffdsffffffffffffffffffffffffffffffffffffffffffffffffffffff')
            st.stop()
    else:
        st.write('Goodbye')

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
            new_user = Users(last_name=last_name, first_name = first_name, username=username, password= password, fonction='patient')
            new_user.save_to_db()
            # db.add(new_user)
            # db.commit()
            st.success('You have successfully registered. You can now sign-in.')

elif (selected == 'Logout'):
    st.title('Click to log out')
    logout = st.button('Log out')
    if logout:
        st.session_state['password_correct'] = False
        st.experimental_rerun()

