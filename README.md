# 🚀 Importador CSV → Vindi → Omie

Sistema automatizado para importar CSV de transações para o OMIE, enriquecendo os dados com informações da Vindi (CPF real e nome do produto).

---

## 📋 O QUE O SISTEMA FAZ

1. **Lê arquivo CSV** com transações
2. **Busca dados na Vindi** (CPF real + nome do produto)
3. **Cria clientes no Omie** com CPF real
4. **Cria contas a receber no Omie** com dados completos
5. **Gera relatório** de sucesso/erros

---

## 🔧 INSTALAÇÃO

### **1. Clone ou baixe o projeto**

```bash
cd importador_csv_omie
```

### **2. Instale as dependências**

```bash
pip install -r requirements.txt
```

### **3. Configure as credenciais**

Copie o arquivo de exemplo:
```bash
cp env.example .env
```

Edite o arquivo `.env` e adicione suas credenciais:

```env
# CREDENCIAIS VINDI
VINDI_TOKEN_LOBO_ATIVIDADES=SEU_TOKEN_COMPLETO_AQUI

# CREDENCIAIS OMIE (já configuradas)
OMIE_APP_KEY=5604910395084
OMIE_APP_SECRET=bd388fb9bf27eb6b638b0daf134f6312

# CONFIGURAÇÕES
CONTA_VINDI_ID=4328092596
EMPRESA=LOBO_ATIVIDADES
```

⚠️ **IMPORTANTE:** Pegue o token completo da Vindi clicando no ícone do olho!

---

## 🎯 COMO USAR

### **Executar importação:**

```bash
python importar.py seu_arquivo.csv
```

**Exemplo:**
```bash
python importar.py dados_setembro.csv
```

### **O que acontece:**

1. Sistema lê o CSV
2. Para cada linha:
   - Filtra canceladas/aguardando pagamento
   - Busca CPF e produto na Vindi (campo "Extra" = Charge ID)
   - Cria cliente no Omie
   - Cria conta a receber no Omie
   - Mostra progresso em tempo real
3. Gera relatório JSON com resultados

---

## 📊 ESTRUTURA DO CSV

O CSV deve ter estas colunas (delimitador `;`):

- **Id** - ID da transação
- **Cliente** - Nome do cliente
- **E-mail do cliente** - Email
- **Valor** - Valor bruto
- **Valor loja** - Valor líquido
- **Taxa** - Taxa cobrada
- **Data Credito** - Data de crédito (DD/MM/YYYY ou YYYY-MM-DD)
- **Status** - Status da transação
- **Extra** - Charge ID da Vindi (IMPORTANTE!)
- **Meio de Pagamento** - Forma de pagamento

---

## 📁 ESTRUTURA DO PROJETO

```
importador_csv_omie/
├── importar.py          ← Script principal
├── vindi_api.py         ← Cliente API Vindi
├── omie_api.py          ← Cliente API Omie
├── utils.py             ← Funções utilitárias
├── config.py            ← Configurações
├── requirements.txt     ← Dependências
├── env.example          ← Exemplo de .env
├── .env                 ← Suas credenciais (NÃO commitar!)
├── Dockerfile           ← Para rodar em container
└── README.md            ← Este arquivo
```

---

## 🐳 RODAR EM SERVIDOR (Docker)

### **1. Build da imagem:**

```bash
docker build -t importador-omie .
```

### **2. Rodar container:**

```bash
docker run -v $(pwd)/dados:/app/dados -v $(pwd)/relatorios:/app/relatorios importador-omie python importar.py /app/dados/seu_arquivo.csv
```

**Ou com docker-compose:**

```bash
docker-compose up
```

---

## 📝 LOGS E RELATÓRIOS

### **Durante a execução:**
- Mostra progresso em tempo real
- Indica sucesso/erro de cada transação
- Mostra se pegou dados da Vindi ou usou fallback

### **Após conclusão:**
- Gera arquivo JSON: `relatorio_importacao_YYYYMMDD_HHMMSS.json`
- Contém todos os resultados detalhados

---

## ⚠️ NOTAS IMPORTANTES

1. **Token Vindi:** Precisa ser da conta LOBO_ATIVIDADES (onde estão os charges do CSV)
2. **Campo "Extra":** É o Charge ID da Vindi (essencial para enriquecimento)
3. **Rate Limiting:** Sistema aguarda 1 segundo entre cada transação
4. **Fallback:** Se Vindi falhar, usa CPF gerado válido
5. **Idempotência:** Usar mesmo ID de integração evita duplicatas

---

## 🔍 TROUBLESHOOTING

### **Erro: "Token inválido"**
- Verifique se copiou o token COMPLETO da Vindi
- Token deve ter ~40 caracteres

### **Erro: "Charge não encontrado (404)"**
- Charge pertence a outra conta Vindi
- Verifique se está usando token da conta correta

### **Erro: "Cliente já existe"**
- Normal! Sistema continua e cria a conta a receber

### **Erro: "Conta já existe"**
- Transação já foi importada anteriormente
- Verificar código de integração

---

## 🆘 SUPORTE

Para dúvidas ou problemas:
- Veja os logs detalhados durante execução
- Consulte o arquivo de relatório JSON
- Verifique as credenciais no `.env`

---

**Desenvolvido para Lobo Atividades Esportivas LTDA** 🏃‍♂️

