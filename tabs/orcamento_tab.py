import streamlit as st
import json
from collections import defaultdict

def show_orcamento_tab(username, contas_data):
    st.subheader("Orçamento por Categoria")

    ARQUIVO_LIMITES = "orcamento_limites.json"

    # Categorias usadas em todo o app
    categorias = [
        "Salário", "Alimentação", "Lazer", "Educação", "Investimentos", "Outros",
        "Transporte", "Saúde", "Moradia", "Roupas", "Viagem", "Presentes",
        "Impostos", "Assinaturas", "Cartão"
    ]

    # --- Carregar limites do JSON ---
    try:
        with open(ARQUIVO_LIMITES, "r", encoding="utf-8") as f:
            limites_salvos = json.load(f)
    except FileNotFoundError:
        limites_salvos = {}

    # Inicializa session_state se não existir
    if "orcamento_limites" not in st.session_state:
        st.session_state["orcamento_limites"] = limites_salvos.get(username, {})

    # --- Calcula gastos por categoria (excluindo Salário) ---
    gastos_categoria = defaultdict(float)
    for contas in contas_data.values():
        for conta in contas.values():
            for t in conta.get("transacoes", []):
                if t["categoria"] != "Salário":
                    gastos_categoria[t["categoria"]] += abs(t["valor"])

    # --- Loop para definir limites e mostrar progresso ---
    for cat in categorias:
        if cat not in st.session_state["orcamento_limites"]:
            st.session_state["orcamento_limites"][cat] = 0.0

        col_limite, col_progresso = st.columns([1, 2])

        # Input do limite
        st.session_state["orcamento_limites"][cat] = col_limite.number_input(
            f"Limite {cat}",
            value=st.session_state["orcamento_limites"][cat],
            step=10.0,
            key=f"limite_{cat}"
        )

        # Barra de progresso
        gasto = gastos_categoria.get(cat, 0)
        limite = st.session_state["orcamento_limites"][cat]

        if limite > 0:
            progresso = min(gasto / limite, 1.0)
            col_progresso.write(f"{gasto:.2f} / {limite:.2f}")
            col_progresso.progress(progresso)
        else:
            col_progresso.write(f"{gasto:.2f} / Sem limite definido")

    # --- Botão para salvar limites ---
    if st.button("Salvar Limites"):
        limites_salvos[username] = st.session_state["orcamento_limites"]
        with open(ARQUIVO_LIMITES, "w", encoding="utf-8") as f:
            json.dump(limites_salvos, f, ensure_ascii=False, indent=4)
        st.success("Limites salvos com sucesso!")
