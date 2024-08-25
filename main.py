from fastapi import FastAPI
from pydantic import BaseModel
from langchain.embeddings import OpenAIEmbeddings
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
# from langchain.chains.question_answering import load_qa_chain
# from langchain.llms import OpenAI
from langchain import PromptTemplate

import chromadb
import os

os.environ["OPENAI_API_KEY"] = ("-")
os.environ["CHROMA_PATH"] = "/chroma"
os.environ["PINECONE_API_KEY"] = "e9cb230e-979e-4c7d-967b-8788ad806bd6"
os.environ["QDRANT_API_KEY"] = "y51snXPq9TJIC8uYJm5_2quxGdx8miv4loSCcBB1a_k8ke_2y03ZgA"


def get_embedding_function():
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    return embeddings


client = chromadb.PersistentClient(
    path=os.environ['CHROMA_PATH'],
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

db = Chroma(
    client=client, collection_name="iamed",
    persist_directory=os.environ['CHROMA_PATH'], embedding_function=get_embedding_function()
)

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
    template = """
    You are a specialized estetic procedures triage assistant. Your knowledge is restricted to the inputed documents. 
    You must not use your pre-trained knowledge and must not use web content.
    You will receive the patient medical record.

    You have to answer in a simplified and clear form. You have to answer in brazilian portuguese.

    Considering a patient with the following medical record:

    Age: {idade} years
    Has {alergias}
    Previous aesthetic procedures: {procedimentos_anteriores}
    Continuous medications: {medicamentos}
    Health conditions: {condicoes_saude}

    Is there anything in the record that prevents the {procedimento} 
    procedure with {toxina} from being performed?

    To justify the response, search for articles in the database of https://pubmed.ncbi.nlm.nih.gov/ and give me clickable links.
    """
    prompt_template = PromptTemplate(
        input_variables=["idade", "alergias", "procedimentos_anteriores", "medicamentos", "condicoes_saude",
                         "procedimento"], template=template)

    query = prompt_template.format(
        idade=data.idade,
        alergias=data.alergias,
        procedimentos_anteriores=data.procedimentos_anteriores,
        medicamentos=data.medicamentos,
        condicoes_saude=data.condicoes_saude,
        procedimento=data.procedimento,
        toxina=data.toxina
    )

    # Precisa da API
    # docs = db.similarity_search(query, k=1)
    # print(docs)
    # chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
    # response = chain.run(input_documents=docs, question=query)

    response = "Baseado nos registros médicos, o procedimento de Harmonização Facial com Nabota pode ser realizado, mas é necessário precaução devido à condição de gravidez mencionada."

    return {"response": response}
