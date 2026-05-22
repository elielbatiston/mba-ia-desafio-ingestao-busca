# Desafio MBA Engenharia de Software com IA - Full Cycle

## Configuração do Ambiente

1. **Configurar as variáveis de ambiente:**

   - Duplique o arquivo `.env.example` e renomeie para `.env`
   - Abra o arquivo `.env` e substitua os valores pelas suas chaves de API reais obtidas

2. **Como executar:**

  a-) Permita que o arquivo start.sh seja executado com o comando abaixo: 

   ```bash
   chmod +x start.sh
   ```
   
  b-) Depois execute

  ```bash
  ./start.sh
  ```

O script start.sh irá fazer a ingestão do documento no banco de dados postgres e entrar no chat.py 
para você fazer as perguntas
