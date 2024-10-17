import os
from azure.storage.blob import BlobServiceClient
from pydantic import BaseModel
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb
import sqlite3

# Configuração da conexão com Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_name = "chroma-container"
blob_name = "chroma_data.db"
local_file_name = "/tmp/chroma_data.db"  # Caminho temporário para trabalhar com o arquivo localmente

# Fazer download do arquivo SQLite do Blob Storage para o sistema local
def download_sqlite_blob():
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    with open(local_file_name, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

# Upload do arquivo SQLite de volta para o Blob Storage após as operações
def upload_sqlite_blob():
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    with open(local_file_name, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

# Verificar se o banco de dados local já existe, caso contrário, baixar do Blob Storage
if not os.path.exists(local_file_name):
    download_sqlite_blob()

# Configurações de ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("A chave da API da OpenAI não está definida. Verifique se a variável de ambiente OPENAI_API_KEY está configurada corretamente.")

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
    path=local_file_name,  # Usar o caminho do arquivo baixado localmente
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

# Instância do banco de dados ChromaDB
db = Chroma(
    client=client, collection_name="iamed",
    persist_directory=local_file_name,  # Usar o caminho local
    embedding_function=get_embedding_function()
)

# Após terminar todas as operações, carregar o banco de dados atualizado de volta ao Azure Blob Storage
upload_sqlite_blob()

# Opcional: limpar o arquivo local temporário
os.remove(local_file_name)
