import streamlit as st
import json

def show_admin_tab(username, get_contas):
    if username != "admin":
        st.info("Somente administradores podem acessar esta aba.")
        return

    st.subheader("Gerenciar Contas (somente Admin)")

    # --- Adicionar Conta ---
    st.markdown("### Adicionar Conta")
    novo_usuario = st.text_input("Usuário", key="input_novo_usuario")
    nova_conta = st.text_input("Nome da Conta Bancaria", key="input_nova_conta")

    if st.button("Adicionar Conta", key="btn_adicionar_conta"):
        contas = get_contas("admin")
        if novo_usuario not in contas:
            contas[novo_usuario] = {}
        contas[novo_usuario][nova_conta] = {"transacoes": []}
        with open("contas.json", "w", encoding="utf-8") as f:
            json.dump(contas, f, ensure_ascii=False, indent=4)
        st.success(f"Conta '{nova_conta}' adicionada para o usuário '{novo_usuario}'")
        st.rerun()

    # --- Remover Conta ---
    st.markdown("### Remover Conta")
    contas = get_contas("admin")
    if contas:
        usuario_remover = st.selectbox("Escolha o usuário", options=list(contas.keys()), key="select_usuario_remover")
        conta_remover = st.selectbox("Escolha a conta", options=list(contas[usuario_remover].keys()), key="select_conta_remover")
        if st.button("Remover Conta", key="btn_remover_conta"):
            contas[usuario_remover].pop(conta_remover)
            with open("contas.json", "w", encoding="utf-8") as f:
                json.dump(contas, f, ensure_ascii=False, indent=4)
            st.warning(f"Conta '{conta_remover}' removida do usuário '{usuario_remover}'")
            st.rerun()
