# 1. Usar uma versão mais recente do Node.js (Node 18 ou superior)
FROM node:18

# 2. Defina o diretório de trabalho no contêiner
WORKDIR /app

# 3. Copiar apenas o package.json e o package-lock.json (se houver) para o contêiner
COPY package.json /app/
COPY package-lock.json /app/

# 4. Instalar as dependências (isso vai aproveitar o cache se o package.json não mudar)
RUN npm install

# 5. Copiar o restante do código do projeto para o contêiner
COPY . /app/

# 6. Rodar o build da aplicação React (essa etapa prepara o app para produção)
RUN npm run build

# 7. Expor a porta onde o app React vai rodar
EXPOSE 3000

# 8. Rodar o servidor de desenvolvimento
CMD ["npm", "run", "dev"]

