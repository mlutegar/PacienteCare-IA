from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# Definir modelo de dados para o paciente
class PatientData(BaseModel):
    idade: int
    alergias: str
    procedimentos_anteriores: str
    medicamentos: str
    condicoes_saude: str
    procedimento: str
    toxina: str

@app.post("/predict/")
async def predict(data: PatientData):
    # Simples retorno para testar
    return {"response": f"Recebido dados do paciente: {data.idade} anos, {data.alergias}, {data.procedimentos_anteriores}"}
