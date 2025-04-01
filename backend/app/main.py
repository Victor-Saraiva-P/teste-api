from fastapi import FastAPI
import logging
from app.controller.operadoras_controller import router as operadoras_router
from app.startup.downloader import baixar_operadoras_csv
from app.startup.load_data import carregar_dados
from app.config import OPERADORAS_URL, PASTA_DOWNLOAD

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# "Montamos" as rotas do APIRouter das operadoras
app.include_router(operadoras_router)

@app.on_event("startup")
async def startup_event():
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
def root():
    return {"mensagem": "API de Operadoras ativa!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
