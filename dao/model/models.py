import os
from pydantic import BaseModel
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb

# Configurações de ambiente
os.environ["OPENAI_API_KEY"] = "-"
os.environ["CHROMA_PATH"] = "/home/runner/work/chroma_data"
os.environ["PINECONE_API_KEY"] = "e9cb230e-979e-4c7d-967b-8788ad806bd6"
os.environ["QDRANT_API_KEY"] = "y51snXPq9TJIC8uYJm5_2quxGdx8miv4loSCcBB1a_k8ke_2y03ZgA"

# Modelo de dados para o paciente
class PatientData(BaseModel):
    idade: int
    alergias: str
    procedimentos_anteriores: str
    medicamentos: str
    condicoes_saude: str
    procedimento: str
    toxina: str

# Função de embeddings
def get_embedding_function():
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    return embeddings

# Configuração do cliente ChromaDB
client = chromadb.PersistentClient(
    path=os.environ['CHROMA_PATH'],
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

# Instância do banco de dados ChromaDB
db = Chroma(
    client=client, collection_name="iamed",
    persist_directory=os.environ['CHROMA_PATH'], embedding_function=get_embedding_function()
)
