<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { OperadorasService } from "./services/api";
import { Operadora, OperadorasFilter } from "./types/operadora";
import OperadorasFilterComponent from "./components/OperadorasFilter.vue";
import OperadorasCards from "./components/OperadorasCards.vue";
import OperadorasPagination from "./components/OperadorasPagination.vue";
import operadorasIcon from "./assets/icone-operadores.png";

const operadoras = ref<Operadora[]>([]);
const loading = ref(true);
const totalPages = ref(0);
const currentPage = ref(1);
const totalItems = ref(0);
const error = ref<string | null>(null);

// FIXO: Número de itens por página definido como constante (10)
const ITEMS_PER_PAGE = 10;

const filter = reactive<OperadorasFilter>({
  page: 1,
  page_size: ITEMS_PER_PAGE,
});

const fetchOperadoras = async () => {
  loading.value = true;
  error.value = null;
  try {
    console.log("Fetching operadoras with filter:", filter);
    const response = await OperadorasService.getOperadoras(filter);
    console.log("API response:", response);
    operadoras.value = response.items;
    totalPages.value = response.total_pages;
    currentPage.value = response.page;
    totalItems.value = response.total;
  } catch (err: any) {
    console.error("Error fetching operadoras:", err);
    error.value = err.message || "Erro ao carregar dados";
  } finally {
    loading.value = false;
  }
};

const handleFilter = (newFilter: OperadorasFilter) => {
  // Garantir que o page_size definido pelo componente de filtro não substitua o valor constante
  newFilter.page_size = ITEMS_PER_PAGE;
  Object.assign(filter, newFilter);
  fetchOperadoras();
};

const handlePageChange = (page: number) => {
  filter.page = page;
  fetchOperadoras();
};

onMounted(() => {
  console.log("App component mounted");
  fetchOperadoras();
});
</script>

<template>
  <div class="container">
    <header>
      <div class="header-content">
        <img :src="operadorasIcon" alt="Ícone Operadoras" class="header-icon" />
        <h1>Sistema de Operadoras de Saúde</h1>
      </div>
    </header>

    <main>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <OperadorasFilterComponent @filter="handleFilter" />

      <div class="results-info">
        <p v-if="!loading">
          Exibindo {{ operadoras.length }} de {{ totalItems }} operadoras
          encontradas
        </p>
      </div>

      <OperadorasCards :operadoras="operadoras" :loading="loading" />

      <OperadorasPagination
        v-if="totalPages > 0"
        :current-page="currentPage"
        :total-pages="totalPages"
        @update:page="handlePageChange"
      />
    </main>
  </div>
</template>

<style>
/* Global styles */
body {
  color: #333;
  background-color: #f8f9fa;
  margin: 0;
  min-height: 100vh;
  font-family: "Inter", sans-serif;
}

#app {
  width: 100%;
  margin: 0;
  padding: 0;
  max-width: none;
  text-align: left;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

header {
  margin-bottom: 2rem;
  text-align: center;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.header-icon {
  height: 40px;
  width: auto;
}

header h1 {
  color: #333;
  margin-bottom: 0.5rem;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.results-info {
  margin-bottom: 1rem;
  font-style: italic;
  color: #666;
}

.error-message {
  background-color: #fff2f0;
  border: 1px solid #ffccc7;
  color: #cf1322;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 4px;
}
</style>
