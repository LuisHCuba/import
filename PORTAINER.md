# 🐳 DEPLOY NO PORTAINER COM STACK

## 📋 PASSO A PASSO

### **1. Preparar arquivo `.env`**

Crie um arquivo `.env` no seu computador com as credenciais:

```env
VINDI_TOKEN_LOBO_ATIVIDADES=SEU_TOKEN_COMPLETO_AQUI
OMIE_APP_KEY=5604910395084
OMIE_APP_SECRET=bd388fb9bf27eb6b638b0daf134f6312
CONTA_VINDI_ID=4328092596
EMPRESA=LOBO_ATIVIDADES
```

---

### **2. Criar Stack no Portainer**

1. **Acesse seu Portainer**
2. **Vá em:** Stacks → Add Stack
3. **Nome da Stack:** `importador-omie`
4. **Build method:** Web editor

---

### **3. Cole este Docker Compose:**

```yaml
version: '3.8'

services:
  importador-omie:
    image: python:3.10-slim
    container_name: importador-omie
    working_dir: /app
    ports:
      - "5000:5000"
    volumes:
      - importador-uploads:/app/uploads
      - importador-relatorios:/app/relatorios
      - ./app:/app
    environment:
      VINDI_TOKEN_LOBO_ATIVIDADES: ${VINDI_TOKEN_LOBO_ATIVIDADES}
      OMIE_APP_KEY: "5604910395084"
      OMIE_APP_SECRET: "bd388fb9bf27eb6b638b0daf134f6312"
      CONTA_VINDI_ID: "4328092596"
      EMPRESA: "LOBO_ATIVIDADES"
    command: >
      sh -c "pip install -q requests python-dotenv flask werkzeug &&
             python app.py"
    restart: unless-stopped

volumes:
  importador-uploads:
  importador-relatorios:
```

---

### **4. Configurar Variáveis de Ambiente**

Na seção **Environment variables** do Portainer, adicione:

```
VINDI_TOKEN_LOBO_ATIVIDADES = SEU_TOKEN_COMPLETO_AQUI
```

---

### **5. Upload dos Arquivos**

Após criar a stack, você precisa copiar os arquivos Python:

**Opção A: Via Portainer Console**

1. Vá em Containers → importador-omie → Console
2. Execute:
```bash
cd /app
```

3. Crie os arquivos usando `cat > arquivo.py` e cole o conteúdo

**Opção B: Via Volume Bind**

1. No servidor onde está o Portainer, crie a pasta:
```bash
mkdir -p /var/lib/docker/volumes/importador-app/_data
```

2. Copie todos os arquivos `.py` e pasta `templates/` para lá

---

### **6. Deploy da Stack**

1. Clique em **Deploy the stack**
2. Aguarde o container iniciar
3. Acesse: `http://SEU_SERVIDOR:5000`

---

## 🌐 ACESSAR A INTERFACE

Após deploy:

```
http://IP_DO_SERVIDOR:5000
```

Ou se configurou domínio:

```
http://importador.seudominio.com
```

---

## 🔄 ATUALIZAR O PROJETO

Para atualizar código:

1. Vá em Portainer → Stacks → importador-omie
2. Edite os arquivos no volume
3. Clique em **Restart** no container

---

## 📊 MONITORAR LOGS

No Portainer:

1. Containers → importador-omie → Logs
2. Veja logs em tempo real da aplicação

---

## 🔒 SEGURANÇA

- ✅ Use variáveis de ambiente para credenciais
- ✅ Configure firewall para limitar acesso à porta 5000
- ✅ Considere adicionar autenticação básica
- ✅ Use HTTPS com proxy reverso (Nginx/Traefik)

---

## 🎯 FACILITAR AINDA MAIS (OPCIONAL)

### **Adicionar ao Portainer App Templates:**

1. Em Portainer → App Templates → Custom Templates
2. Crie template com o docker-compose acima
3. Usuário só precisa:
   - Clicar no template
   - Adicionar token
   - Deploy!

---

**Pronto para usar no Portainer! 🚀**

