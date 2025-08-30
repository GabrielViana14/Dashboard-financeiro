import pickle
from pathlib import Path
import streamlit as st
import streamlit_authenticator as stauth

def get_authenticator():
    # Carregar senhas hasheadas
    file_path = Path(__file__).parent / 'hashed_senhas.pkl'
    with file_path.open('rb') as file:
        hashed_senhas = pickle.load(file)

    # Configuração de credenciais
    credentials = {
        "usernames": {
            "admin": {"name": "Admin", "password": hashed_senhas[0]},
        }
    }

    # Inicializar autenticador
    authenticator = stauth.Authenticate(
        credentials=credentials,
        cookie_name="dashboard_financeiro",
        key="abcdef",
        expiry_days=30
    )
    return authenticator
