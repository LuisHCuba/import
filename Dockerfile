FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Instalar curl para healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do projeto
COPY *.py .
COPY *.sh .
COPY templates/ ./templates/

# Dar permissão de execução
RUN chmod +x start.sh

# Criar diretórios
RUN mkdir -p /app/uploads /app/relatorios

# Expor porta
EXPOSE 5000

# Comando padrão - rodar via script de inicialização
CMD ["./start.sh"]

