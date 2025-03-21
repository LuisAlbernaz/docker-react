<template>
  <div id="app">
    <h1>Upload de Arquivo</h1>
    <div v-if="!isAuthenticated">
      <h2>Login</h2>
      <input v-model="username" placeholder="Usuário" />
      <input v-model="password" type="password" placeholder="Senha" />
      <button @click="login">Entrar</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
    <div v-else>
      <h2>Bem-vindo, {{ user.username }}!</h2>
      <input type="file" @change="handleFileChange" />
      <button @click="uploadFile">Enviar Arquivo</button>
      <p v-if="message" :class="{ 'success': isSuccess, 'error': isError }">
        {{ message }}
      </p>
      <div v-if="uploadedFiles.length > 0">
        <h2>Arquivos Enviados</h2>
        <ul>
          <li v-for="file in uploadedFiles" :key="file">
            {{ file }}
          </li>
        </ul>
      </div>
      <button @click="logout">Sair</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      isAuthenticated: false,
      user: {},
      errorMessage: "",
      file: null,
      message: "",
      isSuccess: false,
      isError: false,
      uploadedFiles: [],
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch("http://localhost:8000/token", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: `username=${this.username}&password=${this.password}`,
        });

        if (response.ok) {
          const data = await response.json();
          localStorage.setItem("token", data.access_token);
          this.isAuthenticated = true;
          this.fetchUserData();
          this.fetchUploadedFiles();
        } else {
          this.errorMessage = "Usuário ou senha incorretos.";
        }
      } catch (error) {
        this.errorMessage = "Erro na conexão com o servidor.";
      }
    },
    async fetchUserData() {
      const token = localStorage.getItem("token");
      const response = await fetch("http://localhost:8000/users/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        this.user = await response.json();
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.isAuthenticated = false;
      this.user = {};
    },
    handleFileChange(event) {
      this.file = event.target.files[0];
    },
    async uploadFile() {
      if (!this.file) {
        this.showMessage('Por favor, selecione um arquivo.', 'error');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.file);

      try {
        const token = localStorage.getItem("token");
        const response = await fetch('http://localhost:8000/upload', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        });

        if (response.ok) {
          const result = await response.json();
          this.showMessage(`Arquivo enviado com sucesso: ${result.filename}`, 'success');
          this.fetchUploadedFiles();
        } else {
          const errorResponse = await response.json();
          console.error('Erro ao enviar o arquivo. Status:', response.status, 'Resposta:', errorResponse);
          this.showMessage('Erro ao enviar o arquivo.', 'error');
        }
      } catch (error) {
        console.error('Erro na conexão com o servidor:', error);
        this.showMessage('Erro na conexão com o servidor.', 'error');
      }
    },
    showMessage(message, type) {
      this.message = message;
      this.isSuccess = type === 'success';
      this.isError = type === 'error';

      setTimeout(() => {
        this.message = '';
        this.isSuccess = false;
        this.isError = false;
      }, 5000);
    },
    async fetchUploadedFiles() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch('http://localhost:8000/files', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

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
  mounted() {
    const token = localStorage.getItem("token");
    if (token) {
      this.isAuthenticated = true;
      this.fetchUserData();
      this.fetchUploadedFiles();
    }
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