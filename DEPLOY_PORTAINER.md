# 🚀 DEPLOY NO PORTAINER - GUIA COMPLETO

## 📦 OPÇÃO 1: USAR IMAGEM DO GITHUB (Recomendado)

### **Passo 1: Subir projeto no GitHub**

```bash
# No seu computador
cd importador_csv_omie
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/SEU_USUARIO/importador-csv-omie.git
git push -u origin main
```

### **Passo 2: Criar Stack no Portainer**

1. **Acesse Portainer** → Stacks → Add Stack
2. **Nome:** `importador-omie`
3. **Build method:** Repository
4. **Repository URL:** `https://github.com/SEU_USUARIO/importador-csv-omie`
5. **Compose path:** `docker-compose.yml`

### **Passo 3: Configurar Variáveis de Ambiente**

Na seção **Environment variables**, adicione:

```
VINDI_TOKEN_LOBO_ATIVIDADES=DEIXE_VAZIO_AQUI
```

(O usuário vai configurar depois via interface web)

### **Passo 4: Deploy!**

Clique em **Deploy the stack**

---

## 📦 OPÇÃO 2: UPLOAD MANUAL (Mais Simples)

### **Passo 1: Criar pasta no servidor**

Conecte no servidor via SSH:

```bash
mkdir -p /opt/importador-omie
cd /opt/importador-omie
```

### **Passo 2: Copiar arquivos**

Copie TODOS os arquivos do projeto para `/opt/importador-omie`:

```
/opt/importador-omie/
├── app.py
├── importar.py
├── vindi_api.py
├── omie_api.py
├── utils.py
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── templates/
    ├── index.html
    └── configuracoes.html
```

### **Passo 3: Criar Stack no Portainer**

1. **Stacks → Add Stack**
2. **Nome:** `importador-omie`
3. **Build method:** Web editor
4. **Cole o conteúdo de `stack-portainer.yml`**
5. **OU use Upload e envie `docker-compose.yml`**

### **Passo 4: Configurar Volume Path**

Edite o stack para apontar para a pasta:

```yaml
services:
  importador-omie:
    build: /opt/importador-omie  # ← Caminho no servidor
    # ... resto igual
```

### **Passo 5: Deploy**

---

## 🌐 ACESSAR O SISTEMA

Após deploy:

```
http://IP_DO_SERVIDOR:5000
```

### **Primeira vez:**

1. Acesse: `http://IP_DO_SERVIDOR:5000/configuracoes`
2. **Cole o token COMPLETO da Vindi**
3. **Salve**
4. **Volte para home** e faça upload do CSV!

---

## 🔧 CONFIGURAÇÕES VIA INTERFACE WEB

### **Tela de Configurações:**

O usuário pode configurar TUDO pela interface:

- ✅ Token Vindi
- ✅ Credenciais Omie
- ✅ Conta Vindi ID
- ✅ Empresa

**Configurações são salvas em `config.json`** dentro do volume!

---

## 📊 VOLUMES CRIADOS

O Portainer cria estes volumes automaticamente:

- `importador-uploads` → Arquivos CSV enviados
- `importador-relatorios` → Relatórios JSON gerados
- `importador-config` → config.json com credenciais

**Dados persistem** mesmo se container for recriado!

---

## 🔄 ATUALIZAR PROJETO

### **Se está no GitHub:**

1. Faça push das mudanças no GitHub
2. No Portainer: Stack → Pull and redeploy

### **Se é local:**

1. Atualize arquivos em `/opt/importador-omie`
2. No Portainer: Stack → Redeploy

---

## 🆘 TROUBLESHOOTING

### **Container não inicia:**

```bash
# Ver logs
docker logs importador-omie
```

### **Porta 5000 em uso:**

Edite o stack e mude a porta:
```yaml
ports:
  - "8080:5000"  # Usar porta 8080
```

### **Configurações não salvam:**

Verifique permissões do volume:
```bash
docker exec -it importador-omie ls -la /app
```

---

## 🎯 RESUMO RÁPIDO

**Para usuário final:**

1. ✅ Acessa `http://servidor:5000/configuracoes`
2. ✅ Cola token da Vindi
3. ✅ Salva
4. ✅ Volta e faz upload do CSV
5. ✅ Acompanha progresso em tempo real!

**SEM PRECISAR MEXER EM ARQUIVO, TERMINAL OU DOCKER! 🎉**

