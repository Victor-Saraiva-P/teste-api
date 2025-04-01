export interface Operadora {
  registro_ans: string;
  cnpj: string;
  razao_social: string;
  nome_fantasia: string;
  modalidade: string;
  logradouro?: string;
  numero?: string;
  complemento?: string;
  bairro?: string;
  cidade: string;
  uf: string;
  cep?: string;
  ddd?: string;
  telefone?: string;
  fax?: string;
  email?: string;
  representante?: string;
  cargo_representante?: string;
  regiao_de_comercializacao?: number;
  data_registro: string;
}

export interface OperadorasResponse {
  items: Operadora[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface OperadorasFilter {
  uf?: string;
  cidade?: string;
  razao_social?: string;
  page: number;
  page_size: number;
  sort_by?: string;
  sort_order?: "asc" | "desc";
}
