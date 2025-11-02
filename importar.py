#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal para importar CSV para OMIE com enriquecimento da Vindi
"""

import csv
import json
import time
from datetime import datetime
from vindi_api import extrair_dados_vindi
from omie_api import criar_cliente, criar_conta_receber
from utils import parse_valor, parse_data, gerar_cpf_valido


def processar_csv(arquivo_csv):
    """
    Processa o arquivo CSV e importa para OMIE
    """
    print("="*80)
    print("🚀 IMPORTADOR CSV → VINDI → OMIE")
    print("="*80)
    print(f"📁 Arquivo: {arquivo_csv}")
    print(f"⏰ Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80)
    
    # Ler CSV
    print("\n📂 Lendo CSV...")
    linhas = []
    
    try:
        with open(arquivo_csv, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            linhas = list(reader)
        
        print(f"✅ {len(linhas)} linhas carregadas")
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
        return
    
    # Estatísticas
    total = 0
    processadas = 0
    sucessos_cliente = 0
    sucessos_conta = 0
    erros = 0
    puladas = 0
    
    resultados = []
    
    print(f"\n{'='*80}")
    print("📊 PROCESSANDO TRANSAÇÕES")
    print(f"{'='*80}\n")
    
    for i, linha in enumerate(linhas):
        total += 1
        print(f"\n📋 [{i+1}/{len(linhas)}] Processando...")
        
        # Extrair dados do CSV
        transaction_id = linha.get('Id', '').strip()
        status = linha.get('Status', '').strip()
        data_credito = linha.get('Data Credito', '').strip()
        extra = linha.get('Extra', '').strip()
        
        # Filtrar canceladas e aguardando pagamento
        if status in ['Cancelada', 'Aguardando Pagamento']:
            print(f"  ⏭️  Pulando: Status = {status}")
            puladas += 1
            continue
        
        # Validar data de crédito
        if not data_credito or data_credito == '-':
            print(f"  ⏭️  Pulando: Sem data de crédito")
            puladas += 1
            continue
        
        # Preparar dados básicos
        transacao = {
            'id': transaction_id,
            'nome': linha.get('Cliente', '').strip(),
            'email': linha.get('E-mail do cliente', '').strip(),
            'valor': parse_valor(linha.get('Valor', '0')),
            'valor_liquido': parse_valor(linha.get('Valor loja', '0')),
            'taxa': parse_valor(linha.get('Taxa', '0')),
            'data_credito_formatada': parse_data(data_credito),
            'forma_pagamento': linha.get('Meio de Pagamento', 'Não especificado').strip(),
            'cpf_cnpj': gerar_cpf_valido(transaction_id),  # CPF gerado como fallback
            'produto_nome': 'Serviço',  # Produto genérico como fallback
            'charge_id': extra
        }
        
        print(f"  ID: {transaction_id}")
        print(f"  Cliente: {transacao['nome']}")
        print(f"  Valor: R$ {transacao['valor']:.2f}")
        print(f"  Data Crédito: {transacao['data_credito_formatada']}")
        
        # ENRIQUECER COM DADOS DA VINDI
        if extra and extra != '-':
            print(f"  🔍 Buscando dados na Vindi (Charge ID: {extra})...")
            
            cpf_vindi, produto_vindi, erro_vindi = extrair_dados_vindi(extra)
            
            if cpf_vindi:
                transacao['cpf_cnpj'] = cpf_vindi
                print(f"  ✅ CPF Real: {cpf_vindi}")
            else:
                print(f"  ⚠️  CPF: Usando gerado ({transacao['cpf_cnpj']})")
            
            if produto_vindi:
                transacao['produto_nome'] = produto_vindi
                print(f"  ✅ Produto: {produto_vindi}")
            else:
                print(f"  ⚠️  Produto: Usando genérico")
            
            if erro_vindi:
                print(f"  ℹ️  Vindi: {erro_vindi}")
        else:
            print(f"  ⚠️  Sem Charge ID, usando dados gerados")
        
        # Criar observação
        transacao['observacao'] = (
            f"Transação ID: {transaction_id} | "
            f"Charge ID: {extra or 'N/A'} | "
            f"Cliente: {transacao['nome']} | "
            f"Email: {transacao['email']} | "
            f"Valor: R$ {transacao['valor']:.2f} | "
            f"Data Crédito: {data_credito} | "
            f"Produto: {transacao['produto_nome']} | "
            f"Forma: {transacao['forma_pagamento']}"
        )
        
        # CRIAR CLIENTE NO OMIE
        print(f"  📤 Criando cliente no Omie...")
        sucesso_cli, codigo_cli, erro_cli = criar_cliente(transacao)
        
        if sucesso_cli:
            sucessos_cliente += 1
            print(f"  ✅ Cliente: OK")
        else:
            print(f"  ❌ Cliente: {erro_cli}")
        
        # CRIAR CONTA A RECEBER NO OMIE
        print(f"  📤 Criando conta a receber no Omie...")
        sucesso_cta, codigo_cta, erro_cta = criar_conta_receber(transacao)
        
        if sucesso_cta:
            sucessos_conta += 1
            print(f"  ✅ Conta: {codigo_cta}")
            processadas += 1
        else:
            print(f"  ❌ Conta: {erro_cta}")
            erros += 1
        
        # Salvar resultado
        resultado = {
            "transaction_id": transaction_id,
            "cliente": transacao['nome'],
            "valor": transacao['valor'],
            "cpf_vindi": cpf_vindi if extra and extra != '-' else None,
            "produto_vindi": produto_vindi if extra and extra != '-' else None,
            "sucesso_cliente": sucesso_cli,
            "sucesso_conta": sucesso_cta,
            "codigo_omie": codigo_cta if sucesso_cta else None,
            "erro": erro_cta if not sucesso_cta else None,
            "processado_em": datetime.now().isoformat()
        }
        resultados.append(resultado)
        
        # Rate limiting
        time.sleep(1)
    
    # RELATÓRIO FINAL
    print(f"\n{'='*80}")
    print("📊 RELATÓRIO FINAL")
    print(f"{'='*80}")
    print(f"📈 Total no CSV: {total}")
    print(f"✅ Processadas: {processadas}")
    print(f"⏭️  Puladas: {puladas}")
    print(f"❌ Erros: {erros}")
    print(f"👥 Clientes criados: {sucessos_cliente}")
    print(f"💰 Contas criadas: {sucessos_conta}")
    print(f"{'='*80}")
    
    # Salvar relatório JSON
    relatorio_arquivo = f"relatorio_importacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    relatorio = {
        "data_processamento": datetime.now().isoformat(),
        "arquivo_csv": arquivo_csv,
        "total_linhas": total,
        "processadas": processadas,
        "puladas": puladas,
        "erros": erros,
        "sucessos_cliente": sucessos_cliente,
        "sucessos_conta": sucessos_conta,
        "resultados": resultados
    }
    
    with open(relatorio_arquivo, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 Relatório salvo: {relatorio_arquivo}")
    print(f"\n🎉 IMPORTAÇÃO CONCLUÍDA!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("❌ Uso: python importar.py ARQUIVO.csv")
        print("📝 Exemplo: python importar.py dados.csv")
        sys.exit(1)
    
    arquivo = sys.argv[1]
    processar_csv(arquivo)

