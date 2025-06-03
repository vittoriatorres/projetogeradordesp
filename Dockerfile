# Usa imagem oficial com Python 3.11
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia todos os arquivos do projeto para dentro do contêiner
COPY . .

# Atualiza o pip e instala as dependências
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expõe a porta usada pela aplicação Streamlit
EXPOSE 2025

# Comando para rodar na porta e endereço definidos
CMD ["streamlit", "run", "app.py", "--server.port=2025", "--server.address=0.0.0.0"]