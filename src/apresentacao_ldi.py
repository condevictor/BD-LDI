#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Locação de Imóveis 
=========================================================
Executa apenas as consultas já definidas no arquivo SQL
"""

import psycopg2
import configparser
import os
import sys


def carregar_configuracao():
    """Carrega configurações do arquivo config.ini"""
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    return config['DATABASE']


def conectar_banco(config_db):
    """Estabelece conexão com o banco de dados"""
    try:
        conexao = psycopg2.connect(
            host=config_db['host'],
            port=config_db['port'],
            database=config_db['database'],
            user=config_db['user'],
            password=config_db['password']
        )
        return conexao
    except Exception as e:
        print(f"ERRO na conexao: {e}")
        return None


def executar_consulta_simples(conexao, sql):
    """Executa uma consulta e mostra resultados simples (max 10 linhas)"""
    try:
        cursor = conexao.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
        cursor.close()
        
        if not resultados:
            print("Nenhum resultado encontrado.")
            return
        
        # Mostrar cabeçalho
        print(" | ".join(f"{col[:15]:<15}" for col in colunas))
        print("-" * (len(colunas) * 18))
        
        # Mostrar dados (max 10 linhas)
        for linha in resultados[:10]:
            valores = []
            for item in linha:
                texto = str(item)[:15] if item is not None else ""
                valores.append(f"{texto:<15}")
            print(" | ".join(valores))
        
        print(f"\nTotal: {len(resultados)} registros")
        if len(resultados) > 10:
            print("(Mostrando apenas primeiros 10)")
            
    except Exception as e:
        print(f"ERRO: {e}")


def extrair_consultas_do_sql():
    """Extrai as consultas prontas do arquivo SQL"""
    consultas = []
    arquivo_sql = "SQL/v2-ldi.sql"
    
    try:
        with open(arquivo_sql, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        consulta_atual = ""
        titulo_atual = ""
        dentro_consulta = False
        
        for linha in linhas:
            linha = linha.strip()
            
            # Identificar início de consulta
            if linha.startswith("-- Consulta") and ":" in linha:
                if consulta_atual and titulo_atual:
                    consultas.append({"titulo": titulo_atual, "sql": consulta_atual.strip()})
                
                titulo_atual = linha.split(": ", 1)[1] if ": " in linha else linha
                consulta_atual = ""
                dentro_consulta = True
                continue
            
            # Parar na próxima consulta ou seção
            if linha.startswith("-- =") or linha.startswith("-- 💰") or linha.startswith("-- 📊"):
                if consulta_atual and titulo_atual:
                    consultas.append({"titulo": titulo_atual, "sql": consulta_atual.strip()})
                    consulta_atual = ""
                    titulo_atual = ""
                dentro_consulta = False
                continue
            
            # Coletar SQL
            if dentro_consulta and linha and not linha.startswith("--"):
                consulta_atual += linha + "\n"
        
        # Adicionar última consulta
        if consulta_atual and titulo_atual:
            consultas.append({"titulo": titulo_atual, "sql": consulta_atual.strip()})
            
        return consultas
        
    except Exception as e:
        print(f"ERRO ao ler arquivo SQL: {e}")
        return []


def main():
    """Função principal simplificada"""
    print("SISTEMA DE LOCACAO DE IMOVEIS")
    print("=" * 40)
    
    # Conectar
    print("Conectando ao banco...")
    config_db = carregar_configuracao()
    conexao = conectar_banco(config_db)
    if not conexao:
        return
    
    # Executar script SQL completo (cria banco + dados)
    print("Executando script SQL completo...")
    try:
        with open("SQL/v2-ldi.sql", 'r', encoding='utf-8') as f:
            sql_script = f.read()
        cursor = conexao.cursor()
        cursor.execute(sql_script)
        conexao.commit()
        cursor.close()
        print("Banco criado e populado com sucesso!")
    except Exception as e:
        print(f"ERRO ao executar SQL: {e}")
        return
    
    # Extrair e executar consultas
    print("\nExtração e execução das consultas:")
    print("=" * 40)
    
    consultas = extrair_consultas_do_sql()
    
    if not consultas:
        print("ERRO: Nenhuma consulta encontrada no arquivo SQL")
        return
    
    for i, consulta in enumerate(consultas, 1):
        print(f"\n[{i}/21] {consulta['titulo']}")
        print("-" * 50)
        executar_consulta_simples(conexao, consulta['sql'])
        
        if i % 5 == 0:  # Pausa a cada 5 consultas
            input("\nPressione ENTER para continuar...")
    
    conexao.close()
    print(f"\nConcluído! {len(consultas)} consultas executadas.")


if __name__ == "__main__":
    main()
