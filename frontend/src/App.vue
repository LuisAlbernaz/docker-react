<template>
  <div id="app">
    <h1>Upload de Arquivo</h1>
    <input type="file" @change="handleFileChange" />
    <button @click="uploadFile">Enviar Arquivo</button>

    <!-- Mensagem de status -->
    <p v-if="message" :class="{ 'success': isSuccess, 'error': isError }">
      {{ message }}
    </p>

    <!-- Lista de arquivos enviados -->
    <div v-if="uploadedFiles.length > 0">
      <h2>Arquivos Enviados</h2>
      <ul>
        <li v-for="file in uploadedFiles" :key="file">
          {{ file }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      file: null, // Arquivo selecionado
      message: '', // Mensagem de status
      isSuccess: false, // Indica se a mensagem é de sucesso
      isError: false, // Indica se a mensagem é de erro
      uploadedFiles: [], // Lista de arquivos enviados
    };
  },
  methods: {
    // Captura o arquivo selecionado
    handleFileChange(event) {
      this.file = event.target.files[0];
    },

    // Envia o arquivo para o backend
async uploadFile() {
  if (!this.file) {
    this.showMessage('Por favor, selecione um arquivo.', 'error');
    return;
  }

  const formData = new FormData();
  formData.append('file', this.file); // Adiciona o arquivo ao FormData

  console.log('Arquivo selecionado:', this.file.name); // Log do nome do arquivo
  console.log('Preparando para enviar o arquivo...'); // Log de preparação

  try {
    console.log('Enviando arquivo para o backend...'); // Log antes de enviar
    const response = await fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData,
    });

    console.log('Resposta do backend:', response); // Log da resposta do backend

    if (response.ok) {
      const result = await response.json();
      console.log('Arquivo enviado com sucesso:', result); // Log de sucesso
      this.showMessage(`Arquivo enviado com sucesso: ${result.filename}`, 'success');
      this.fetchUploadedFiles(); // Atualiza a lista de arquivos
    } else {
      const errorResponse = await response.json(); // Captura a resposta de erro
      console.error('Erro ao enviar o arquivo. Status:', response.status, 'Resposta:', errorResponse); // Log de erro
      this.showMessage('Erro ao enviar o arquivo.', 'error');
    }
  } catch (error) {
    console.error('Erro na conexão com o servidor:', error); // Log de erro de conexão
    this.showMessage('Erro na conexão com o servidor.', 'error');
  }
},

    // Exibe uma mensagem de status
    showMessage(message, type) {
      this.message = message;
      this.isSuccess = type === 'success';
      this.isError = type === 'error';

      // Limpa a mensagem após 5 segundos
      setTimeout(() => {
        this.message = '';
        this.isSuccess = false;
        this.isError = false;
      }, 5000);
    },

    // Busca a lista de arquivos enviados
    async fetchUploadedFiles() {
      try {
        const response = await fetch('http://localhost:8000/files');
        if (response.ok) {
          const files = await response.json();
          this.uploadedFiles = files;
        } else {
          this.showMessage('Erro ao carregar a lista de arquivos.', 'error');
        }
      } catch (error) {
        this.showMessage('Erro na conexão com o servidor.', 'error');
      }
    },
  },
  // Carrega a lista de arquivos ao montar o componente
  mounted() {
    this.fetchUploadedFiles();
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
}

input {
  margin-bottom: 10px;
}

button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #369f6e;
}

.success {
  color: green;
}

.error {
  color: red;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 5px 0;
}
</style>