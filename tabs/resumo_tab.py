import streamlit as st
import pandas as pd
import plotly.express as px
from collections import defaultdict

def show_resumo_tab(username, contas_data, config):
    st.title(f"Bem-vindo(a), {username.capitalize()}!")
    st.subheader("Visão geral dos saldos")
    saldo_total = 0
    cards_data = []

    # Saldos negativos
    saldos_negativos = []
    if username == "admin":
        for user, contas in contas_data.items():
            for conta_nome, conta in contas.items():
                saldo = sum(t["valor"] for t in conta.get("transacoes", []))
                if saldo < 0:
                    saldos_negativos.append((f"{user} - {conta_nome}", saldo))
    else:
        contas = contas_data.get(username, {})
        for conta_nome, conta in contas.items():
            saldo = sum(t["valor"] for t in conta.get("transacoes", []))
            if saldo < 0:
                saldos_negativos.append((f"{conta_nome}", saldo))

    for nome, saldo in saldos_negativos:
        st.warning(f"Saldo negativo em {nome}: R${saldo:.2f}")

    # Cards de saldo
    for user, contas in contas_data.items():
        if username == 'admin':
            st.markdown(f"**Usuário: {user}**")
        cols = st.columns(len(contas))
        for i, (conta_nome, conta) in enumerate(contas.items()):
            saldo = sum(t["valor"] for t in conta.get("transacoes", []))
            with cols[i]:
                st.metric(
                    label=conta_nome,
                    value=f"R${saldo:.2f}",
                    delta=f"{len(conta.get('transacoes', []))} transações",
                )
            cards_data.append({"Conta": f"{user} - {conta_nome}", "Saldo": saldo})
            saldo_total += saldo

    st.markdown(f"### Saldo Total: R${saldo_total:.2f}")
    st.write("")

    # Gráfico de barras
    st.subheader("Saldos por Conta")
    contas_list, saldos_list = [], []
    for user, contas in contas_data.items():
        for conta_nome, conta in contas.items():
            contas_list.append(conta_nome)
            saldos_list.append(sum(t["valor"] for t in conta.get("transacoes", [])))

    fig = px.bar(
        x=contas_list,
        y=saldos_list,
        color=saldos_list,
        color_continuous_scale="Blues",
        text=saldos_list,
        labels={"x": "Conta", "y": "Saldo (R$)"}
    )
    fig.update_traces(texttemplate="R$%{text:.2f}", textposition="outside", textfont=dict(size=18))
    fig.update_layout(showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True, config=config)
    st.write("")

    # Evolução do saldo ao longo do tempo
    historico = []
    for conta_nome, conta in contas.items():
        saldo = 0
        for t in sorted(conta.get("transacoes", []), key=lambda x: x["data"]):
            saldo += t["valor"]
            historico.append({"data": t["data"], "conta": conta_nome, "saldo": saldo})

    df = pd.DataFrame(historico, columns=["data", "conta", "saldo"])
    if not df.empty:
        df["data"] = pd.to_datetime(df["data"])
        st.subheader("Evolução do Saldo ao Longo do Tempo")
        fig2 = px.line(df, x="data", y="saldo", color="conta", markers=True)
        st.plotly_chart(fig2, use_container_width=True, config=config)
    else:
        st.info("Nenhuma transação registrada para exibir a evolução do saldo.")

    # Gastos por categoria
    categorias_totais = defaultdict(float)
    for conta in contas_data.values():
        for conta_nome, c in conta.items():
            for t in c.get("transacoes", []):
                if t["categoria"] != "Salário":
                    categorias_totais[t["categoria"]] += abs(t["valor"])

    if categorias_totais:
        st.subheader("Gastos por Categoria")
        st.bar_chart(pd.DataFrame.from_dict(categorias_totais, orient="index", columns=["Total"]))
    else:
        st.info("Nenhum gasto registrado para exibir.")
    st.write("")

    # Top 3 categorias
    top_categorias = sorted(categorias_totais.items(), key=lambda x: x[1], reverse=True)[:3]
    st.subheader("Top 3 categorias de gasto")
    cols = st.columns(3)
    for cat, val in top_categorias:
        with cols[top_categorias.index((cat, val))]:
            st.metric(label=cat, value=f"R${val:.2f}")
    st.write("")

    # Últimas transações
    st.subheader("Últimas transações")
    ultimas = []
    for conta_nome, conta in contas.items():
        for t in conta.get("transacoes", []):
            ultimas.append({
                "Conta": conta_nome,
                "Descricao": t["descricao"],
                "Categoria": t["categoria"],
                "Valor": t["valor"],
                "Data": t["data"]
            })
    ultimas = sorted(ultimas, key=lambda x: x["Data"], reverse=True)[:10]
    st.table(ultimas)
