<script setup lang="ts">
import { ref, reactive, defineEmits } from 'vue';
import { OperadorasFilter } from '../types/operadora';

const emit = defineEmits<{
  filter: [filter: OperadorasFilter]
}>();

// Available UFs for the dropdown
const ufs = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
             'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
             'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'];

const filter = reactive<OperadorasFilter>({
  uf: '',
  cidade: '',
  razao_social: '',
  page: 1,
  page_size: 5,
  sort_by: 'razao_social',
  sort_order: 'asc'
});

// Sorting options
const sortOptions = [
  { value: 'razao_social', label: 'Razão Social' },
  { value: 'nome_fantasia', label: 'Nome Fantasia' },
  { value: 'data_registro', label: 'Data de Registro' },
  { value: 'cidade', label: 'Cidade' },
  { value: 'uf', label: 'UF' }
];

const applyFilter = () => {
  emit('filter', { ...filter });
};

const resetFilter = () => {
  filter.uf = '';
  filter.cidade = '';
  filter.razao_social = '';
  filter.page = 1;
  filter.sort_by = 'razao_social';
  filter.sort_order = 'asc';
  emit('filter', { ...filter });
};
</script>

<template>
  <div class="filter-container">
    <h2>Filtros</h2>
    <div class="filter-form">
      <div class="filter-row">
        <div class="filter-item">
          <label for="uf">UF</label>
          <select id="uf" v-model="filter.uf">
            <option value="">Todos</option>
            <option v-for="uf in ufs" :key="uf" :value="uf">{{ uf }}</option>
          </select>
        </div>
        
        <div class="filter-item">
          <label for="cidade">Cidade</label>
          <input id="cidade" type="text" v-model="filter.cidade" placeholder="Filtrar por cidade">
        </div>
        
        <div class="filter-item">
          <label for="razao-social">Razão Social</label>
          <input id="razao-social" type="text" v-model="filter.razao_social" placeholder="Filtrar por razão social">
        </div>
      </div>
      
      <div class="filter-row">
        <div class="filter-item">
          <label for="sort-by">Ordenar por</label>
          <select id="sort-by" v-model="filter.sort_by">
            <option v-for="option in sortOptions" :key="option.value" :value="option.value">
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
        
        <div class="filter-item">
          <label for="page-size">Itens por página</label>
          <select id="page-size" v-model="filter.page_size">
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="50">50</option>
          </select>
        </div>
      </div>
      
      <div class="filter-buttons">
        <button class="btn btn-primary" @click="applyFilter">Aplicar Filtros</button>
        <button class="btn btn-secondary" @click="resetFilter">Limpar Filtros</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.filter-container {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.filter-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.filter-item {
  flex: 1;
  min-width: 200px;
  display: flex;
  flex-direction: column;
}

.filter-item label {
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input, select {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.filter-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn {
  padding: 0.6em 1.2em;
  border-radius: 8px;
  border: 1px solid transparent;
  font-size: 1em;
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