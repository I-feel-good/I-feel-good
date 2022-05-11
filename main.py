from model import *
import streamlit as st
import streamlit_authenticator as stauth
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from streamlit_option_menu import option_menu
import logging as lg

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: primary;
}
</style>""", unsafe_allow_html=True)

st.get_option("theme.primaryColor")

with st.sidebar:
    connected = False
    if connected:
        lg.warning(f'Connection : {connected}')
        selected = option_menu("Main Menu", ["Home", "Patient", "Information", 'Settings'], icons=['house', '', 'card-text','gear'], menu_icon="cast", default_index=1)
    else:
        lg.warning(f'Connection : {connected}')
        selected = option_menu("Main Menu", ["Home","Sign-in", "Sign-up"], icons=['house', "person", "pen"], menu_icon="cast", default_index=1)

if selected == 'Home':
    st.title('coucou home')
    st.balloons()
    
elif (selected == 'Patient') & (connected==True):
    st.title('coucou Patient')
    if st.button('Add Patient'):
        st.write('Why hello there')
    else:
        st.write('Goodbye')
    
    
elif (selected == 'Information') & (connected==True):
    st.title('coucou Information')
    if st.button('Add Information'):
            st.write('Why hello there')
    else:
        st.write('Goodbye')
    
elif (selected == 'Sign-in') & (connected==False):
    st.title("Login")
    st.session_state['username'] = st.text_input('Username')
    st.session_state['password'] = st.text_input('Password', type='password', key='login_button')
    # hashed_password = stauth.Hasher(password).generate()
    # users = get_users(st.session_state['username'], st.session_state['password'])

    st.button('Login', key="login_page_button")
    
elif (selected == 'Sign-up') & (connected==False):
    st.title("Sign up")
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm password', type='password')
    hashed_password = stauth.Hasher(password).generate()
    hashed_confirm_password = stauth.Hasher(confirm_password).generate()

    st.button('Sign up', key="signup_page_button")#, on_click=login_message
