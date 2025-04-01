import logging

import mysql.connector

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from sql_util import ler_sql_arquivo


def carregar_dados():
    """
    Carrega os dados dos CSVs para as tabelas demonstracoes_contabeis e operadoras
    usando o comando LOAD DATA LOCAL INFILE.
    """
    logging.info("Carregando dados para as tabelas...")
    conn = None

    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            charset='utf8mb4',
            allow_local_infile=True
        )
        cursor = conn.cursor()

        # --- Carregar dados para operadoras ---
        caminho_csv_operadoras = "downloads/operadoras/Relatorio_cadop.csv"
        logging.info(f"Carregando dados do arquivo: {caminho_csv_operadoras}")
        query_load_operadoras = ler_sql_arquivo("load_operadoras.sql")
        cursor.execute(query_load_operadoras % caminho_csv_operadoras.replace('\\', '/'))
        conn.commit()
        logging.info("Dados carregados para operadoras com sucesso.")

    except Exception as erro:
        logging.error(f"Erro ao carregar dados: {erro}")
    finally:
        if conn:
            conn.close()