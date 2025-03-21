from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],  # Permite solicitações do frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Diretório para salvar os arquivos enviados
UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Rota para upload de arquivos
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Salva o arquivo no diretório de uploads
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return JSONResponse(
            status_code=200,
            content={"message": "Arquivo recebido com sucesso!", "filename": file.filename},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}")

# Rota para listar arquivos enviados
@app.get("/files")
async def list_files():
    try:
        # Lista os arquivos no diretório de uploads
        files = os.listdir(UPLOAD_DIR)
        return JSONResponse(
            status_code=200,
            content=files,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar arquivos: {str(e)}")