import streamlit as st
import json
import os

# Configuração da Página
st.set_page_config(page_title="Meu Sistema de Estudos", layout="wide")

# --- SEGURANÇA SIMPLES ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    
    if not st.session_state.auth:
        senha = st.sidebar.text_input("Senha de Acesso", type="password")
        if senha == "1234": # VOCÊ PODE MUDAR ESSA SENHA
            st.session_state.auth = True
            st.rerun()
        else:
            st.warning("Por favor, insira a senha na barra lateral.")
            return False
    return True

if check_password():
    # --- CARREGAMENTO DO BANCO ---
    @st.cache_data
    def carregar_dados():
        if os.path.exists("banco_final.json"):
            with open("banco_final.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    dados = carregar_dados()

    if not dados:
        st.error("Arquivo 'banco_final.json' não encontrado no repositório.")
    else:
        # --- LÓGICA DE NAVEGAÇÃO ---
        if "indice" not in st.session_state:
            st.session_state.indice = 0

        q = dados[st.session_state.indice]

        # --- INTERFACE (O SEU VISUALIZADOR LINDO) ---
        st.caption(f"{q['info']} | ID: {q['id']}")
        
        # Texto Associado (Retrátil)
        html_assoc = q.get('htmlTextoAssociado') or q.get('txtAssoc', '')
        if html_assoc and len(html_assoc) > 10:
            with st.expander("Ver Texto Associado / Imagem de Apoio"):
                st.markdown(html_assoc, unsafe_allow_html=True)

        # Enunciado
        st.markdown(f"### {q.get('htmlEnunciado') or q.get('enunciado')}", unsafe_allow_html=True)

        # Alternativas
        letras = ['A', 'B', 'C', 'D', 'E']
        for i, alt in enumerate(q['alts']):
            if st.button(f"{letras[i]}) {alt}", key=f"btn_{i}", use_container_width=True):
                if letras[i] == q['gabarito']:
                    st.success("Correto!")
                else:
                    st.error(f"Errado! O gabarito é {q['gabarito']}")

        # --- NAVEGAÇÃO ---
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Anterior"):
                if st.session_state.indice > 0:
                    st.session_state.indice -= 1
                    st.rerun()
        with col2:
            st.write(f"Questão {st.session_state.indice + 1} de {len(dados)}")
        with col3:
            if st.button("Próxima →"):
                if st.session_state.indice < len(dados) - 1:
                    st.session_state.indice += 1
                    st.rerun()