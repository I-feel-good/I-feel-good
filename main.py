from model import Users, Informations
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


m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: primary;
}
</style>""", unsafe_allow_html=True)

st.get_option("theme.primaryColor")

def sidebar_menu(connected=False):
    if connected:
        lg.warning(f'Connection : {connected}')
        return option_menu("Main Menu", ["Home", "Patient", "Information", 'Settings', 'Logout'], icons=['house', '', 'card-text','gear'], menu_icon="cast", default_index=1)
    else:
        lg.warning(f'Connection : {connected}')
        return option_menu("Main Menu", ["Home","Sign-in", "Sign-up"], icons=['house', "person", "pen"], menu_icon="cast", default_index=1)


with st.sidebar:
    selected = sidebar_menu()
    # connected = True
    # if connected:
    #     lg.warning(f'Connection : {connected}')
    #     selected =  option_menu("Main Menu", ["Home", "Patient", "Information", 'Settings', 'Logout'], icons=['house', '', 'card-text','gear'], menu_icon="cast", default_index=1)
    # else:
    #     lg.warning(f'Connection : {connected}')
    #     selected =  option_menu("Main Menu", ["Home","Sign-in", "Sign-up"], icons=['house', "person", "pen"], menu_icon="cast", default_index=1)


if selected == 'Home':
    st.title('coucou home')
    st.balloons()
    
elif (selected == 'Patient'):# & (connected==True):
    st.title('coucou Patient')
    if st.button('Add Patient'):
        st.write('Why hello there')
    else:
        st.write('Goodbye')
    
    
elif (selected == 'Information'):# & (connected==True):
    st.title('coucou Information')
    if st.button('Add Information'):
            st.write('Why hello there')
    else:
        st.write('Goodbye')
    
elif (selected == 'Sign-in'):# & (connected==False):
    with st.form(key="Login_form"):
        st.title("Login")
        st.session_state['username'] = st.text_input('Username')
        password = st.text_input('Password', type='password', key='login_button')
        # hashed_password = stauth.Hasher(password).generate()
        st.session_state['password'] = stauth.Hasher(password).generate()
        submit_login = st.form_submit_button("Login")
        if submit_login:
            user = db.query(Users).filter_by(username=st.session_state['username'],
                                password=password).first()
            try:
                if (user.username == st.session_state['username']) & (user.password == password):
                    st.write(("username", st.session_state['username'], "password", password))
                    
            except AttributeError:
                st.error("Username or password incorrect.")
    
    
elif (selected == 'Sign-up'):# & (connected==False):
    st.title("Sign up")
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm password', type='password')
    hashed_password = stauth.Hasher(password).generate()
    hashed_confirm_password = stauth.Hasher(confirm_password).generate()

    st.button('Sign up', key="signup_page_button")#, on_click=login_message
