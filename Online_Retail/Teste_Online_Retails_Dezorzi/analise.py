# importação
import streamlit as st
import locale
import pandas as pd
import plotly.express as px
from datetime import datetime
from sqlalchemy import create_engine

# Configuração da página Streamlit
st.set_page_config(
    page_title="Online Retails",
    page_icon="📊",
    layout='wide',
    initial_sidebar_state='expanded'
)

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Conexão com o banco de dados
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/online_retail"
engine = create_engine(DATABASE_URL)

# Função para carregar os dados com cache

def load_data():
    query = "SELECT * FROM view_fonline_stremlit"
    return pd.read_sql(query, engine)

# Carregar os dados
df = load_data()

# SIDEBAR
with st.sidebar:
    
    # Título
    st.title("Online Retails")
    
    # FILTROS SIDEBAR 
    
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
    
    # Filtro de Países
    paises_distintos = df['pais'].unique().tolist()
    fil_paises = st.multiselect(
        "Pais",
        paises_distintos
    )
    if fil_paises:
        df = df[df['pais'].isin(fil_paises)]
    
    # Filtro de Clientes
    clientes_distintos = df['id_cliente'].unique().tolist()
    fil_cliente = st.multiselect(
        "Cliente",
        clientes_distintos
    )
    if fil_cliente:
        df = df[df['id_cliente'].isin(fil_cliente)]
        
    # Filtro de Produtos
    produtos_distintos = df['produtos'].unique().tolist()
    fil_produtos = st.multiselect(
        "Produtos",
        produtos_distintos
    )
    if fil_produtos:
        df = df[df['produtos'].isin(fil_produtos)]
        

cabecalho = st.container()
cabecalho.title("Bem Vindo a sua Gestão Financeira", )

class Medidas:
    def __init__(self) -> None:
        pass
    
    def soma_faturamento(self):
        soma = df['valor_receita'].sum()
        return round(soma,2)
    
    def calcular_ticket_medio(self):
        """Calcula o Ticket Médio com base na soma de 'valor_receita' por data de fatura."""
        # Calculando a soma total das receitas
        total_faturamento = self.soma_faturamento()

        # Calculando o número de datas distintas
        num_datas_distintas = df['data_fatura'].nunique()

        # Calculando o Ticket Médio
        ticket_medio = total_faturamento / num_datas_distintas if num_datas_distintas != 0 else 0
        return round(ticket_medio, 2)
    
    def soma_produtos(self):
        soma = df['quantidade'].sum()
        return round(soma,2)
    
    
    def soma_clientes_unicos(self):
        soma = len(df['id_cliente'].unique())
        return round(soma,2)

medidas = Medidas()

# Aqui você formata a soma do faturamento como "R$ 8.000,00"
faturamento_formatado = locale.currency(medidas.soma_faturamento(), grouping=True)
ticket_medio = locale.currency(medidas.calcular_ticket_medio(), grouping=True)
soma_produtos = locale.format_string("%d", medidas.soma_produtos(), grouping=True)  
soma_clientes_unicos = locale.format_string("%d", medidas.soma_clientes_unicos(), grouping=True)    
col1,col2,col3 = st.columns(3)

# Exibindo a métrica no Streamlit
with col1:
    st.metric("R$ Receita", faturamento_formatado)
    st.metric("Ticket Médio", ticket_medio)
    st.metric("Qtde de Produtos", soma_produtos)
    st.metric("Qtde Clientes Únicos", soma_clientes_unicos)
    
    
    
