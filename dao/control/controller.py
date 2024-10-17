from langchain_core.prompts import PromptTemplate
from langchain.chains import load_qa_chain
from langchain.llms import OpenAI
from dao.model.models import db


def root_controller():
    return {"message": "Hello World"}


def say_hello_controller(name: str):
    return {"message": f"Hello {name}"}


def predict_controller(data):
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
                         "procedimento", "toxina"], template=template)

    query = prompt_template.format(
        idade=data.idade,
        alergias=data.alergias,
        procedimentos_anteriores=data.procedimentos_anteriores,
        medicamentos=data.medicamentos,
        condicoes_saude=data.condicoes_saude,
        procedimento=data.procedimento,
        toxina=data.toxina
    )

    # Realizar a busca de documentos semelhantes
    docs = db.similarity_search(query, k=1)

    # Carregar o modelo de IA da OpenAI e gerar a resposta
    chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
    response = chain.run(input_documents=docs, question=query)

    return {"response": response}
