from fastapi import FastAPI
import logging
from app.startup.downloader import baixar_operadoras_csv
from app.startup.load_data import carregar_dados
from app.config import OPERADORAS_URL, PASTA_DOWNLOAD

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """Executa as funções de download e carregamento de dados na inicialização."""
    try:
        logger.info("Iniciando download dos dados...")
        pasta_destino = f"{PASTA_DOWNLOAD}/operadoras"
        arquivo_csv = baixar_operadoras_csv(OPERADORAS_URL, pasta_destino)

        if arquivo_csv:
            logger.info(f"Download concluído: {arquivo_csv}")

            logger.info("Iniciando carregamento de dados para o banco...")
            carregar_dados()
            logger.info("Carregamento de dados concluído.")
        else:
            logger.error("Falha ao baixar arquivo CSV. Carregamento de dados não foi executado.")
    except Exception as e:
        logger.error(f"Erro durante a inicialização: {str(e)}")


@app.get("/")
def read_root():
    return {"mensagem": "Olá, FastAPI!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}