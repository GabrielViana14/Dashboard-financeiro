import pickle
from pathlib import Path
import streamlit_authenticator as stauth

nomes = ['Admin']
usernames = ['admin']
senhas = ['teste']

# Criar objeto Hasher
hasher = stauth.Hasher()

# Gerar hashes individualmente
hashed_senhas = [hasher.hash(s) for s in senhas]

# Salvar em arquivo .pkl
file_path = Path(__file__).parent / 'hashed_senhas.pkl'
with file_path.open('wb') as file:
    pickle.dump(hashed_senhas, file)
print(f"Hashed passwords saved to {file_path}")