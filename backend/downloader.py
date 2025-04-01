import logging
import os
import requests
from bs4 import BeautifulSoup


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

    # Verifica se existe pelo menos dois links e seleciona o segundo.
    if links_csv and len(links_csv) > 1:
        url_segundo = links_csv[1]
        logging.info(f"Selecionado o segundo arquivo: {url_segundo}")
        return baixar_arquivo(url_segundo, pasta_destino)
    else:
        logging.warning("Nenhum segundo arquivo CSV encontrado.")
        return None
