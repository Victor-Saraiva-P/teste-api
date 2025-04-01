import axios from "axios";
import type { OperadorasFilter, OperadorasResponse } from "../types/operadora";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8080",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

export const OperadorasService = {
  getOperadoras: async (
    filters: OperadorasFilter
  ): Promise<OperadorasResponse> => {
    const params = new URLSearchParams();

    if (filters.uf) params.append("uf", filters.uf);
    if (filters.cidade) params.append("cidade", filters.cidade);
    if (filters.razao_social)
      params.append("razao_social", filters.razao_social);
    params.append("page", filters.page.toString());
    params.append("page_size", filters.page_size.toString());
    if (filters.sort_by) params.append("sort_by", filters.sort_by);
    if (filters.sort_order) params.append("sort_order", filters.sort_order);

    try {
      console.log(
        "API request URL:",
        apiClient.defaults.baseURL + "/operadoras"
      );
      console.log("API request params:", params.toString());

      const response = await apiClient.get("/operadoras", { params });

      console.log("API response data:", response.data);

      return {
        items: response.data.data || [],
        total: response.data.total || 0,
        page: response.data.page || 1,
        page_size: response.data.page_size || 10,
        total_pages: response.data.total_pages || 1,
      };
    } catch (error: any) {
      console.error("API request failed:", error);
      if (error.code === "ECONNREFUSED" || !error.response) {
        throw new Error(
          "Não foi possível conectar ao servidor. Verifique se o backend está em execução."
        );
      }
      throw error;
    }
  },
};
