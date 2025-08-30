import streamlit as st
from auth import get_authenticator
from main_page import show_main_page
import time

# Gatilho para atualização
if 'update_trigger' not in st.session_state:
    st.session_state['update_trigger'] = False
    
# Inicializa o autenticador
authenticator = get_authenticator()

# Renderiza o formulário de login
authenticator.login(key="Login", location="main")

# Verifica status de autenticação usando st.session_state
if "authentication_status" in st.session_state:
    if st.session_state["authentication_status"]:
        authenticator.logout("Logout", location="sidebar")
        # Spinner enquanto a main page carrega
        with st.spinner("Carregando seu dashboard..."):
            if 'name' in st.session_state and st.session_state['name'] is not None:
                show_main_page(st.session_state['name'].lower())
            else:
                st.warning("Por favor, faça login primeiro.")
    elif st.session_state["authentication_status"] is False:
        st.error("Usuário ou senha incorretos")
else:
    st.warning("Por favor, insira seu usuário e senha")
