#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE TESTE RÁPIDO - BD-LDI
===============================
Execução simplificada para testes e demonstrações rápidas
"""

import psycopg2
import pandas as pd
from datetime import datetime


def teste_conexao_rapido():
    """Teste rápido de conexão e execução de uma consulta simples"""
    print("🔍 TESTE RÁPIDO - BD-LDI")
    print("=" * 40)
    
    # Configurações de conexão
    config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'ldi',
        'user': 'ldi',
        'password': 'ldi123'
    }
    
    try:
        # Conectar
        print("📡 Conectando ao banco...")
        conn = psycopg2.connect(**config)
        conn.set_client_encoding('UTF-8')
        
        # Teste simples
        print("✅ Conexão estabelecida!")
        cursor = conn.cursor()
        
        # Verificar se as tabelas existem
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tabelas = cursor.fetchall()
        print(f"📊 Tabelas encontradas: {len(tabelas)}")
        
        if len(tabelas) > 0:
            print("\nTabelas no banco:")
            for tabela in tabelas:
                cursor.execute(f"SELECT COUNT(*) FROM {tabela[0]};")
                count = cursor.fetchone()[0]
                print(f"  • {tabela[0]}: {count} registros")
        else:
            print("⚠️  Nenhuma tabela encontrada. Execute o script principal primeiro.")
        
        # Consulta de teste simples
        if len(tabelas) > 0:
            print("\n🔍 Executando consulta de teste...")
            df = pd.read_sql_query("""
                SELECT u.nome, COUNT(r.id_reserva) as total_reservas
                FROM usuario u
                LEFT JOIN reserva r ON u.id_usuario = r.id_usuario
                GROUP BY u.nome
                ORDER BY total_reservas DESC
                LIMIT 5;
            """, conn)
            
            print("\n📊 Top 5 usuários por reservas:")
            print(df.to_string(index=False))
        
        conn.close()
        print("\n✅ Teste concluído com sucesso!")
        
    except psycopg2.Error as e:
        print(f"❌ Erro de conexão: {e}")
        print("\nVerifique se:")
        print("  • O Docker está rodando")
        print("  • O container PostgreSQL está ativo")
        print("  • Execute: cd SQL && docker-compose up -d")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")


if __name__ == "__main__":
    teste_conexao_rapido()
