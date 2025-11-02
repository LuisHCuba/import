#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações do sistema - CARREGAMENTO DINÂMICO
"""

import os
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Arquivo de configuração persistente
CONFIG_FILE = 'config.json'

# URLs DAS APIs (fixas)
VINDI_API_URL = 'https://app.vindi.com.br/api/v1'
OMIE_API_URL_CLIENTES = 'https://app.omie.com.br/api/v1/geral/clientes/'
OMIE_API_URL_CONTAS = 'https://app.omie.com.br/api/v1/financas/contareceber/'


def carregar_config():
    """Carrega configurações do arquivo JSON ou variáveis de ambiente"""
    config = {}
    
    # Tentar carregar do arquivo JSON primeiro
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print("✅ Configurações carregadas do arquivo config.json")
                return config
        except:
            pass
    
    # Fallback para variáveis de ambiente
    config = {
        'VINDI_TOKEN': os.getenv('VINDI_TOKEN_LOBO_ATIVIDADES', ''),
        'OMIE_APP_KEY': os.getenv('OMIE_APP_KEY', ''),
        'OMIE_APP_SECRET': os.getenv('OMIE_APP_SECRET', ''),
        'CONTA_VINDI_ID': int(os.getenv('CONTA_VINDI_ID', '0')) if os.getenv('CONTA_VINDI_ID') else 0,
        'EMPRESA': os.getenv('EMPRESA', 'LOBO_ATIVIDADES')
    }
    
    return config


def salvar_config(config):
    """Salva configurações no arquivo JSON"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar config: {e}")
        return False


def validar_config(config):
    """Valida se configurações estão completas"""
    erros = []
    
    if not config.get('VINDI_TOKEN'):
        erros.append("Token Vindi não configurado")
    
    if not config.get('OMIE_APP_KEY'):
        erros.append("App Key Omie não configurada")
    
    if not config.get('OMIE_APP_SECRET'):
        erros.append("App Secret Omie não configurada")
    
    return len(erros) == 0, erros


# Carregar config global
_config = carregar_config()

# Exportar variáveis (compatibilidade com código antigo)
VINDI_TOKEN = _config.get('VINDI_TOKEN', '')
OMIE_APP_KEY = _config.get('OMIE_APP_KEY', '')
OMIE_APP_SECRET = _config.get('OMIE_APP_SECRET', '')
CONTA_VINDI_ID = _config.get('CONTA_VINDI_ID', 4328092596)
EMPRESA = _config.get('EMPRESA', 'LOBO_ATIVIDADES')


def get_config():
    """Retorna configuração atual"""
    return _config


def atualizar_config(nova_config):
    """Atualiza configuração em memória e arquivo"""
    global _config, VINDI_TOKEN, OMIE_APP_KEY, OMIE_APP_SECRET, CONTA_VINDI_ID, EMPRESA
    
    _config.update(nova_config)
    salvar_config(_config)
    
    # Atualizar variáveis globais
    VINDI_TOKEN = _config.get('VINDI_TOKEN', '')
    OMIE_APP_KEY = _config.get('OMIE_APP_KEY', '')
    OMIE_APP_SECRET = _config.get('OMIE_APP_SECRET', '')
    CONTA_VINDI_ID = _config.get('CONTA_VINDI_ID', 4328092596)
    EMPRESA = _config.get('EMPRESA', 'LOBO_ATIVIDADES')

