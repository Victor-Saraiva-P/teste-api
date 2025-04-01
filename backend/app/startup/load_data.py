import logging
import mysql.connector
import os

from app.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def carregar_dados():
    """
    Carrega os dados somente se a tabela 'operadoras' não existir ou estiver vazia.
    Agora, o LOAD DATA LOCAL INFILE está definido diretamente no código.
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

        # 1) Verificar se a tabela 'operadoras' existe
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = %s AND table_name = 'operadoras'
        """, (DB_NAME,))
        tabela_existe = cursor.fetchone()[0] > 0

        # 2) Criar a tabela se não existir
        if not tabela_existe:
            logging.info("A tabela 'operadoras' não existe. Criando...")
            query_create_table = """
            CREATE TABLE IF NOT EXISTS operadoras (
                registro_ans VARCHAR(20) PRIMARY KEY,
                cnpj VARCHAR(20),
                razao_social VARCHAR(255),
                nome_fantasia VARCHAR(255),
                modalidade VARCHAR(100),
                logradouro VARCHAR(255),
                numero VARCHAR(20),
                complemento VARCHAR(100),
                bairro VARCHAR(100),
                cidade VARCHAR(100),
                uf CHAR(2),
                cep VARCHAR(10),
                ddd VARCHAR(5),
                telefone VARCHAR(20),
                fax VARCHAR(20),
                email VARCHAR(100),
                representante VARCHAR(255),
                cargo_representante VARCHAR(100),
                regiao_de_comercializacao TINYINT,  -- <--- nova coluna
                data_registro DATE
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
            """
            cursor.execute(query_create_table)
            conn.commit()
            logging.info("Tabela 'operadoras' criada com sucesso.")
        else:
            # Se a tabela existe, verificar se ela contém registros
            cursor.execute("SELECT COUNT(*) FROM operadoras")
            registros = cursor.fetchone()[0]
            if registros > 0:
                logging.info(f"A tabela 'operadoras' já contém {registros} registros. Pulando carregamento.")
                return  # Não faz o LOAD DATA, pois já tem dados

        # 3) Se a tabela estiver vazia, faz o LOAD DATA
        caminho_csv_operadoras = os.path.join("downloads", "operadoras", "Relatorio_cadop.csv")
        if not os.path.exists(caminho_csv_operadoras):
            logging.warning(f"O arquivo {caminho_csv_operadoras} não foi encontrado.")
            return

        logging.info(f"Carregando dados do arquivo: {caminho_csv_operadoras}")

        # Aqui está o trecho "embutido" do LOAD DATA
        load_data_sql = """
        LOAD DATA LOCAL INFILE '%s'
        INTO TABLE operadoras
        CHARACTER SET utf8mb4
        FIELDS TERMINATED BY ';'
        OPTIONALLY ENCLOSED BY '"'
        LINES TERMINATED BY '\\n'
        IGNORE 1 LINES
        (
          registro_ans,
          cnpj,
          razao_social,
          nome_fantasia,
          modalidade,
          logradouro,
          numero,
          complemento,
          bairro,
          cidade,
          uf,
          cep,
          ddd,
          telefone,
          fax,
          email,
          representante,
          cargo_representante,
          regiao_de_comercializacao,
          @data_registro
        )
        SET data_registro = CASE
            WHEN @data_registro = '' THEN NULL
            ELSE STR_TO_DATE(TRIM(@data_registro), '%%Y-%%m-%%d')
        END;
        """

        # Substitui '%s' pelo caminho do CSV (corrigindo barras invertidas)
        sql_completo = load_data_sql % caminho_csv_operadoras.replace('\\', '/')

        # Executa o LOAD DATA
        cursor.execute(sql_completo)
        conn.commit()

        logging.info("Dados carregados para operadoras com sucesso.")

    except Exception as erro:
        logging.error(f"Erro ao carregar dados: {erro}")
    finally:
        if conn:
            conn.close()
