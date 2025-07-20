#!/usr/bin/env python3
"""
Script para executar o sistema de locação com Streamlit
Inicializa o banco de dados e executa a aplicação web
"""

import subprocess
import sys
import os
import psycopg2
import configparser

def carregar_configuracao():
    """Carrega configurações do banco"""
    config = configparser.ConfigParser()
    config.read('../config.ini', encoding='utf-8')
    return {
        'host': config['DATABASE']['HOST'],
        'port': int(config['DATABASE']['PORT']), 
        'database': config['DATABASE']['DATABASE'],
        'user': config['DATABASE']['USER'],
        'password': config['DATABASE']['PASSWORD']
    }

def inicializar_banco():
    """Inicializa o banco de dados"""
    print("🔧 Inicializando banco de dados...")
    
    try:
        config = carregar_configuracao()
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        # Executar script SQL
        with open('../SQL/v2-ldi.sql', 'r', encoding='utf-8') as file:
            sql_script = file.read()
            cursor.execute(sql_script)
            conn.commit()
        
        cursor.close()
        conn.close()
        print("✅ Banco de dados inicializado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        return False

def executar_streamlit():
    """Executa o aplicativo Streamlit"""
    print("🚀 Iniciando aplicação Streamlit...")
    print("📱 A aplicação será aberta no seu navegador em: http://localhost:8501")
    print("🛑 Para parar, pressione Ctrl+C")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "../src/app_streamlit.py",
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada!")
    except Exception as e:
        print(f"❌ Erro ao executar Streamlit: {e}")

def main():
    """Função principal"""
    print("🏠 SISTEMA DE LOCAÇÃO DE IMÓVEIS - STREAMLIT")
    print("=" * 50)
    
    # Verificar se o banco está acessível
    if inicializar_banco():
        print("\n" + "=" * 50)
        executar_streamlit()
    else:
        print("❌ Não foi possível inicializar o sistema.")
        sys.exit(1)

if __name__ == "__main__":
    main()
