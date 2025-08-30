import streamlit as st
import pandas as pd
import plotly.express as px
from collections import defaultdict

def show_analises_tab(username, contas_data, config):
    st.subheader("Gráficos e Análises Avançadas")
    st.info("Em desenvolvimento...")

    # --- Evolução do saldo ao longo do tempo ---
    historico = []
    for user, contas in contas_data.items():
        for conta_nome, conta in contas.items():
            saldo = 0
            for t in sorted(conta.get("transacoes", []), key=lambda x: x["data"]):
                saldo += t["valor"]
                historico.append({"data": t["data"], "conta": f"{user} - {conta_nome}", "saldo": saldo})

    if historico:
        df = pd.DataFrame(historico)
        df["data"] = pd.to_datetime(df["data"])
        fig = px.line(df, x="data", y="saldo", color="conta", markers=True, title="Evolução do Saldo")
        st.plotly_chart(fig, use_container_width=True, config=config)
    else:
        st.info("Nenhuma transação registrada para exibir a evolução do saldo.")

    # --- Gastos por categoria (excluindo Salário) ---
    gastos_categoria = defaultdict(float)
    for contas in contas_data.values():
        for conta in contas.values():
            for t in conta.get("transacoes", []):
                if t["categoria"] != "Salário":
                    gastos_categoria[t["categoria"]] += abs(t["valor"])

    if gastos_categoria:
        df_gastos = pd.DataFrame.from_dict(gastos_categoria, orient="index", columns=["Total"])
        fig = px.pie(df_gastos, values="Total", names=df_gastos.index, title="Gastos por Categoria")
        st.plotly_chart(fig, use_container_width=True, config=config)
    else:
        st.info("Nenhum gasto registrado para exibir os gastos por categoria.")

    # --- Fluxo mensal (entradas e saídas) ---
    df_transacoes = []
    for contas in contas_data.values():
        for conta in contas.values():
            for t in conta.get("transacoes", []):
                df_transacoes.append(t)

    if df_transacoes:
        df_transacoes = pd.DataFrame(df_transacoes)
        df_transacoes['data'] = pd.to_datetime(df_transacoes['data'])
        df_transacoes['mes'] = df_transacoes['data'].dt.to_period('M').dt.to_timestamp()
        mensal = df_transacoes.groupby('mes')['valor'].sum().reset_index()
        fig = px.bar(mensal, x='mes', y='valor', title='Fluxo Mensal')
        st.plotly_chart(fig, use_container_width=True, config=config)
    else:
        st.info("Nenhuma transação registrada para exibir o fluxo mensal.")
