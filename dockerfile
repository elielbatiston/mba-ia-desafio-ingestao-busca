# Imagem oficial do Python
FROM python:3.12-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos da aplicação
COPY . .

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["tail", "-f", "/dev/null"]
