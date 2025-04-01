from typing import Optional
import math
from fastapi import APIRouter, Query

from app.services.operadoras_service import buscar_operadoras_com_filtros

router = APIRouter()

@router.get("/operadoras")
def get_operadoras(
    uf: Optional[str] = Query(None, description="Filtrar por UF (ex.: SP, MG, RJ)"),
    cidade: Optional[str] = Query(None, description="Filtrar por nome (ou parte) da cidade"),
    razao_social: Optional[str] = Query(None, description="Filtrar por parte da razão social"),
    nome_fantasia: Optional[str] = Query(None, description="Filtrar por parte do nome fantasia"),
    sort_by: Optional[str] = Query(None, description="Campo para ordenar (ex.: 'uf', 'cidade', 'razao_social', 'nome_fantasia')"),
    sort_order: Optional[str] = Query(None, description="asc ou desc"),
    page: int = Query(1, description="Número da página (1-based)"),
    page_size: int = Query(50, description="Quantidade de registros por página")
):
    """
    Retorna operadoras paginadas, filtrando por UF, cidade, razao_social e nome_fantasia.
    Também permite ordenar e paginar.

    Exemplo de uso:
    GET /operadoras?uf=SP&cidade=paulo&razao_social=unimed&sort_by=data_registro&sort_order=asc&page=1&page_size=5
    """
    total, rows = buscar_operadoras_com_filtros(
        uf=uf,
        cidade=cidade,
        razao_social=razao_social,
        nome_fantasia=nome_fantasia,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )

    total_pages = math.ceil(total / page_size) if page_size else 1

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "data": rows
    }
