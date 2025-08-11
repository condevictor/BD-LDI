#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Locação de Imóveis - Demonstração SQL
Executa as 21 consultas definidas no arquivo SQL
"""

import os
from database import db_manager


def executar_consulta(sql, titulo):
    """Executa uma consulta e exibe resultados formatados"""
    try:
        resultados, colunas = db_manager.execute_query(sql)
        
        print(f"\n{titulo}")
        print("-" * 60)
        
        if not resultados:
            print("Nenhum resultado encontrado.")
            return
        
        # Exibir cabeçalho
        header = " | ".join(f"{col[:15]:<15}" for col in colunas)
        print(header)
        print("-" * len(header))
        
        # Exibir dados (máximo 10 linhas)
        for linha in resultados[:10]:
            valores = []
            for item in linha:
                texto = str(item)[:15] if item is not None else ""
                valores.append(f"{texto:<15}")
            print(" | ".join(valores))
        
        print(f"\nTotal: {len(resultados)} registros")
        if len(resultados) > 10:
            print("(Mostrando apenas 10 primeiros)")
            
    except Exception as e:
        print(f"ERRO: {e}")


def extrair_consultas():
    """Extrai consultas do arquivo SQL"""
    consultas = []
    
    try:
        # Busca o arquivo SQL
        for sql_path in ["./v2-ldi.sql", "SQL/v2-ldi.sql", "../SQL/v2-ldi.sql"]:
            if os.path.exists(sql_path):
                with open(sql_path, 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
                break
        else:
            raise FileNotFoundError("Arquivo SQL não encontrado")
        
        consulta_atual = ""
        titulo_atual = ""
        dentro_consulta = False
        
        for linha in linhas:
            linha = linha.strip()
            
            # Identifica início de consulta
            if linha.startswith("-- Consulta") and ":" in linha:
                if consulta_atual and titulo_atual:
                    consultas.append({"titulo": titulo_atual, "sql": consulta_atual.strip()})
                
                titulo_atual = linha.split(": ", 1)[1]
                consulta_atual = ""
                dentro_consulta = True
                continue
            
            # Para na próxima seção
            if linha.startswith("-- =") or linha.startswith("-- 💰") or linha.startswith("-- 📊"):
                if consulta_atual and titulo_atual:
                    consultas.append({"titulo": titulo_atual, "sql": consulta_atual.strip()})
                    consulta_atual = ""
                    titulo_atual = ""
                dentro_consulta = False
                continue
            
            # Coleta SQL
            if dentro_consulta and linha and not linha.startswith("--"):
                consulta_atual += linha + "\n"
        
        # Adiciona última consulta
        if consulta_atual and titulo_atual:
            consultas.append({"titulo": titulo_atual, "sql": consulta_atual.strip()})
            
        return consultas
        
    except Exception as e:
        print(f"ERRO ao ler arquivo SQL: {e}")
        return []


def main():
    """Função principal"""
    print("SISTEMA DE LOCAÇÃO DE IMÓVEIS")
    print("=" * 60)
    
    try:
        # Inicializa banco de dados
        print("Inicializando banco de dados...")
        db_manager.execute_script("SQL/v2-ldi.sql")
        print("Banco criado e populado com sucesso!")
        
        # Executa consultas
        consultas = extrair_consultas()
        
        if not consultas:
            print("ERRO: Nenhuma consulta encontrada")
            return
        
        print(f"\nExecutando {len(consultas)} consultas:")
        
        for i, consulta in enumerate(consultas, 1):
            print(f"\n[{i}/{len(consultas)}]", end=" ")
            executar_consulta(consulta['sql'], consulta['titulo'])
            
            # Pausa a cada 5 consultas
            if i % 5 == 0 and i < len(consultas):
                input("\nPressione ENTER para continuar...")
        
        print(f"\nConcluído! {len(consultas)} consultas executadas.")
        
    except ConnectionError as e:
        print(f"\n{e}")
        print("\nVerifique se:")
        print("1. PostgreSQL está rodando (docker-compose up -d)")
        print("2. Credenciais em config.ini estão corretas")
        
    except Exception as e:
        print(f"\nERRO: {e}")


if __name__ == "__main__":
    main()
