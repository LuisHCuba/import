#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Web para Importação CSV → Vindi → Omie
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import threading
from datetime import datetime
from werkzeug.utils import secure_filename
from importar import processar_csv as processar_csv_original
from vindi_api import extrair_dados_vindi
from omie_api import criar_cliente, criar_conta_receber
from utils import parse_valor, parse_data, gerar_cpf_valido
import csv
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RELATORIOS_FOLDER'] = 'relatorios'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Garantir pastas existem
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RELATORIOS_FOLDER'], exist_ok=True)

# Estado global da importação
importacao_estado = {
    'em_andamento': False,
    'progresso': 0,
    'total': 0,
    'processadas': 0,
    'erros': 0,
    'puladas': 0,
    'mensagem': '',
    'logs': [],
    'arquivo_atual': None
}


def adicionar_log(mensagem, tipo='info'):
    """Adiciona log ao estado"""
    importacao_estado['logs'].append({
        'timestamp': datetime.now().isoformat(),
        'tipo': tipo,
        'mensagem': mensagem
    })
    
    # Manter apenas últimos 100 logs
    if len(importacao_estado['logs']) > 100:
        importacao_estado['logs'] = importacao_estado['logs'][-100:]


def processar_csv_async(arquivo_path):
    """Processa CSV de forma assíncrona"""
    global importacao_estado
    
    importacao_estado['em_andamento'] = True
    importacao_estado['progresso'] = 0
    importacao_estado['logs'] = []
    
    adicionar_log(f"📂 Iniciando processamento: {os.path.basename(arquivo_path)}", 'success')
    
    try:
        # Ler CSV
        adicionar_log("📖 Lendo arquivo CSV...", 'info')
        linhas = []
        
        with open(arquivo_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            linhas = list(reader)
        
        importacao_estado['total'] = len(linhas)
        adicionar_log(f"✅ {len(linhas)} linhas carregadas", 'success')
        
        # Processar cada linha
        processadas = 0
        sucessos = 0
        erros = 0
        puladas = 0
        
        for i, linha in enumerate(linhas):
            importacao_estado['progresso'] = i + 1
            
            # Extrair dados
            transaction_id = linha.get('Id', '').strip()
            status = linha.get('Status', '').strip()
            data_credito = linha.get('Data Credito', '').strip()
            extra = linha.get('Extra', '').strip()
            
            # Filtrar
            if status in ['Cancelada', 'Aguardando Pagamento']:
                puladas += 1
                importacao_estado['puladas'] = puladas
                adicionar_log(f"⏭️ Pulada #{transaction_id}: {status}", 'warning')
                continue
            
            if not data_credito or data_credito == '-':
                puladas += 1
                importacao_estado['puladas'] = puladas
                adicionar_log(f"⏭️ Pulada #{transaction_id}: Sem data crédito", 'warning')
                continue
            
            # Preparar transação
            transacao = {
                'id': transaction_id,
                'nome': linha.get('Cliente', '').strip(),
                'email': linha.get('E-mail do cliente', '').strip(),
                'valor': parse_valor(linha.get('Valor', '0')),
                'valor_liquido': parse_valor(linha.get('Valor loja', '0')),
                'taxa': parse_valor(linha.get('Taxa', '0')),
                'data_credito_formatada': parse_data(data_credito),
                'forma_pagamento': linha.get('Meio de Pagamento', '').strip(),
                'cpf_cnpj': gerar_cpf_valido(transaction_id),
                'produto_nome': 'Serviço',
                'charge_id': extra
            }
            
            adicionar_log(f"📋 Processando #{transaction_id}: {transacao['nome']}", 'info')
            
            # Enriquecer com Vindi
            if extra and extra != '-':
                cpf_vindi, produto_vindi, erro = extrair_dados_vindi(extra)
                
                if cpf_vindi:
                    transacao['cpf_cnpj'] = cpf_vindi
                    adicionar_log(f"  ✅ CPF: {cpf_vindi}", 'success')
                
                if produto_vindi:
                    transacao['produto_nome'] = produto_vindi
                    adicionar_log(f"  ✅ Produto: {produto_vindi}", 'success')
            
            transacao['observacao'] = f"Transação {transaction_id} | {transacao['nome']} | R$ {transacao['valor']:.2f}"
            
            # Criar cliente
            sucesso_cli, _, _ = criar_cliente(transacao)
            
            # Criar conta
            sucesso_cta, codigo, erro_cta = criar_conta_receber(transacao)
            
            if sucesso_cta:
                sucessos += 1
                processadas += 1
                adicionar_log(f"  ✅ Importada! Código Omie: {codigo}", 'success')
            else:
                erros += 1
                adicionar_log(f"  ❌ Erro: {erro_cta}", 'error')
            
            importacao_estado['processadas'] = processadas
            importacao_estado['erros'] = erros
            
            time.sleep(1)  # Rate limiting
        
        # Finalizar
        adicionar_log(f"\n🎉 CONCLUÍDO! {processadas} importadas, {erros} erros, {puladas} puladas", 'success')
        
    except Exception as e:
        adicionar_log(f"💥 ERRO GERAL: {str(e)}", 'error')
    
    finally:
        importacao_estado['em_andamento'] = False


@app.route('/')
def index():
    """Página principal"""
    from config import get_config, validar_config
    config = get_config()
    config_ok, erros = validar_config(config)
    
    return render_template('index.html', config_ok=config_ok, erros=erros)


@app.route('/configuracoes')
def configuracoes():
    """Página de configurações"""
    from config import get_config
    config = get_config()
    
    # Mascarar tokens para exibição
    config_display = config.copy()
    if config_display.get('VINDI_TOKEN'):
        token = config_display['VINDI_TOKEN']
        config_display['VINDI_TOKEN_DISPLAY'] = f"{token[:10]}...{token[-5:]}" if len(token) > 15 else token
    
    return render_template('configuracoes.html', config=config_display)


@app.route('/api/configuracoes', methods=['GET', 'POST'])
def api_configuracoes():
    """API para gerenciar configurações"""
    from config import get_config, atualizar_config, validar_config
    
    if request.method == 'GET':
        config = get_config()
        
        # Mascarar tokens
        config_display = config.copy()
        if config_display.get('VINDI_TOKEN'):
            token = config_display['VINDI_TOKEN']
            config_display['VINDI_TOKEN_MASKED'] = f"{token[:10]}...{token[-5:]}" if len(token) > 15 else token
        else:
            config_display['VINDI_TOKEN_MASKED'] = ''
        
        config_ok, erros = validar_config(config)
        
        return jsonify({
            'config': config_display,
            'valido': config_ok,
            'erros': erros
        })
    
    elif request.method == 'POST':
        nova_config = request.json
        
        # Validar
        config_ok, erros = validar_config(nova_config)
        
        if not config_ok:
            return jsonify({'sucesso': False, 'erros': erros}), 400
        
        # Salvar
        atualizar_config(nova_config)
        
        return jsonify({'sucesso': True, 'mensagem': 'Configurações salvas com sucesso!'})


@app.route('/api/upload', methods=['POST'])
def upload_csv():
    """Upload de arquivo CSV"""
    if 'file' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'erro': 'Arquivo vazio'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'erro': 'Apenas arquivos CSV são permitidos'}), 400
    
    # Salvar arquivo
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename_final = f"{timestamp}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_final)
    file.save(filepath)
    
    # Iniciar processamento em thread separada
    importacao_estado['arquivo_atual'] = filename_final
    thread = threading.Thread(target=processar_csv_async, args=(filepath,))
    thread.start()
    
    return jsonify({
        'sucesso': True,
        'mensagem': 'Upload realizado! Processamento iniciado...',
        'arquivo': filename_final
    })


