import streamlit as st
import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).parent / "contas.json"

def init_contas():
    if not DATA_FILE.exists():
        contas = {
            "admin": {
                "Conta 1": {
                    "descricao": "Saldo anterior",
                    "valor": 100.0,
                    "categoria": "Salario",
                    "data": "2020-01-01 00:00:00"
                    },
            }
        }
        save_contas(contas)

def load_contas():
    init_contas()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_contas(contas):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(contas, f, indent=4)

def get_contas(usuario):
    contas = load_contas()
    if usuario == "admin":
        return contas  # admin vê todos os usuários
    return {usuario: contas[usuario]}

def add_transacao(user, conta_nome, descricao, valor, categoria):
    with open("contas.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    nova_transacao = {
        "descricao": descricao,
        "valor": valor,
        "categoria": categoria,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data[user][conta_nome]["transacoes"].append(nova_transacao)

    with open("contas.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def remove_transacao(usuario, conta_nome, trans_index):
    contas = load_contas()
    
    if usuario not in contas or conta_nome not in contas[usuario]:
        raise ValueError("Usuário ou conta inválida.")
    
    # Remove a transação pelo índice
    if 0 <= trans_index < len(contas[usuario][conta_nome]["transacoes"]):
        contas[usuario][conta_nome]["transacoes"].pop(trans_index)
    else:
        raise IndexError("Índice de transação inválido.")
    
    save_contas(contas)

def calcular_saldo(conta: dict) -> float:
    return sum(t["valor"] for t in conta.get("transacoes", []))

