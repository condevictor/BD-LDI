#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de conexão com banco de dados PostgreSQL
Sistema de Locação de Imóveis
"""

import psycopg2
import os
from pathlib import Path


class DatabaseManager:
    """Gerenciador de conexão e operações com banco PostgreSQL"""
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self):
        """Carrega configurações do arquivo .env"""
        # Busca .env em diferentes locais
        for env_path in ['.env', '../.env', Path(__file__).parent.parent / '.env']:
            if os.path.exists(env_path):
                self._load_env_file(env_path)
                break
        else:
            # Se não encontrar .env, usa valores padrão
            print("Arquivo .env não encontrado, usando valores padrão...")
        
        return {
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'DATABASE': os.getenv('DB_DATABASE', 'ldi'),
            'USER': os.getenv('DB_USER', 'ldi'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'ldi123')
        }
    
    def _load_env_file(self, env_path):
        """Carrega variáveis do arquivo .env"""
        with open(env_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    
    def get_connection(self):
        """Conecta ao banco PostgreSQL"""
        try:
            return psycopg2.connect(
                host=self.config['HOST'],
                port=int(self.config['PORT']),
                database=self.config['DATABASE'],
                user=self.config['USER'],
                password=self.config['PASSWORD']
            )
        except psycopg2.OperationalError as e:
            if "role" in str(e) and "does not exist" in str(e):
                raise ConnectionError(f"ERRO: Usuário '{self.config['USER']}' não existe no PostgreSQL")
            elif "Connection refused" in str(e):
                raise ConnectionError(f"ERRO: PostgreSQL não está rodando na porta {self.config['PORT']}")
            else:
                raise ConnectionError(f"ERRO de conexão: {e}")
    
    def execute_query(self, sql):
        """Executa consulta SQL e retorna resultados"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                return results, columns
    
    def execute_script(self, script_path):
        """Executa script SQL completo"""
        # Busca arquivo SQL em diferentes locais
        for path in [script_path, f"../{script_path}", Path(__file__).parent.parent / script_path]:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as file:
                    sql_content = file.read()
                break
        else:
            raise FileNotFoundError(f"Script SQL não encontrado: {script_path}")
        
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_content)
                conn.commit()


# Instância global
db_manager = DatabaseManager()
