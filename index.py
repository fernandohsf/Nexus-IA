import os
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader

# Configurando logging para gravar somente no arquivo
log_filename = 'nexus_log.txt'  # Nome do arquivo de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler(log_filename),  # Cria ou sobrescreve o arquivo de log
])

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

# Inicializando o modelo de Chat
chat = ChatGroq(model='llama3-8b-8192')

def resposta_bot(mensagens, documento):
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

def documentos_web(urls):
    conteudo_combinado = ""
    for url in urls:
        try:
            loader = WebBaseLoader(url)
            documentos = loader.load()
            for doc in documentos:
                conteudo_combinado += doc.page_content + "\n"
            logging.info(f"Documentos carregados com sucesso da URL: {url}")
        except Exception as e:
            logging.error(f"Erro ao carregar documentos da URL {url}: {e}")
    return conteudo_combinado

print('Bem-vindo ao Nexus')
logging.info("Nexus iniciado com sucesso.")

urls = [
    'https://fapec.org/',
    'https://conveniar.atlassian.net/wiki/spaces/CONV/pages/1016588/Guias+de+Utiliza+o'
]
documento = documentos_web(urls)

mensagens = []
while True:
    pergunta = input('Usuario: ')
    if pergunta.lower() == 'sair':
        logging.info("Usuário encerrou a conversa.")
        break
    logging.info(f"Pergunta do usuário: {pergunta}")
    mensagens.append(('user', pergunta))

    try:
        resposta = resposta_bot(mensagens, documento)
        logging.info(f"Resposta gerada pelo bot: {resposta}")
    except Exception as e:
        logging.error(f"Erro ao gerar a resposta: {e}")
        resposta = "Desculpe, ocorreu um erro ao processar sua solicitação."

    mensagens.append(('assistant', resposta))
    print(f'Bot: {resposta}')

print('Muito obrigado por usar o Nexus')
logging.info("Nexus finalizado.")