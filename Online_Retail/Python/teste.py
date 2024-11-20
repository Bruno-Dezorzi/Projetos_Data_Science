import plotly.express as px
import pandas as pd
import streamlit as st

# Exemplo de dados (substitua com seus dados)
df = pd.DataFrame({
    'pais': ['United Kingdom', 'USA', 'Germany', 'France', 'Italy', 'Brazil'],
    'valor_receita': [100000, 250000, 150000, 120000, 180000, 80000],
    'quantidade': [150, 300, 200, 180, 250, 100],
    'valor_unitario': [10, 12, 15, 13, 11, 8]
})

def mapa():
    # Substituindo valores NaN por 0 e garantindo que 'valor_receita' seja float
    df['valor_receita'] = df['valor_receita'].fillna(0).astype(float)

    # Substituindo valores negativos de 'valor_receita' por 0, pois o tamanho não pode ser negativo
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
                         hover_name="pais",  # Nome do país ao passar o mouse
                         hover_data=["quantidade", "valor_unitario"],  # Dados extras ao passar o mouse
                         size_max=100,  # Tamanho máximo das bolhas
                         projection="natural earth",  # Projeção do mapa
                         title="Mapa de Bolhas de Receita por País",
                         locationmode='country names')  # Especifica o modo de localização como nomes de países

    # Ajustando a visualização para exibir as bolhas corretamente
    fig.update_layout(
        mapbox_style="carto-positron",  # Estilo do mapa
        height=800,  # Ajuste de altura do gráfico
        showlegend=False  # Ocultar legenda para um visual mais limpo
    )

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig)

# Chamar a função mapa()
mapa()
