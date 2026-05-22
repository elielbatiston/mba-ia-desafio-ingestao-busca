import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

for k in ("OPENAI_API_KEY", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", "PDF_PATH"):
    if k in os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")
      
PDF_PATH = Path(os.getenv("PDF_PATH", "")).expanduser().resolve()

if not PDF_PATH.exists():
    raise FileNotFoundError(f"PDF not found: {PDF_PATH}")
  
if not PDF_PATH.is_file():
    raise ValueError(f"Invalid pdf file: {PDF_PATH}")
    
def ingest_pdf():
    docs = PyPDFLoader(str(PDF_PATH)).load()      

    splits = RecursiveCharacterTextSplitter(
      chunk_size=1000, 
      chunk_overlap=150,
      add_start_index=False).split_documents(docs)

    if not splits:
        raise SystemExit(0)
      
    enriched = [
      Document(
        page_content=d.page_content, 
        metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
      ) 
      for d in splits
    ]  

    ids = [f"doc-{i}" for i in range(len(enriched))]
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL", "text-embedding-3-small"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,    
    )

    store.add_documents(documents=enriched, ids=ids)

if __name__ == "__main__":
    ingest_pdf()
