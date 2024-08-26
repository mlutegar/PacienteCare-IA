from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dao.view.routes import router

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Origem que você deseja permitir
    allow_credentials=True,
    allow_methods=["*"],  # Métodos HTTP permitidos
    allow_headers=["*"],  # Cabeçalhos HTTP permitidos
)

# Incluir as rotas
app.include_router(router)
