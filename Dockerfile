# Usar a imagem base oficial do Python 3.12
FROM python:3.12-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instalar SQLite 3.35.0 ou superior e outras dependências necessárias
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    libsqlite3-dev \
    && wget https://sqlite.org/2021/sqlite-autoconf-3350500.tar.gz \
    && tar xvfz sqlite-autoconf-3350500.tar.gz \
    && cd sqlite-autoconf-3350500 \
    && ./configure --prefix=/usr/local \
    && make \
    && make install \
    && rm -rf /var/lib/apt/lists/*

# Verificar a versão do SQLite para garantir que seja a correta
RUN sqlite3 --version

# Adicionar o SQLite à variável de ambiente para que a nova versão seja usada
ENV LD_LIBRARY_PATH="/usr/local/lib"

# Copiar os arquivos do projeto para o contêiner
COPY . .

# Instalar as dependências do projeto (incluindo gunicorn e uvicorn)
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o Uvicorn irá usar
EXPOSE 8000

# Comando para iniciar o servidor FastAPI com Gunicorn e Uvicorn
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
