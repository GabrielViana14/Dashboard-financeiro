import streamlit as st
import pandas as pd
import json
from datetime import datetime
from contas import get_contas, add_transacao, remove_transacao

def show_transacoes_tab(username, contas_data):
    st.subheader("Detalhes das transações")
    categorias = [
        "Salário", "Alimentação", "Lazer", "Educação", "Investimentos", "Outros",
        "Transporte", "Saúde", "Moradia", "Roupas", "Viagem", "Presentes",
        "Impostos", "Assinaturas", "Cartão"
    ]

    for user, contas in contas_data.items():
        if username == 'admin': 
            st.subheader(f"Usuário: {user}")
        for conta_nome, conta in contas.items():
            with st.expander(f"{conta_nome}"):

                # ---- FILTROS ----
                col_start, col_end = st.columns(2)
                data_inicio = col_start.date_input("Data início", value=pd.to_datetime("2025-01-01"), key=f"start_{user}_{conta_nome}")
                data_fim = col_end.date_input("Data fim", value=pd.to_datetime("2025-12-31"), key=f"end_{user}_{conta_nome}")

                search = st.text_input("Pesquisar descrição", key=f"search_{user}_{conta_nome}")

                opcao_ordenacao = st.selectbox("Ordenar por", ["Data", "Valor", "Categoria"], key=f"sort_{user}_{conta_nome}")

                # ---- FILTRAR TRANSAÇÕES ----
                transacoes_filtradas = [
                    t for t in conta["transacoes"]
                    if data_inicio <= datetime.strptime(t["data"], "%Y-%m-%d %H:%M:%S").date() <= data_fim
                    and search.lower() in t["descricao"].lower()
                ]

                if opcao_ordenacao == "Valor":
                    transacoes_filtradas.sort(key=lambda x: x["valor"], reverse=True)
                elif opcao_ordenacao == "Data":
                    transacoes_filtradas.sort(key=lambda x: x["data"], reverse=True)
                elif opcao_ordenacao == "Categoria":
                    transacoes_filtradas.sort(key=lambda x: x["categoria"])
                st.write("")

                # ---- RESUMO DA CONTA ----
                total_entrada = sum(t["valor"] for t in transacoes_filtradas if t["valor"] > 0)
                total_saida = sum(t["valor"] for t in transacoes_filtradas if t["valor"] < 0)
                st.info(f"Total Entrada: R\${total_entrada:.2f} | Total Saída: R\${total_saida:.2f}")
                st.write("")

                # ---- LISTAR TRANSAÇÕES ----
                col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1])
                col1.write("Descrição")
                col2.write("Categoria")
                col3.write("Valor")
                col4.write("Data")
                col5.write("Ações")
                for j, t in enumerate(transacoes_filtradas):
                    col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1])
                    col1.write(t['descricao'])
                    col2.write(t['categoria'])
                    col3.write(f"R${t['valor']:.2f}")
                    dt = datetime.strptime(t["data"], "%Y-%m-%d %H:%M:%S")
                    col4.write(dt.strftime("%d/%m/%Y %H:%M"))

                    if username == "admin" or username == user:
                        if col5.button("❌", key=f"del_{user}_{conta_nome}_{j}"):
                            remove_transacao(user, conta_nome, j)
                            st.warning("Transação removida!")
                            st.rerun()
                st.write("")

                # ---- ADICIONAR NOVA TRANSAÇÃO ----
                if username == user:
                    descricao = st.text_input(f"Descrição - {conta_nome}", key=f"desc_{user}_{conta_nome}")
                    valor = st.number_input(f"Valor - {conta_nome}", key=f"val_{user}_{conta_nome}")
                    categoria = st.selectbox(f"Categoria - {conta_nome}", categorias, key=f"cat_{user}_{conta_nome}")
                    if st.button(f"Adicionar - {conta_nome}", key=f"add_{user}_{conta_nome}"):
                        add_transacao(user, conta_nome, descricao, valor, categoria)
                        st.success("Transação adicionada com sucesso!")
                        st.rerun()

                # ---- EXPORTAR CSV ----
                if transacoes_filtradas:
                    df_export = pd.DataFrame(transacoes_filtradas)
                    csv = df_export.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Exportar transações (CSV)",
                        data=csv,
                        file_name=f"{user}_{conta_nome}_transacoes.csv",
                        mime="text/csv"
                    )

    # ---- ADICIONAR NOVA CONTA ----
    st.subheader("Adicionar nova conta do banco")
    nova_conta_nome = st.text_input("Nome da conta", key="nova_conta")

    if st.button("Adicionar Conta"):
        if nova_conta_nome.strip() == "":
            st.warning("Digite um nome válido para a conta.")
        else:
            contas = get_contas(username)
            if username not in contas:
                contas[username] = {}

            if nova_conta_nome in contas[username]:
                st.warning("Essa conta já existe.")
            else:
                contas[username][nova_conta_nome] = {"transacoes": []}
                with open("contas.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                data[username][nova_conta_nome] = {"transacoes": []}
                with open("contas.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                st.success(f"Conta '{nova_conta_nome}' criada com sucesso!")
                st.rerun()
