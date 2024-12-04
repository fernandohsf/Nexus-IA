import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
chat = ChatGroq(model='llama3-8b-8192')

def resposta_bot(mensagens):
    loader = WebBaseLoader('https://fapec.org/')
    documento = loader.load()

    mensagem_system = """
    Você é o assistente virtual da FAPEC chamado Nexus.
    Sempre responda de forma clara, concisa e com tom positivo.
    Você utiliza as seguintes informações para formular suas respostas: {informacoes}.
    Sempre evite sair do assunto: {informacoes}.
    """
    mensagens_modelo = [('system', mensagem_system)]
    mensagens_modelo += mensagens

    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({'informacoes': documento}).content