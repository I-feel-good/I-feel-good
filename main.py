from model import *
import streamlit as st
from streamlit_option_menu import option_menu
import logging as lg

# SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace('postgres://','postgresql://')
# engine = create_engine(SQLALCHEMY_DATABASE_URI)
# # lg.warning(engine)
# lg.warning("START")
# Sessions = sessionmaker(bind=engine)
# db = Sessions()

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

    
    
elif (selected == 'Information') & (connected==True):
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
    
elif (selected == 'Sign-in') & (connected==False):
    st.title("Vous n'etes pas connecté bande de batard")
    
elif (selected == 'Sign-up') & (connected==False):
    st.title("Enregistrer tete d'alien")
    
    
