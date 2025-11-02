#!/bin/bash

# Script de inicialização que garante valores padrão

# Definir valores padrão se variáveis estiverem vazias
export VINDI_TOKEN_LOBO_ATIVIDADES="${VINDI_TOKEN_LOBO_ATIVIDADES:-}"
export OMIE_APP_KEY="${OMIE_APP_KEY:-5604910395084}"
export OMIE_APP_SECRET="${OMIE_APP_SECRET:-bd388fb9bf27eb6b638b0daf134f6312}"
export CONTA_VINDI_ID="${CONTA_VINDI_ID:-4328092596}"
export EMPRESA="${EMPRESA:-LOBO_ATIVIDADES}"

echo "✅ Variáveis de ambiente configuradas"
echo "Token Vindi: ${VINDI_TOKEN_LOBO_ATIVIDADES:0:10}..."
echo "Omie Key: ${OMIE_APP_KEY}"
echo "Conta ID: ${CONTA_VINDI_ID}"

# Iniciar aplicação
python app.py

