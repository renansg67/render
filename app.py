# app.py
import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv

# --- CONFIGURAÇÃO ---
load_dotenv() 

# Vamos ler as variáveis que o Render nos dá
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
# --------------------

# --- DEBUG DE VARIÁVEIS ---
# Vamos imprimir na tela o que o Render está vendo
st.title("🐞 Debugando Variáveis de Ambiente no Render 🐞")
st.header("Verificação das Chaves:")

st.write(f"1. Chave 'DB_HOST':")
st.write(f"`{DB_HOST}`")

st.write(f"2. Chave 'POSTGRES_DB':")
st.write(f"`{DB_NAME}`")

st.write(f"3. Chave 'POSTGRES_USER':")
st.write(f"`{DB_USER}`")

st.write("4. Chave 'POSTGRES_PASSWORD':")
if DB_PASS is None or DB_PASS == "":
    st.error("ERRO: A variável 'POSTGRES_PASSWORD' está VAZIA ou não foi encontrada.")
else:
    st.success("OK: A variável 'POSTGRES_PASSWORD' foi encontrada (Não será exibida por segurança).")

st.header("Tentativa de Conexão:")
# --------------------


# Função para pegar a conexão com o banco
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=5432 
        )
        return conn
    except Exception as e:
        # Mostra o erro real do psycopg2
        st.error(f"Erro real do psycopg2: {e}")
        return None

# --- Interface do Streamlit ---
conn = get_db_connection()

if conn:
    st.success("🎉 CONECTADO COM SUCESSO! 🎉")
    st.balloons()
    
    # ... (o resto do seu código de escrita e leitura pode vir aqui) ...
    
    conn.close()