from typing import Optional

from app.repositories.operadoras_repository import listar_operadoras_paginado


def buscar_operadoras_com_filtros(
        uf: Optional[str],
        cidade: Optional[str],
        razao_social: Optional[str],
        nome_fantasia: Optional[str],
        sort_by: Optional[str],
        sort_order: Optional[str],
        page: int,
        page_size: int
):
    """
    Orquestra a busca paginada das operadoras, com filtros e ordenação.
    Aqui você pode adicionar validações extras se quiser.
    """
    # Exemplo de validação do page_size
    if page_size > 200:
        page_size = 200  # limita

    total, rows = listar_operadoras_paginado(
        uf=uf,
        cidade=cidade,
        razao_social=razao_social,
        nome_fantasia=nome_fantasia,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )
    return total, rows
