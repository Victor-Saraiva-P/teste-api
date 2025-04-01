<script setup lang="ts">
import { computed, defineProps, defineEmits } from 'vue';

const props = defineProps<{
  currentPage: number;
  totalPages: number;
}>();

const emit = defineEmits<{
  'update:page': [page: number]
}>();

const pages = computed(() => {
  const pageArray = [];
  const maxVisiblePages = 5;
  
  if (props.totalPages <= maxVisiblePages) {
    // If we have fewer pages than the max visible, show all
    for (let i = 1; i <= props.totalPages; i++) {
      pageArray.push(i);
    }
  } else {
    // Always show first page
    pageArray.push(1);
    
    let startPage = Math.max(2, props.currentPage - 1);
    let endPage = Math.min(props.totalPages - 1, props.currentPage + 1);
    
    // Adjust for edge cases
    if (props.currentPage <= 2) {
      endPage = 4;
    } else if (props.currentPage >= props.totalPages - 1) {
      startPage = props.totalPages - 3;
    }
    
    // Add ellipsis after first page if needed
    if (startPage > 2) {
      pageArray.push('...');
    }
    
    // Add visible page numbers
    for (let i = startPage; i <= endPage; i++) {
      pageArray.push(i);
    }
    
    // Add ellipsis before last page if needed
    if (endPage < props.totalPages - 1) {
      pageArray.push('...');
    }
    
    // Always show last page
    if (props.totalPages > 1) {
      pageArray.push(props.totalPages);
    }
  }
  
  return pageArray;
});

const goToPage = (page: number | string) => {
  if (typeof page === 'number') {
    emit('update:page', page);
  }
};

const goToPreviousPage = () => {
  if (props.currentPage > 1) {
    emit('update:page', props.currentPage - 1);
  }
};

const goToNextPage = () => {
  if (props.currentPage < props.totalPages) {
    emit('update:page', props.currentPage + 1);
  }
};
</script>

<template>
  <div class="pagination-container">
    <button 
      class="pagination-button" 
      :disabled="currentPage === 1" 
      @click="goToPreviousPage"
    >
      &laquo; Anterior
    </button>
    
    <div class="page-numbers">
      <button 
        v-for="(page, index) in pages" 
        :key="index"
        :class="[
          'pagination-button', 
          'page-button', 
          { active: page === currentPage, ellipsis: page === '...' }
        ]"
        :disabled="page === '...'"
        @click="goToPage(page)"
      >
        {{ page }}
      </button>
    </div>
    
    <button 
      class="pagination-button" 
      :disabled="currentPage === totalPages" 
      @click="goToNextPage"
    >
      Próximo &raquo;
    </button>
  </div>
</template>

<style scoped>
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1.5rem;
  gap: 0.5rem;
}

.page-numbers {
  display: flex;
  gap: 0.25rem;
}

.pagination-button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background-color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-button:not(:disabled):hover {
  background-color: #f0f0ff;
  border-color: #646cff;
}

.page-button {
  min-width: 2.5rem;
  text-align: center;
}

.page-button.active {
  background-color: #646cff;
  color: white;
  border-color: #646cff;
}

.page-button.ellipsis {
  border: none;
  background: transparent;
  pointer-events: none;
}
</style>