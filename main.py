from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dao.view.routes import router
import uvicorn

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mlutegar.github.io"],  # Origem que você deseja permitir
    allow_credentials=True,
    allow_methods=["*"],  # Métodos HTTP permitidos
    allow_headers=["*"],  # Cabeçalhos HTTP permitidos
)

# Incluir as rotas
app.include_router(router)

# Iniciar a aplicação com Uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)