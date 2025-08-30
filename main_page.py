import json
from time import time
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from contas import get_contas, add_transacao, remove_transacao
from datetime import datetime
import pandas as pd
from collections import defaultdict

from tabs.resumo_tab import show_resumo_tab
from tabs.transacoes_tab import show_transacoes_tab
from tabs.orcamento_tab import show_orcamento_tab
from tabs.graficos_tab import show_analises_tab
from tabs.admin_tab import show_admin_tab

# Config para manter a barra de ferramentas sempre visível
config = {
    "displayModeBar": True,       # Sempre mostrar
    "displaylogo": False,         # Remove o logo do Plotly
    "modeBarButtonsToRemove": [], # Lista de botões que você quer remover
}


def show_main_page(username):
    if "update_trigger" not in st.session_state:
        st.session_state["update_trigger"] = False

    contas_data = get_contas(username)  # sempre puxa do JSON atualizado

    # ---- Abas principais ----
    tabs = ["Resumo", "Transações", "Orçamento", "Gráficos / Análises"]
    if username == "admin":
        tabs.append("Gerenciar Contas")  # só aparece para admin

    tab1, tab2, tab3, tab4, *tab_admin = st.tabs(tabs)

    # ---- Chamadas das abas ----
    with tab1:
        show_resumo_tab(username, contas_data, config)

    with tab2:
        show_transacoes_tab(username, contas_data)

    with tab3:
        show_orcamento_tab(username, contas_data)

    with tab4:
        show_analises_tab(username, contas_data, config)

    if username == "admin" and tab_admin:
        with tab_admin[0]:
            show_admin_tab(username, get_contas)

    # ---- Sidebar ----
    with st.sidebar:
        st.header("Navegação e Filtros")

        # Seleção de usuário (apenas para admin)
        if username == "admin":
            usuario_selecionado = st.selectbox(
                "Selecionar usuário",
                list(contas_data.keys()),
                index=0
            )
        else:
            usuario_selecionado = username

        # Filtros globais por data
        st.subheader("Filtrar por Data")
        data_inicio_sidebar = st.date_input("Data Início", value=pd.to_datetime("2025-01-01"))
        data_fim_sidebar = st.date_input("Data Fim", value=pd.to_datetime("2025-12-31"))

        # Botão de atualização
        if st.button("Atualizar Dashboard"):
            st.session_state["update_trigger"] = not st.session_state.get("update_trigger", False)
            st.rerun()
