#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente para API da Vindi
"""

import requests
import base64
from config import VINDI_TOKEN, VINDI_API_URL


def get_headers():
    """Retorna headers autenticados para API Vindi"""
    auth_string = base64.b64encode(f'{VINDI_TOKEN}:'.encode()).decode()
    return {
        'Authorization': f'Basic {auth_string}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


def buscar_charge(charge_id):
    """
    Busca dados completos de um charge na Vindi
    Retorna: charge com bill.id, CPF, etc
    """
    try:
        url = f'{VINDI_API_URL}/charges/{charge_id}'
        response = requests.get(url, headers=get_headers(), timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('charge'), None
        elif response.status_code == 404:
            return None, f"Charge {charge_id} não encontrado"
        elif response.status_code == 401:
            return None, "Token inválido ou expirado"
        else:
            return None, f"Erro {response.status_code}: {response.text}"
            
    except Exception as e:
        return None, f"Erro de conexão: {str(e)}"


def buscar_bill(bill_id):
    """
    Busca dados completos de uma bill (fatura) na Vindi
    Retorna: bill com bill_items contendo product.name
    """
    try:
        url = f'{VINDI_API_URL}/bills/{bill_id}'
        response = requests.get(url, headers=get_headers(), timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('bill'), None
        elif response.status_code == 404:
            return None, f"Bill {bill_id} não encontrada"
        else:
            return None, f"Erro {response.status_code}: {response.text}"
            
    except Exception as e:
        return None, f"Erro de conexão: {str(e)}"


def extrair_dados_vindi(charge_id):
    """
    Extrai CPF e nome do produto de um charge da Vindi
    Retorna: (cpf, produto_nome, erro)
    """
    if not charge_id or charge_id == '-':
        return None, None, "Charge ID vazio"
    
    # 1. Buscar charge
    charge, erro = buscar_charge(charge_id)
    if erro:
        return None, None, erro
    
    if not charge:
        return None, None, "Charge não retornou dados"
    
    cpf = None
    produto_nome = None
    
    # 2. Extrair CPF do gateway_response_fields
    if charge.get('last_transaction'):
        last_txn = charge['last_transaction']
        if last_txn.get('gateway_response_fields'):
            fields = last_txn['gateway_response_fields']
            cpf = fields.get('document_number')
    
    # 3. Buscar bill para pegar produto
    bill = charge.get('bill')
    if bill and bill.get('id'):
        bill_data, erro_bill = buscar_bill(bill['id'])
        
        if bill_data:
            bill_items = bill_data.get('bill_items', [])
            if bill_items and len(bill_items) > 0:
                first_item = bill_items[0]
                if first_item.get('product'):
                    produto_nome = first_item['product'].get('name')
    
    return cpf, produto_nome, None

