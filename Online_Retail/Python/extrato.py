# importação
import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine


class OnlineRetails:
    
    def __init__(self):
        self.engine = self.create_engine()
    
    @staticmethod
    def create_engine():
        DATABASE_URL = "postgresql://postgres:123456@localhost:5432/online_retail"
        return create_engine(DATABASE_URL)

    
    def load_data(self):
        # Cria uma conexão e busca todos os registros da tabela "view_fonline_retail"
        query = "SELECT * FROM view_fonline_stremlit"
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df
    
    '''
    TRATAMENTO DOS DADOS
    '''
    
    
    
    
    
    '''
    SELEÇÃO DOS DADOS
    '''
    def dataframe(self):
        df = self.load_data()
        return df

df = OnlineRetails()
df = df.load_data()


# Site


# SIDEBAR
with st.sidebar:
    
    #TITLE
    st.title("Online Retails")
    
    #FILTROS SIDEBAR 
    
    # Filtro de intervalo de datas
    data = pd.to_datetime(df['data_fatura'])
    min_date = data.min()
    max_date = data.max()
    data_intervalo = st.date_input(
        "Intervalo de Datas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Filtrar o DataFrame pelo intervalo de datas selecionado
    if isinstance(data_intervalo, tuple) and len(data_intervalo) == 2:
        start_date, end_date = data_intervalo
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df = df[(data >= start_date) & (data <= end_date)]
    
    
    paises_distintos = df['pais'].unique().tolist()
    fil_paises = st.multiselect(
        "Pais",
        paises_distintos
    )
    if fil_paises:
        df = df[df['pais'].isin(fil_paises)]
    
    
    clientes_distintos = df['id_cliente'].unique().tolist()
    fil_cliente = st.multiselect(
        "Cliente",
        clientes_distintos
    )
    if fil_cliente:
        df = df[df['id_cliente'].isin(fil_cliente)]
        
        
    produtos_distintos = df['produtos'].unique().tolist()
    fil_produtos = st.multiselect(
        "Produtos",
        produtos_distintos
    )
    if fil_produtos:
        df = df[df['produtos'].isin(fil_produtos)]
    

# PAGINA
st.title("Extrato")
st.dataframe(df)
