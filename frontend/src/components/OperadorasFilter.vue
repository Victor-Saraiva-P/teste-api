<script setup lang="ts">
import { ref, reactive, defineEmits } from "vue";
import { OperadorasFilter } from "../types/operadora";

const emit = defineEmits<{
  filter: [filter: OperadorasFilter];
}>();

// UFs
const ufs = [
  "AC",
  "AL",
  "AP",
  "AM",
  "BA",
  "CE",
  "DF",
  "ES",
  "GO",
  "MA",
  "MT",
  "MS",
  "MG",
  "PA",
  "PB",
  "PR",
  "PE",
  "PI",
  "RJ",
  "RN",
  "RS",
  "RO",
  "RR",
  "SC",
  "SP",
  "SE",
  "TO",
];

const filter = reactive<OperadorasFilter>({
  uf: "",
  cidade: "",
  razao_social: "",
  page: 1,
  // FIXO: Número de itens por página definido como constante (10)
  page_size: 10,
  sort_by: "razao_social",
  sort_order: "asc",
});

// Sorting options
const sortOptions = [
  { value: "razao_social", label: "Razão Social" },
  { value: "nome_fantasia", label: "Nome Fantasia" },
  { value: "data_registro", label: "Data de Registro" },
  { value: "cidade", label: "Cidade" },
  { value: "uf", label: "UF" },
];

const applyFilter = () => {
  emit("filter", { ...filter });
};

const resetFilter = () => {
  filter.uf = "";
  filter.cidade = "";
  filter.razao_social = "";
  filter.page = 1;
  filter.sort_by = "razao_social";
  filter.sort_order = "asc";
  emit("filter", { ...filter });
};
</script>

<template>
  <div class="filter-container">
    <!-- Barra de pesquisa por razão social destacada -->
    <div class="search-bar">
      <input
        id="razao-social"
        type="text"
        v-model="filter.razao_social"
        placeholder="Pesquisar por razão social..."
        @keyup.enter="applyFilter"
      />
      <button class="search-button" @click="applyFilter">Buscar</button>
    </div>

    <div class="filter-toggles">
      <details class="filter-details">
        <summary>Filtros adicionais</summary>
        <div class="filter-form">
          <div class="filter-row">
            <div class="filter-item">
              <label for="uf">UF</label>
              <select id="uf" v-model="filter.uf">
                <option value="">Todos</option>
                <option v-for="uf in ufs" :key="uf" :value="uf">
                  {{ uf }}
                </option>
              </select>
            </div>

            <div class="filter-item">
              <label for="cidade">Cidade</label>
              <input
                id="cidade"
                type="text"
                v-model="filter.cidade"
                placeholder="Filtrar por cidade"
              />
            </div>
          </div>

          <div class="filter-row">
            <div class="filter-item">
              <label for="sort-by">Ordenar por</label>
              <select id="sort-by" v-model="filter.sort_by">
                <option
                  v-for="option in sortOptions"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </div>

            <div class="filter-item">
              <label for="sort-order">Ordem</label>
              <select id="sort-order" v-model="filter.sort_order">
                <option value="asc">Crescente</option>
                <option value="desc">Decrescente</option>
              </select>
            </div>
          </div>

          <div class="filter-buttons">
            <button class="btn btn-primary" @click="applyFilter">
              Aplicar
            </button>
            <button class="btn btn-secondary" @click="resetFilter">
              Limpar
            </button>
          </div>
        </div>
      </details>
    </div>
  </div>
</template>

<style scoped>
.filter-container {
  background-color: white;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Estilo mais proeminente para a barra de pesquisa */
.search-bar {
  display: flex;
  margin-bottom: 1rem;
}

.search-bar input {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid #e2e2e2;
  border-radius: 8px 0 0 8px;
  font-size: 1.1rem;
  transition: border-color 0.3s;
}

.search-bar input:focus {
  outline: none;
  border-color: #646cff;
}

.search-button {
  background-color: #646cff;
  color: white;
  border: none;
  border-radius: 0 8px 8px 0;
  padding: 0 1.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #535bf2;
}

/* Filtros adicionais em um menu colapsável */
.filter-toggles {
  width: 100%;
}

.filter-details {
  width: 100%;
}

summary {
  cursor: pointer;
  padding: 0.5rem 0;
  color: #646cff;
  font-weight: 500;
  user-select: none;
}

summary:focus {
  outline: none;
}

.filter-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.filter-item {
  flex: 1;
  min-width: 180px;
  display: flex;
  flex-direction: column;
}

.filter-item label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  font-size: 0.85rem;
  color: #666;
}

input,
select {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.btn {
  padding: 0.5em 1em;
  border-radius: 4px;
  border: 1px solid transparent;
  font-size: 0.9em;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s;
}

.btn-primary {
  background-color: #646cff;
  color: white;
}

.btn-primary:hover {
  background-color: #535bf2;
}

.btn-secondary {
  background-color: #e2e2e2;
  color: #333;
}

.btn-secondary:hover {
  background-color: #d0d0d0;
}
</style>
