FROM python:3.12-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie apenas o requirements primeiro (se quiser melhorar build cache)
# Se não tiver, pode ignorar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copia o código fonte
COPY ./src ./src

# Copia o .env também (se precisar dentro do container)
COPY .env .

# Comando correto: roda o Python diretamente
CMD ["python", "src/application.py"]