@app.route('/api/status')
def status():
    """Retorna status atual da importação"""
    return jsonify(importacao_estado)


@app.route('/api/relatorios')
def listar_relatorios():
    """Lista todos os relatórios gerados"""
    try:
        relatorios = []
        for arquivo in os.listdir(app.config['RELATORIOS_FOLDER']):
            if arquivo.startswith('relatorio_') and arquivo.endswith('.json'):
                filepath = os.path.join(app.config['RELATORIOS_FOLDER'], arquivo)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                relatorios.append({
                    'arquivo': arquivo,
                    'data': dados.get('data_processamento'),
                    'processadas': dados.get('processadas', 0),
                    'erros': dados.get('erros', 0)
                })
        
        relatorios.sort(key=lambda x: x['data'], reverse=True)
        return jsonify(relatorios)
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/relatorio/<arquivo>')
def download_relatorio(arquivo):
    """Download de relatório específico"""
    filepath = os.path.join(app.config['RELATORIOS_FOLDER'], arquivo)
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({'erro': 'Relatório não encontrado'}), 404


if __name__ == '__main__':
    print("="*80)
    print("🌐 IMPORTADOR CSV → VINDI → OMIE")
    print("="*80)
    print("Acesse: http://localhost:5000")
    print("="*80)
    app.run(host='0.0.0.0', port=5000, debug=False)

