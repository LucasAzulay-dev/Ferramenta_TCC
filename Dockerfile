# Base image com Python
# Base image com Python
FROM python:3.10.5

# Instalar dependências necessárias, incluindo GCC
RUN apt-get update && apt-get install -y \
    build-essential \ 
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY runtime_execute.py /app
COPY compile_test_vector_original_sut.py /app
COPY TestDriversSource /app/TestDriversSource

# Comando para rodar o script Python
# CMD ["python", "runtime_execute.py"]
