# 1. Usar a imagem do Node.js
FROM node:16

# 2. Defina o diretório de trabalho no contêiner
WORKDIR /app

# 3. Rodar o comando para criar o app React (vai criar os arquivos necessários, como package.json)
RUN npx create-react-app .

# 4. Instalar as dependências (no caso do React, isso já deve ter sido feito pelo create-react-app, mas se necessário)
RUN npm install

# 5. Rodar o build da aplicação React (essa etapa prepara o app para produção)
RUN npm run build

# 6. Expor a porta onde o app React vai rodar
EXPOSE 3000

# 7. Rodar o servidor de desenvolvimento
CMD ["npm", "start"]
