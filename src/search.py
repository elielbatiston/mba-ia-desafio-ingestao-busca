import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

- Responda sempre em frase completa e contextualizada.
- Converta valores monetários para formato simplificado.
  Exemplo: "R$ 5,00" deve virar "5 reais".  

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL", "text-embedding-3-small"))

store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True,    
)

llm = ChatOpenAI(model="gpt-5-nano", temperature=0)

def search_prompt(question=None):          
    results = store.similarity_search_with_score(query=question, k=10)

    contexts = []

    for i, (doc, score) in enumerate(results, start=1):             
        contexts.append(doc.page_content)

    if not contexts:
      return "Não tenho informações necessárias para responder sua pergunta."
  
    contexts = "\n\n".join(contexts)

    prompt = PROMPT_TEMPLATE.format(
        contexto=contexts,
        pergunta=question
    )
    
    result = llm.invoke(prompt)
    
    if not result:
      return "Não tenho informações necessárias para responder sua pergunta."
  
    return result.content         
        