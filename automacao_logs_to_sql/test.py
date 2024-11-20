# Cell 1: Imports e Configurações
import os
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

# Configurações globais
diretorio_principal = "C:/Projetos/Data_Science/Projetos_Data_Science/automacao_logs_to_sql/clientes"
db_usuario = 'root'
db_senha = '123456'
db_host = 'localhost'
db_nome = 'public'
db_tabela = "logs_teste"

# Cell 2: Função para Conectar ao Banco de Dados

def conectar_banco(usuario, senha, host, nome_banco):
    """
    Conecta ao banco de dados MySQL e retorna o engine.
    """
    engine = create_engine(f'mysql+pymysql://{usuario}:{senha}@{host}/{nome_banco}')
    return engine

# Teste da conexão ao banco de dados
try:
    engine = conectar_banco(db_usuario, db_senha, db_host, db_nome)
    with engine.connect() as conn:
        print("Conexão concedida")
except Exception as e:
    print("Erro de conexão:", e)
    

# Cell 3: Função para Extrair Logs de Arquivos

def extrair_logs(diretorio):
    """
    Extrai logs de arquivos .log em subpastas e retorna um DataFrame com as mensagens de log.
    """
    novos_dados = []
    log_messages = []

    log_messages.append("Início da varredura nas pastas dos clientes")
    
    # Percorre todas as pastas e arquivos dentro do diretório principal
    for cliente in os.listdir(diretorio):
        caminho_cliente = os.path.join(diretorio, cliente)
        
        # Verifica se é uma pasta (cliente)
        if os.path.isdir(caminho_cliente):
            log_messages.append(f"Processando pasta do cliente: {cliente}")
            
            # Para cada arquivo .log dentro da pasta do cliente
            for arquivo in os.listdir(caminho_cliente):
                if arquivo.endswith('.log'):
                    caminho_arquivo = os.path.join(caminho_cliente, arquivo)
                    log_messages.append(f"   Lendo arquivo: {arquivo}")
                    
                    # Abre o arquivo .log e lê linha por linha
                    with open(caminho_arquivo, 'r', encoding='latin-1') as file:
                        for linha in file:
                            if len(linha) >= 19:
                                # Extrai a data e hora dos primeiros 19 caracteres
                                data_hora = linha[:19]
                                # Extrai o log (resto da linha)
                                log = linha[19:].strip()
                                
                                # Adiciona os dados na lista
                                novos_dados.append([cliente, arquivo, data_hora, log])

    # Cria um DataFrame com os dados coletados
    df = pd.DataFrame(novos_dados, columns=['CLIENTE', 'DOCUMENTO', 'DATA_HORA', 'LOG'])
    df["DATA_HORA"] = pd.to_datetime(df["DATA_HORA"], errors='coerce')  # Converte DATA_HORA para datetime
    return df, log_messages

# Cell 4: Funções para Manipulação do Banco de Dados

def truncar_tabela(engine, tabela):
    """
    Trunca a tabela especificada.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text(f"TRUNCATE TABLE {tabela}"))
            print("Tabela truncada com sucesso.")
    except Exception as e:
        print(f"Erro no truncate: {e}")

def inserir_dados_banco(df, engine, tabela):
    """
    Insere o DataFrame em uma tabela no banco de dados.
    """
    try:
        df.to_sql(tabela, con=engine, if_exists='append', index=False)
        print("Dados inseridos no banco de dados com sucesso.")
        print(f"Quantidade de registros inseridos: {len(df)}")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir os dados no banco de dados: {e}")

# Cell 5: Função Principal 

def processar_logs(diretorio, tabela, processos):
    """
    Processa logs de um diretório e insere os dados no banco de dados.
    """
    
    engine = conectar_banco(db_usuario, db_senha, db_host, db_nome)
    
    df_logs, log_messages = extrair_logs(diretorio)
    truncar_tabela(engine, tabela)
    inserir_dados_banco(df_logs, engine, tabela)
    
    # Opcional: Imprime as mensagens de log coletadas durante a execução
    if processos == True:
        for log in log_messages:
            print(log)
    print("Terminou com Sucesso")
    
# Executa a função principal
processar_logs(diretorio_principal, db_tabela, processos =  False)