def barra_pais():
        # Agrupando por 'pais' e somando 'valor_receita' e 'quantidade', além de calcular a média de 'valor_unitario'
        df_sorted = df.groupby('pais').agg(
            valor_receita=('valor_receita', 'sum'),  # Soma do valor da receita por país
            quantidade=('quantidade', 'sum'),        # Soma da quantidade por país
            valor_unitario=('valor_unitario', 'max')  # Máximo do valor unitário por país
        ).reset_index()

        # Ordenando os países por valor_receita em ordem decrescente
        df_sorted = df_sorted.sort_values(by='valor_receita', ascending=True)

        # Criando o gráfico de barras horizontais
        fig = px.bar(df_sorted,
                    x="valor_receita",  # Eixo X é o valor da receita
                    y="pais",  # Eixo Y são os países
                    orientation="h",  # Barras horizontais
                    hover_name="pais",  # Nome do país ao passar o mouse
                    hover_data=["quantidade", "valor_unitario"],  # Dados extras ao passar o mouse
                    title="Receita por País",  # Título do gráfico
                    labels={"valor_receita": "Valor da Receita", "pais": "País"},  # Rótulos personalizados
                    color_discrete_sequence=["#1f77b4"])  # Cor única azul (ajustada para um tom de azul específico)

        # Adicionando rótulos de dados ao lado de cada barra
        fig.update_traces(text=df_sorted['valor_receita'], textposition='outside')  # Mostra o valor das receitas ao lado da barra

        # Ajustando o layout para permitir rolagem horizontal e remover legenda
        fig.update_layout(
            xaxis_title="Valor da Receita",
            yaxis_title="País",
            margin={"l": 150, "r": 50, "t": 50, "b": 50},  # Ajustes para as margens
            showlegend=False,  # Ocultar legenda
            height=600,  # Altura do gráfico
            dragmode="pan",  # Permite arrastar para rolar no gráfico
            xaxis=dict(showgrid=False, range=[0, df_sorted['valor_receita'].max() * 1.1]),  # Ajuste do zoom inicial
            yaxis=dict(showgrid=False),  # Remove as linhas de grade no eixo Y
        )

        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig)
        
def tabela_pais():
    # Agrupando os dados por 'pais' e realizando as agregações
    tabela = df.groupby('pais').agg(
        valor_receita=('valor_receita', 'sum'),  # Soma do valor da receita por país
        quantidade=('quantidade', 'sum'),        # Soma da quantidade por país
        valor_unitario=('valor_unitario', 'max')  # Máximo do valor unitário por país
    ).reset_index()

    # Ordenando os países por valor_receita em ordem crescente
    tabela = tabela.sort_values(by='valor_receita', ascending=False)

    # Exibindo a tabela no Streamlit
    st.dataframe(tabela)
        
def barra_produto():
        # Agrupando por 'produto' e somando 'valor_receita' e 'quantidade', além de calcular a média de 'valor_unitario'
        df_sorted = df.groupby('produtos').agg(
            valor_receita=('valor_receita', 'sum'),  # Soma do valor da receita por país
            quantidade=('quantidade', 'sum'),        # Soma da quantidade por país
            valor_unitario=('valor_unitario', 'max')  # Máximo do valor unitário por país
        ).reset_index()

        # Ordenando os países por valor_receita em ordem decrescente
        df_sorted = df_sorted.sort_values(by='valor_receita', ascending=True)

        # Criando o gráfico de barras horizontais
        fig = px.bar(df_sorted,
                    x="valor_receita",  # Eixo X é o valor da receita
                    y="produtos",  # Eixo Y são os países
                    orientation="h",  # Barras horizontais
                    hover_name="produtos",  # Nome do país ao passar o mouse
                    hover_data=["quantidade", "valor_unitario"],  # Dados extras ao passar o mouse
                    title="Receita por Produto",  # Título do gráfico
                    labels={"valor_receita": "Valor da Receita", "produtos": "Produtos"},  # Rótulos personalizados
                    color_discrete_sequence=["#1f77b4"])  # Cor única azul (ajustada para um tom de azul específico)

        # Adicionando rótulos de dados ao lado de cada barra
        fig.update_traces(text=df_sorted['valor_receita'], textposition='outside')  # Mostra o valor das receitas ao lado da barra

        # Ajustando o layout para permitir rolagem horizontal e remover legenda
        fig.update_layout(
            xaxis_title="Valor da Receita",
            yaxis_title="Produto",
            margin={"l": 150, "r": 50, "t": 50, "b": 50},  # Ajustes para as margens
            showlegend=False,  # Ocultar legenda
            height=600,  # Altura do gráfico
            dragmode="pan",  # Permite arrastar para rolar no gráfico
            xaxis=dict(showgrid=False, range=[0, df_sorted['valor_receita'].max() * 1.1]),  # Ajuste do zoom inicial
            yaxis=dict(showgrid=False),  # Remove as linhas de grade no eixo Y
        )

        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig)
        
