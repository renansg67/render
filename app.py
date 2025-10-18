# app.py
import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv # <-- Importante!

# --- CONFIGURAÇÃO ---
# Carrega as variáveis do arquivo .env (se ele existir)
# Esta linha lê o .env e torna as variáveis
# acessíveis para o os.getenv()
load_dotenv()

# Agora, pegamos as variáveis do ambiente.
# Localmente: Elas virão do .env
# No Render: Elas virão do painel do Render
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("DB_PORT") # <-- MUITO IMPORTANTE: Lendo a porta
# --------------------


# Função para pegar a conexão com o banco
def get_db_connection():
    # Checa se todas as variáveis foram carregadas
    if not all([DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT]):
        st.error("ERRO: Uma ou mais variáveis de ambiente (HOST, DB, USER, PASS, PORT) não foram encontradas.")
        return None
        
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT # <-- MUITO IMPORTANTE: Usando a porta correta (6543)
        )
        return conn
    except psycopg2.OperationalError as e:
        st.error(f"Falha ao conectar! Verifique as credenciais ou a rede. Erro: {e}")
        return None
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
        return None

# --- Interface do Streamlit ---
st.title("Teste com .env e Psycopg2 (Versão Pooler) 🚀")

conn = get_db_connection()

if conn:
    st.success("Conectado com sucesso ao Supabase (usando Transaction Pooler)!")
    
    # Criar tabela (se não existir)
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS test_logs (
                    id SERIAL PRIMARY KEY,
                    message TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            conn.commit()
    except Exception as e:
        st.error(f"Erro ao criar tabela: {e}")

    # Seção de Escrita
    with st.form("add_log_form"):
        message = st.text_input("Escreva uma mensagem para salvar:")
        submitted = st.form_submit_button("Salvar no Banco")
        
        if submitted and message:
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO test_logs (message) VALUES (%s)", 
                        (message,)
                    )
                    conn.commit()
                    st.success("Mensagem salva!")
                    # CORREÇÃO: O comando correto é st.rerun()
                    st.rerun() 
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

    # Seção de Leitura
    st.header("Logs Salvos no Banco")
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT message, created_at FROM test_logs ORDER BY created_at DESC LIMIT 10")
            logs = cur.fetchall()
            
            if not logs:
                st.info("Nenhuma mensagem encontrada.")
            else:
                for log in logs:
                    st.markdown(f"- **{log[0]}** *(em {log[1].strftime('%d/%m/%Y %H:%M')})*")
    except Exception as e:
        st.error(f"Erro ao ler os logs: {e}")
        
    conn.close()