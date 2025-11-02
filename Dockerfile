FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do projeto
COPY *.py .
COPY templates/ ./templates/

# Criar diretórios
RUN mkdir -p /app/uploads /app/relatorios

# Expor porta
EXPOSE 5000

# Comando padrão - rodar interface web
CMD ["python", "app.py"]

