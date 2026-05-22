import os
from search import search_prompt
from dotenv import load_dotenv

load_dotenv()

for k in ("OPENAI_API_KEY", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", "PDF_PATH"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")
      
def main():
    print("=" * 50)
    print("🤖 Chat Terminal iniciado")
    print("Digite 'sair' para encerrar")
    print("=" * 50)
    
    while True:
        question = input("Você: ")
        
        if not question:
          continue

        if question.lower() == "sair":
            print("Bot: Encerrando chat...")
            break
          
        chain = search_prompt(question)          

        if not chain:
            print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
            return
    
        print(f"Bot: {chain}\n")          

if __name__ == "__main__":
    main()
