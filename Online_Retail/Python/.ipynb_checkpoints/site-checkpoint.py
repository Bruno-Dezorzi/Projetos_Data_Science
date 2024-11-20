# importação
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql://postgres:123456@localhost:5432/online_retail"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

def load_data():
    # Cria uma conexão e busca todos os registros da tabela "sua_tabela"
    query = "SELECT * FROM view_fonline_retail"
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
    return df

# Organizar os dados
df = load_data()



# Site
st.title("Visualização de Dados")
st.write("Abaixo estão todos os registros da tabela selecionada:")
st.dataframe(df)
st.write("Abaixo estão todos os registros da tabela selecionada:")