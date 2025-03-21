<template>
  <div>
    <h1>Upload de Arquivo</h1>
    <input type="file" @change="handleFileChange" />
    <button @click="uploadFile">Enviar Arquivo</button>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      file: null,
      message: '',
    };
  },
  methods: {
    handleFileChange(event) {
      this.file = event.target.files[0]; // Pega o arquivo selecionado
    },
    async uploadFile() {
      if (!this.file) {
        this.message = 'Por favor, selecione um arquivo.';
        return;
      }

      const formData = new FormData();
      formData.append('file', this.file); // Adiciona o arquivo ao FormData

      try {
        const response = await fetch('http://localhost:8000/upload', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const result = await response.json();
          this.message = `Arquivo enviado com sucesso: ${result.filename}`;
        } else {
          this.message = 'Erro ao enviar o arquivo.';
        }
      } catch (error) {
        this.message = 'Erro na conexão com o servidor.';
      }
    },
  },
};
</script>

<style scoped>
div {
  margin: 20px;
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
</style>