from typing import Optional
from app.database.connection_db import get_connection

def listar_operadoras_paginado(
    uf: Optional[str] = None,
    cidade: Optional[str] = None,
    razao_social: Optional[str] = None,
    nome_fantasia: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
    page: int = 1,
    page_size: int = 50
):
    """
    Retorna dados paginados de operadoras filtrados por UF, cidade, razao_social, nome_fantasia.
    Também permite ordenar por 'sort_by' e 'sort_order'.

    Retorna: (total, rows), onde:
      total = quantidade total de registros após aplicar os filtros
      rows  = lista de dicionários com os registros paginados
    """

    # Lista de condições e parâmetros para WHERE
    conditions = []
    params = []

    if uf:
        conditions.append("uf = %s")
        params.append(uf.strip())

    if cidade:
        conditions.append("cidade LIKE %s")
        params.append(f"%{cidade.strip()}%")

    if razao_social:
        conditions.append("razao_social LIKE %s")
        params.append(f"%{razao_social.strip()}%")

    if nome_fantasia:
        conditions.append("nome_fantasia LIKE %s")
        params.append(f"%{nome_fantasia.strip()}%")

    # Monta a query base
    base_query = "FROM operadoras WHERE 1=1"
    if conditions:
        base_query += " AND " + " AND ".join(conditions)

    # Query para contar quantos registros há (sem LIMIT/OFFSET)
    count_query = f"SELECT COUNT(*) as total {base_query}"

    # Query final para retornar os dados
    data_query = f"SELECT * {base_query}"

    # sorting
    valid_sort_fields = ["uf", "cidade", "razao_social", "nome_fantasia", "data_registro"]
    if sort_by in valid_sort_fields:
        # Garante que sort_order seja asc ou desc
        if sort_order not in ["asc", "desc"]:
            sort_order = "asc"
        data_query += f" ORDER BY {sort_by} {sort_order}"
    else:
        # Defina um sort padrão (ex.: razao_social asc) se não houver sort_by
        data_query += " ORDER BY razao_social ASC"

    # Paginação
    offset = (page - 1) * page_size
    data_query += " LIMIT %s OFFSET %s"

    # Agora conectamos ao banco e executamos as queries
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # query de contagem
        cursor.execute(count_query, params)
        total = cursor.fetchone()["total"]

        # query de dados (com limit/offset)
        # adicão page_size e offset
        data_params = params[:]  # copia a lista
        data_params.append(page_size)
        data_params.append(offset)

        cursor.execute(data_query, data_params)
        rows = cursor.fetchall()

        return total, rows

    finally:
        if 'conn' in locals() and conn:
            conn.close()
