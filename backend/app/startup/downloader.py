import logging
import os
import requests
from bs4 import BeautifulSoup

from app.config import NOME_ARQUIVO_CSV


def obter_sopa(url: str) -> BeautifulSoup:
    resposta = requests.get(url)
    resposta.raise_for_status()
    return BeautifulSoup(resposta.text, "html.parser")


def obter_links_arquivos(url: str, extensao_arquivo: str) -> list:
    sopa = obter_sopa(url)
    links = []
    for a in sopa.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith(extensao_arquivo):
            url_completa = url.rstrip("/") + "/" + href
            links.append(url_completa)
    return links


def baixar_arquivo(url: str, pasta_destino: str) -> str:
    # Cria a pasta de destino, se não existir.
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Define o caminho local do arquivo.
    nome_arquivo_local = os.path.join(pasta_destino, url.split("/")[-1])

    # Se o arquivo já existir, não baixa novamente.
    if os.path.exists(nome_arquivo_local):
        logging.info(f"Arquivo {nome_arquivo_local} já existe. Não será baixado novamente.")
        return nome_arquivo_local

    logging.info(f"Baixando {url} para {nome_arquivo_local}")
    resposta = requests.get(url, stream=True)
    resposta.raise_for_status()
    with open(nome_arquivo_local, 'wb') as f:
        for bloco in resposta.iter_content(chunk_size=8192):
            if bloco:
                f.write(bloco)

    return nome_arquivo_local


def baixar_operadoras_csv(url_base: str, pasta_destino: str):
    logging.info(f"Buscando arquivos CSV na URL: {url_base}")
    links_csv = obter_links_arquivos(url_base, ".csv")
    logging.info(f"Foram encontrados {len(links_csv)} arquivos CSV.")

    # Verifica se existe pelo menos um arquivo
    if not links_csv:
        logging.warning("Nenhum arquivo CSV encontrado.")
        return None

    # Procura especificamente pelo arquivo
    arquivo_desejado = None
    for link in links_csv:
        if link.endswith(NOME_ARQUIVO_CSV):
            arquivo_desejado = link
            logging.info(f"Arquivo Relatorio_cadop.csv encontrado: {arquivo_desejado}")
            break

    # Se não encontrou o arquivo específico, usa o primeiro da lista
    if not arquivo_desejado and links_csv:
        arquivo_desejado = links_csv[0]
        logging.info(
            f"Arquivo Relatorio_cadop.csv não encontrado. Usando o primeiro arquivo disponível: {arquivo_desejado}")

    if arquivo_desejado:
        return baixar_arquivo(arquivo_desejado, pasta_destino)
    else:
        return None
