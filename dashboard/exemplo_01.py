import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Lê a variavel de ambiente DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_KEY")

def ler_dados_postgres():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        query = "SELECT * FROM bitcoin_dados ORDER BY timestamp DESC"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao ler dados do PostgreSQL: {e}")
        return pd.DataFrame()
    

def main():
    st.set_page_config(page_title="Dashboard de Preços do Bitcoin", layout="wide")
    st.title("Dashboard de Preços do Bitcoin")
    st.write("Este dashboard exibe os preços do Bitcoin ao longo do tempo coletados do PostgreSQL.")


    df = ler_dados_postgres()
    if not df.empty:
        st.subheader("Dados Recentes")
        st.dataframe(df)

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by='timestamp')

        st.subheader("Gráfico de Preços do Bitcoin")
        st.line_chart(data=df, x='timestamp', y='valor', use_container_width=True)

        st.subheader("Estatísticas Descritivas")
        col1, col2, col3 = st.columns(3)
        col1.metric("Preço Atual", f"R$ {df['valor'].iloc[-1]:,.2f}")
        col2.metric("Preço Máximo", f"R$ {df['valor'].max():,.2f}")
        col3.metric("Preço Mínimo", f"R$ {df['valor'].min():,.2f}")

    else:
        st.warning("Nenhum dado disponível para exibição.") 

if __name__ == "__main__":
    main() 