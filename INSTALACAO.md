# 📦 GUIA DE INSTALAÇÃO EM SERVIDOR

## 🖥️ OPÇÃO 1: INSTALAÇÃO DIRETA (Linux/Windows Server)

### **1. Pré-requisitos:**
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### **2. Passos:**

```bash
# 1. Baixar o projeto
cd /caminho/do/servidor
unzip importador_csv_omie.zip
cd importador_csv_omie

# 2. Criar ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar credenciais
cp env.example .env
nano .env  # Ou vim, ou qualquer editor
# Cole suas credenciais aqui!

# 5. Testar
python importar.py seu_arquivo.csv
```

---

## 🐳 OPÇÃO 2: DOCKER (Recomendado para Produção)

### **1. Pré-requisitos:**
- Docker instalado
- Docker Compose (opcional)

### **2. Passos:**

```bash
# 1. Baixar o projeto
cd /caminho/do/servidor
unzip importador_csv_omie.zip
cd importador_csv_omie

# 2. Configurar credenciais
cp env.example .env
nano .env
# Cole suas credenciais!

# 3. Criar pasta para dados
mkdir dados relatorios

# 4. Colocar CSV na pasta dados
cp seu_arquivo.csv dados/

# 5. Build da imagem
docker build -t importador-omie .

# 6. Executar
docker run --rm \
  -v $(pwd)/dados:/app/dados \
  -v $(pwd)/relatorios:/app/relatorios \
  --env-file .env \
  importador-omie \
  python importar.py /app/dados/seu_arquivo.csv
```

### **Ou com Docker Compose:**

```bash
# 1. Editar docker-compose.yml se necessário
# 2. Executar
docker-compose up
```

---

## ⏰ AGENDAR EXECUÇÃO AUTOMÁTICA

### **Linux (Cron):**

```bash
# Editar crontab
crontab -e

# Adicionar linha (executar todo dia às 8h)
0 8 * * * cd /caminho/importador_csv_omie && /caminho/venv/bin/python importar.py dados/arquivo.csv >> logs/importacao.log 2>&1
```

### **Windows (Task Scheduler):**

1. Abrir "Agendador de Tarefas"
2. Criar nova tarefa
3. Gatilho: Diariamente às 8h
4. Ação: Executar programa
   - Programa: `C:\Python310\python.exe`
   - Argumentos: `importar.py dados\arquivo.csv`
   - Iniciar em: `C:\caminho\importador_csv_omie`

---

## 🔄 ATUALIZAR TOKEN VINDI

Se o token expirar:

```bash
# 1. Editar .env
nano .env

# 2. Atualizar linha:
VINDI_TOKEN_LOBO_ATIVIDADES=NOVO_TOKEN_AQUI

# 3. Salvar e executar novamente
```

---

## 📊 VER RELATÓRIOS

Relatórios são salvos automaticamente:

```bash
# Ver último relatório
ls -lt relatorio_*.json | head -1

# Ler relatório
cat relatorio_importacao_20251102_153045.json | jq .
```

---

## 🆘 PROBLEMAS COMUNS

### **"ModuleNotFoundError: No module named 'dotenv'"**
```bash
pip install python-dotenv
```

### **"VINDI_TOKEN não configurado"**
- Verifique se criou o arquivo `.env`
- Verifique se o token está correto

### **"Permission denied"**
```bash
chmod +x importar.py
```

---

## 🔒 SEGURANÇA

- ✅ Nunca commite o arquivo `.env`
- ✅ Use variáveis de ambiente em produção
- ✅ Mantenha backups dos relatórios
- ✅ Rotacione tokens periodicamente

---

**Pronto para usar! 🚀**