def tabela_produto():
    # Agrupando os dados por 'pais' e realizando as agregações
    tabela = df.groupby('produtos').agg(
        valor_receita=('valor_receita', 'sum'),  # Soma do valor da receita por país
        quantidade=('quantidade', 'sum'),        # Soma da quantidade por país
        valor_unitario=('valor_unitario', 'max')  # Máximo do valor unitário por país
    ).reset_index()

    # Ordenando os países por valor_receita em ordem crescente
    tabela = tabela.sort_values(by='valor_receita', ascending=False)

    # Exibindo a tabela no Streamlit
    st.dataframe(tabela)
        
def barra_cliente():
    # Garantir que 'id_cliente' seja tratado como string
    df['id_cliente'] = df['id_cliente'].astype(str)
    
    # Agrupando por 'id_cliente' e somando 'valor_receita' e 'quantidade', além de calcular o máximo de 'valor_unitario'
    df_sorted = df.groupby('id_cliente').agg(
        valor_receita=('valor_receita', 'sum'),  # Soma do valor da receita por cliente
        quantidade=('quantidade', 'sum'),        # Soma da quantidade por cliente
        valor_unitario=('valor_unitario', 'max')  # Máximo do valor unitário por cliente
    ).reset_index()

    # Ordenando os clientes por 'valor_receita' em ordem decrescente
    df_sorted = df_sorted.sort_values(by='valor_receita', ascending=False)

    # Criando o gráfico de barras horizontais
    fig = px.bar(df_sorted,
                 x="valor_receita",  # Eixo X é o valor da receita
                 y="id_cliente",  # Eixo Y são os clientes
                 orientation="h",  # Barras horizontais
                 hover_name="id_cliente",  # Nome do cliente ao passar o mouse
                 hover_data=["quantidade", "valor_unitario"],  # Dados extras ao passar o mouse
                 title="Receita por Cliente",  # Título do gráfico
                 labels={"valor_receita": "Valor da Receita", "id_cliente": "Clientes"},  # Rótulos personalizados
                 color_discrete_sequence=["#1f77b4"])  # Cor única azul (ajustada para um tom de azul específico)

    # Adicionando rótulos de dados ao lado de cada barra
    fig.update_traces(text=df_sorted['valor_receita'], textposition='outside')  # Mostra o valor das receitas ao lado da barra

    # Ajustando o layout para permitir rolagem horizontal e remover legenda
    fig.update_layout(
        xaxis_title="Valor da Receita",
        yaxis_title="Clientes",
        margin={"l": 150, "r": 50, "t": 50, "b": 50},  # Ajustes para as margens
        showlegend=False,  # Ocultar legenda
        height=600,  # Altura do gráfico
        dragmode="pan",  # Permite arrastar para rolar no gráfico
        xaxis=dict(showgrid=False, range=[0, df_sorted['valor_receita'].max() * 1.1]),  # Ajuste do zoom inicial
        yaxis=dict(showgrid=False),  # Remove as linhas de grade no eixo Y
    )

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig)
    
def tabela_cliente():
    # Agrupando os dados por 'pais' e realizando as agregações
    tabela = df.groupby('id_cliente').agg(
        valor_receita=('valor_receita', 'sum'),  # Soma do valor da receita por país
        quantidade=('quantidade', 'sum'),        # Soma da quantidade por país
        valor_unitario=('valor_unitario', 'max')  # Máximo do valor unitário por país
    ).reset_index()

    # Ordenando os países por valor_receita em ordem crescente
    tabela = tabela.sort_values(by='valor_receita', ascending=False)

    # Exibindo a tabela no Streamlit
    st.dataframe(tabela)
