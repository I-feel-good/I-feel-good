from model import *
import streamlit as st
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
    connected = True
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
    st.title('List des Patients')
    if st.button('Ajouter un Patient'):
        first_name = st.text_input('Prénom')
        last_name = st.text_input('Nom')
        username = st.text_input('Surnon')
        password = st.text_input('Mot de passe')
        fonction = st.selectbox(
     'Fonction',
     ('Patient', 'Docteur'))

st.write('You selected:', option)
        st.button('Enregistrer')
    elif st.button('Liste des Patient'):
        pass
    else:
        st.write('Goodbye')
    
    
elif (selected == 'Information') & (connected==True):
    st.title('coucou Information')
    if st.button('Add Information'):
            st.write('Why hello there')
    else:
        st.write('Goodbye')
    
elif (selected == 'Sign-in') & (connected==False):
    st.title("Vous n'etes pas connecté bande de batard")
    
elif (selected == 'Sign-up') & (connected==False):
    st.title("Enregistrer tete d'alien")