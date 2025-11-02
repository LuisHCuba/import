#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Funções utilitárias
"""


def parse_valor(valor_str):
    """Converte string monetária para float"""
    if not valor_str:
        return 0.0
    
    valor_limpo = str(valor_str).replace('R$', '').replace(' ', '').replace(',', '.')
    
    try:
        return float(valor_limpo)
    except:
        return 0.0


def parse_data(data_str):
    """
    Converte data de DD/MM/YYYY ou YYYY-MM-DD para DD/MM/YYYY
    """
    if not data_str or data_str == '-':
        return None
    
    # Se já está em formato YYYY-MM-DD
    if '-' in data_str and len(data_str.split('-')) == 3:
        partes = data_str.split('-')
        return f"{partes[2]}/{partes[1]}/{partes[0]}"
    
    # Se está em DD/MM/YYYY
    if '/' in data_str:
        return data_str.split(' ')[0]  # Remove hora se tiver
    
    return None


def gerar_cpf_valido(id_numero):
    """Gera um CPF válido baseado no ID"""
    base = str(id_numero).zfill(9)[-9:]
    
    def calcular_digito(cpf_parcial):
        soma = 0
        for i, digito in enumerate(cpf_parcial):
            soma += int(digito) * (len(cpf_parcial) + 1 - i)
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    
    digito1 = calcular_digito(base)
    digito2 = calcular_digito(base + str(digito1))
    
    cpf_completo = base + str(digito1) + str(digito2)
    return f"{cpf_completo[:3]}.{cpf_completo[3:6]}.{cpf_completo[6:9]}-{cpf_completo[9:]}"

