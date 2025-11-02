# 🚀 Importador CSV → Vindi → Omie

Sistema automatizado para importar transações de CSV para o OMIE ERP, enriquecendo os dados com informações da API Vindi (CPF real e nome do produto).

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Funcionalidades

- 🌐 **Interface Web** - Upload drag & drop de CSV
- 📊 **Progresso em Tempo Real** - Acompanhe a importação
- 🔄 **Enriquecimento Automático** - Busca CPF e produto na Vindi
- 💾 **Persistência** - Configurações salvas automaticamente
- 🐳 **Docker Ready** - Deploy fácil com Portainer
- ⚙️ **Configurável** - Todos os tokens via interface web
- 📝 **Relatórios** - JSON detalhado de cada importação

---

## 🚀 Deploy Rápido (Portainer)

### **1. Criar Stack no Portainer:**

**Stacks → Add Stack → Web editor**

Cole este docker-compose:

```yaml
version: '3.8'

services:
  importador-omie:
    image: ghcr.io/SEU_USUARIO/importador-csv-omie:latest
    container_name: importador-omie
    ports:
      - "5000:5000"
    volumes:
      - importador-uploads:/app/uploads
      - importador-relatorios:/app/relatorios
      - importador-config:/app
    restart: unless-stopped

volumes:
  importador-uploads:
  importador-relatorios:
  importador-config:
```

### **2. Deploy**

Clique em **Deploy the stack**

### **3. Configurar**

1. Acesse: `http://SEU_SERVIDOR:5000/configuracoes`
2. Cole o **token completo** da Vindi
3. Salve
4. Pronto! ✅

---

## 📋 Como Usar

### **1. Acessar Interface:**
```
http://SEU_SERVIDOR:5000
```

### **2. Configurar Credenciais** (primeira vez):
- Clique em "⚙️ Configurações"
- Cole token da Vindi
- Salve

### **3. Importar CSV:**
- Arraste o CSV ou clique para selecionar
- Acompanhe o progresso em tempo real
- Veja logs ao vivo

### **4. Resultado:**
- ✅ Clientes criados no Omie com CPF real
- ✅ Contas a receber com produtos reais
- ✅ Relatório JSON salvo

---

## 🔧 Instalação Local

```bash
# Clone
git clone https://github.com/SEU_USUARIO/importador-csv-omie.git
cd importador-csv-omie

# Instale
pip install -r requirements.txt

# Execute
python app.py

# Acesse
http://localhost:5000
```

---

## 📊 Estrutura do CSV

Delimitador: `;`

Campos importantes:
- **Id** - ID da transação
- **Cliente** - Nome
- **E-mail do cliente** - Email
- **Valor** - Valor bruto
- **Valor loja** - Valor líquido
- **Taxa** - Taxa cobrada
- **Data Credito** - Data de crédito
- **Status** - Status (filtra Cancelada/Aguardando)
- **Extra** - Charge ID da Vindi (para enriquecimento)

---

## 🔄 Fluxo de Importação

```
CSV Upload
    ↓
Parse CSV (separa campos)
    ↓
Para cada linha:
  ├─ Filtra canceladas
  ├─ Busca /charges/{Extra} na Vindi → CPF real
  ├─ Busca /bills/{bill_id} → Nome do produto
  ├─ Cria cliente no Omie (com CPF real)
  └─ Cria conta a receber (com produto real)
    ↓
Relatório JSON salvo
```

---

## 🐳 Docker

```bash
# Build
docker build -t importador-omie .

# Run
docker run -p 5000:5000 -v $(pwd)/uploads:/app/uploads importador-omie
```

---

## 📝 Relatórios

Salvos em `relatorios/relatorio_importacao_YYYYMMDD_HHMMSS.json`

Contém:
- Total processado
- Sucessos/Erros
- Detalhes de cada transação
- CPF encontrado na Vindi ou gerado
- Produto encontrado ou genérico

---

## 🔒 Segurança

- ✅ Tokens salvos em volume persistente
- ✅ Não expõe credenciais em logs
- ✅ Validação de arquivos CSV
- ✅ Rate limiting nas APIs

---

## 🆘 Suporte

Problemas? Abra uma issue no GitHub!

---

## 📄 Licença

MIT License - Use livremente!

---

**Desenvolvido para Lobo Atividades Esportivas LTDA** 🏃‍♂️