with col2:
    
    
    col1b,col2b,col3b = st.columns(3)
    
   
    
    but_pais = col1b.button("Pais")
    
    if but_pais:
        barra_pais()
        
    
    but_produto = col2b.button("Produto")
    
    if but_produto:
        barra_produto()
    
    
    but_cliente = col3b.button("Cliente")
    
    if but_cliente:
        barra_cliente()
        
with col3:
    if but_pais:
        tabela_pais()
        
    if but_produto:
       tabela_produto()
    
    if but_cliente:
        tabela_cliente()
    
    
# Certifique-se de que 'valor_receita' seja numérico e não tenha NaN
df['valor_receita'] = df['valor_receita'].fillna(0)  # Substitui NaN por 0
df['valor_receita'] = df['valor_receita'].astype(float)  # Garantindo que é float

# Garantir que a coluna 'pais' está correta (nome do país ou código ISO de 2 letras)
df['pais'] = df['pais'].astype(str)  # Garantindo que está em formato de texto

def mapa():
    # Substituindo valores NaN por 0 e garantindo que 'valor_receita' seja float
    df['valor_receita'] = df['valor_receita'].fillna(0).astype(float)

    # Substituindo valores negativos de 'valor_receita' por 0
    df['valor_receita'] = df['valor_receita'].apply(lambda x: max(0, x))

    # Garantindo que a coluna 'pais' está correta
    df['pais'] = df['pais'].astype(str)
    
    # Agregando os dados por país
    df_aggregated = df.groupby('pais').agg(
        valor_receita=('valor_receita', 'sum'),  # Soma do valor da receita por país
        quantidade=('quantidade', 'sum'),        # Soma das quantidades por país
        valor_unitario=('valor_unitario', 'mean')  # Média do valor unitário por país
    ).reset_index()

    # Criação do gráfico
    fig = px.scatter_geo(df_aggregated,
                         locations="pais",  # Coluna com países
                         size="valor_receita",  # Tamanho das bolhas com base no valor da receita
                         color="valor_receita",  # Cor das bolhas com base na receita
                         hover_name="pais",  # Nome do país ao passar o mouse
                         hover_data=["quantidade", "valor_unitario"],  # Dados extras ao passar o mouse
                         size_max=100,  # Tamanho máximo das bolhas
                         projection="equirectangular",  # Projeção do mapa
                         title="Mapa de Bolhas de Receita por País",
                         locationmode='country names',  # Especifica o modo de localização como nomes de países
                         color_continuous_scale="Viridis"  # Gradiente de cor para as bolhas
                        )

    # Ajustando a visualização para exibir as bolhas corretamente
    fig.update_traces(marker=dict(
        line=dict(width=1, color='darkgreen'),  # Borda verde para as bolhas
        opacity=0.7  # Definindo a opacidade para dar um visual mais suave
    ))

    # Ajustando o layout para dar um toque mais bonito
    fig.update_layout(
        mapbox_style="carto-positron",  # Estilo do mapa
        height=800,  # Ajuste de altura do gráfico
        showlegend=False,  # Ocultar legenda para um visual mais limpo
        title={'text': "Mapa de Bolhas de Receita por País", 'x': 0.5, 'xanchor': 'center'},  # Centralizando o título
        geo=dict(
            showland=True,  # Mostrar as áreas de terra
            landcolor="white",  # Cor de fundo da terra
            showlakes=True,  # Mostrar lagos
            lakecolor="lightblue"  # Cor dos lagos,
        )
    )

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig)

mapa = mapa()

# Renomeando as colunas
tabela = df.drop(columns=['id'])  # Remover a coluna 'id'
tabela.columns = [
    'Fatura', 'Cod Produto', 'Produtos', 'Quantidade',
    'Data Hora Fatura', 'Data Fatura', 'Valor Unitário', 'Valor Fatura',
    'Número Cliente', 'Pais', 'Tipo Receita'
]

extrato = st.expander("Extrato")

extrato.dataframe(tabela)










