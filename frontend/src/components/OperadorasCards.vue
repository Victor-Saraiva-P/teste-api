<script setup lang="ts">
import { defineProps } from "vue";
import { Operadora } from "../types/operadora";

defineProps<{
  operadoras: Operadora[];
  loading: boolean;
}>();

const formatDate = (dateString: string): string => {
  if (!dateString) return "-";
  const date = new Date(dateString);
  return new Intl.DateTimeFormat("pt-BR").format(date);
};

const formatPhone = (
  ddd: string | undefined,
  telefone: string | undefined
): string => {
  if (!ddd || !telefone) return "-";
  return `(${ddd}) ${telefone}`;
};
</script>

<template>
  <div class="cards-container">
    <div v-if="loading" class="loading-message">Carregando dados...</div>

    <div v-else-if="operadoras.length === 0" class="no-data-message">
      Nenhuma operadora encontrada
    </div>

    <div v-else class="cards-grid">
      <div
        v-for="operadora in operadoras"
        :key="operadora.registro_ans"
        class="operadora-card"
      >
        <!-- Card Header with Razão Social -->
        <div class="card-header">
          <div class="header-content">
            <h3 class="razao-social">{{ operadora.razao_social }}</h3>
            <div class="registro-ans">ANS: {{ operadora.registro_ans }}</div>
          </div>
        </div>

        <!-- Card Body -->
        <div class="card-body">
          <!-- Basic Info Section -->
          <div class="info-section">
            <h4>Informações Básicas</h4>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">Nome Fantasia</span>
                <span class="info-value">{{
                  operadora.nome_fantasia || "-"
                }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">CNPJ</span>
                <span class="info-value">{{ operadora.cnpj }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Modalidade</span>
                <span class="info-value">{{ operadora.modalidade }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Data de Registro</span>
                <span class="info-value">{{
                  formatDate(operadora.data_registro)
                }}</span>
              </div>
            </div>
          </div>

          <!-- Contact Info Section -->
          <div class="info-section">
            <h4>Contato</h4>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">Telefone</span>
                <span class="info-value">{{
                  formatPhone(operadora.ddd, operadora.telefone)
                }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Email</span>
                <span class="info-value">{{ operadora.email || "-" }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Representante</span>
                <span class="info-value">{{
                  operadora.representante || "-"
                }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Cargo</span>
                <span class="info-value">{{
                  operadora.cargo_representante || "-"
                }}</span>
              </div>
            </div>
          </div>

          <!-- Address Section -->
          <div class="info-section">
            <h4>Endereço</h4>
            <div class="address">
              <p>
                {{ operadora.logradouro || "-" }}, {{ operadora.numero || "-" }}
                {{ operadora.complemento ? `, ${operadora.complemento}` : "" }}
              </p>
              <p>
                {{ operadora.bairro || "-" }} - {{ operadora.cidade }}/{{
                  operadora.uf
                }}
              </p>
              <p>CEP: {{ operadora.cep || "-" }}</p>
            </div>
          </div>
        </div>

        <!-- Card Footer -->
        <div class="card-footer">
          <div class="regiao">
            <span
              >Região de Comercialização:
              {{ operadora.regiao_de_comercializacao || "-" }}</span
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cards-container {
  width: 100%;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.operadora-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.operadora-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-header {
  background-color: #646cff;
  color: white;
  padding: 1rem;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.razao-social {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  line-height: 1.4;
}

.registro-ans {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  align-self: flex-start;
}

.card-body {
  padding: 1rem;
  flex: 1;
}

.info-section {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.info-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.info-section h4 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1rem;
  font-weight: 600;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.7rem;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-label {
  font-size: 0.75rem;
  color: #666;
  margin-bottom: 0.2rem;
}

.info-value {
  font-size: 0.9rem;
}

.address p {
  margin: 0.2rem 0;
  font-size: 0.9rem;
}

.card-footer {
  background-color: #f5f5f5;
  padding: 0.75rem 1rem;
  font-size: 0.85rem;
  color: #555;
}

.loading-message,
.no-data-message {
  text-align: center;
  padding: 2rem;
  font-style: italic;
  color: #777;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .cards-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }

  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
