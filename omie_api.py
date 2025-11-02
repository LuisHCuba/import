#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente para API do OMIE
"""

import requests
import json
from config import OMIE_APP_KEY, OMIE_APP_SECRET, OMIE_API_URL_CLIENTES, OMIE_API_URL_CONTAS


def criar_cliente(transacao):
    """
    Cria cliente no OMIE
    Retorna: (sucesso, codigo_cliente, erro)
    """
    codigo_integracao = f"CSV_{transacao['id']}"
    
    cliente = {
        "codigo_cliente_integracao": codigo_integracao,
        "razao_social": transacao['nome'],
        "nome_fantasia": transacao['nome'].split(' ')[0] if transacao['nome'] else "Cliente",
        "email": transacao['email'],
        "pessoa_fisica": "S",
        "cpf_cnpj": transacao['cpf_cnpj'],
        "inativo": "N"
    }
    
    payload = {
        "call": "IncluirCliente",
        "app_key": OMIE_APP_KEY,
        "app_secret": OMIE_APP_SECRET,
        "param": [cliente]
    }
    
    try:
        response = requests.post(
            OMIE_API_URL_CLIENTES,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return True, codigo_integracao, None
        else:
            # Cliente pode já existir, não é erro crítico
            return True, codigo_integracao, f"Possível duplicado: {response.text[:100]}"
            
    except Exception as e:
        return False, None, str(e)


def criar_conta_receber(transacao):
    """
    Cria conta a receber no OMIE
    Retorna: (sucesso, codigo_lancamento, erro)
    """
    conta_receber = {
        "codigo_lancamento_integracao": f"CSV_{transacao['id']}",
        "codigo_cliente_fornecedor_integracao": f"CSV_{transacao['id']}",
        "data_vencimento": transacao['data_credito_formatada'],
        "valor_documento": transacao['valor_liquido'],
        "codigo_categoria": "1.01.02",
        "data_previsao": transacao['data_credito_formatada'],
        "numero_documento": f"CSV-{transacao['id']}",
        "observacao": transacao['observacao'],
        "data_emissao": transacao['data_credito_formatada'],
        "importado_api": "S",
        "bloqueado": "N",
        "baixar_documento": "S",
        "conciliar_documento": "S"
    }
    
    payload = {
        "call": "IncluirContaReceber",
        "app_key": OMIE_APP_KEY,
        "app_secret": OMIE_APP_SECRET,
        "param": [conta_receber]
    }
    
    try:
        response = requests.post(
            OMIE_API_URL_CONTAS,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            codigo = data.get("codigo_lancamento_omie", "N/A")
            return True, codigo, None
        else:
            return False, None, f"Erro {response.status_code}: {response.text}"
            
    except Exception as e:
        return False, None, str(e)

