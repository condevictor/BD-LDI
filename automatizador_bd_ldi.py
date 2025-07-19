#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AGENTE DE AUTOMAÇÃO DE BANCO DE DADOS - SISTEMA DE LOCAÇÃO DE IMÓVEIS POR TEMPORADA
===================================================================================

Este script automatiza a execução e apresentação dos resultados do banco de dados
de locação de imóveis por temporada (LDI), incluindo:
- Criação e população das tabelas
- Execução de 20 consultas analíticas
- Apresentação formatada dos resultados
- Estatísticas e relatórios detalhados

Autor: Agente de Automação PostgreSQL
Data: 19/07/2025
Versão: 1.0
"""

import psycopg2
import pandas as pd
import time
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging
from contextlib import contextmanager


class ConfiguradorBD:
    """Classe para gerenciar configurações do banco de dados"""
    
    def __init__(self):
        self.host = "localhost"
        self.port = 5432
        self.database = "ldi"
        self.user = "ldi"
        self.password = "ldi123"
        self.encoding = "UTF-8"
    
    def obter_string_conexao(self) -> str:
        """Retorna string de conexão PostgreSQL"""
        return f"host={self.host} port={self.port} dbname={self.database} user={self.user} password={self.password}"


class AutomatizadorBDLDI:
    """
    Classe principal para automação do banco de dados LDI
    """
    
    def __init__(self, config: ConfiguradorBD, recriar_tabelas: bool = True):
        self.config = config
        self.recriar_tabelas = recriar_tabelas
        self.conexao = None
        self.resultados_consultas = {}
        self.estatisticas_execucao = {}
        self.log_execucao = []
        
        # Configurar logging
        self._configurar_logging()
        
        # Definir consultas
        self.consultas = self._definir_consultas()
    
    def _configurar_logging(self):
        """Configura sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ldi_automation.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    @contextmanager
    def conexao_bd(self):
        """Context manager para conexão com banco de dados"""
        try:
            self.conexao = psycopg2.connect(self.config.obter_string_conexao())
            self.conexao.set_client_encoding(self.config.encoding)
            self.logger.info("✅ Conexão com banco de dados estabelecida")
            yield self.conexao
        except psycopg2.Error as e:
            self.logger.error(f"❌ Erro na conexão: {e}")
            raise
        finally:
            if self.conexao:
                self.conexao.close()
                self.logger.info("🔒 Conexão com banco de dados fechada")
    
    def testar_conexao(self) -> bool:
        """Testa conexão com o banco de dados"""
        try:
            with self.conexao_bd() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT version();")
                resultado = cursor.fetchone()
                if resultado:
                    versao = resultado[0]
                    self.logger.info(f"📊 PostgreSQL Version: {versao}")
                else:
                    self.logger.warning("⚠️ Não foi possível obter a versão do PostgreSQL")
                return True
        except Exception as e:
            self.logger.error(f"❌ Falha no teste de conexão: {e}")
            return False
    
    def carregar_script_sql(self) -> str:
        """Carrega o script SQL principal"""
        caminho_sql = os.path.join(os.path.dirname(__file__), 'SQL', 'v2-ldi.sql')
        try:
            with open(caminho_sql, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
                self.logger.info(f"📁 Script SQL carregado: {caminho_sql}")
                return conteudo
        except FileNotFoundError:
            self.logger.error(f"❌ Arquivo SQL não encontrado: {caminho_sql}")
            raise
        except Exception as e:
            self.logger.error(f"❌ Erro ao carregar SQL: {e}")
            raise
    
    def executar_criacao_populacional(self):
        """Executa criação das tabelas e população de dados"""
        self.logger.info("🏗️  Iniciando criação e população do banco de dados...")
        
        try:
            with self.conexao_bd() as conn:
                cursor = conn.cursor()
                
                # Carregar script SQL
                script_sql = self.carregar_script_sql()
                
                # Separar criação/população das consultas
                partes = script_sql.split('-- CONSULTAS SQL --')
                script_criacao = partes[0]
                
                if self.recriar_tabelas:
                    self.logger.info("🗑️  Removendo tabelas existentes...")
                    cursor.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
                
                # Executar script de criação e população
                self.logger.info("📝 Executando script de criação e população...")
                cursor.execute(script_criacao)
                conn.commit()
                
                self.logger.info("✅ Banco de dados criado e populado com sucesso!")
                
        except Exception as e:
            self.logger.error(f"❌ Erro na criação/população: {e}")
            raise
    
    def _definir_consultas(self) -> Dict[int, Dict[str, str]]:
        """Define todas as 20 consultas com suas descrições"""
        return {
            1: {
                "titulo": "Imóveis com Wi-Fi disponíveis entre datas específicas",
                "descricao": "Lista imóveis que possuem Wi-Fi e estão disponíveis no período de 05/08 a 10/08/2025",
                "sql": """
                SELECT i.* FROM imovel i
                JOIN comodidades c ON i.id_imovel = c.id_imovel
                WHERE c.comodidade = 'Wi-Fi'
                AND i.id_imovel NOT IN (
                  SELECT id_imovel FROM reserva
                  WHERE status IN ('confirmada', 'pendente')
                  AND ('2025-08-05' BETWEEN data_inicio AND data_fim OR
                       '2025-08-10' BETWEEN data_inicio AND data_fim OR
                       (data_inicio BETWEEN '2025-08-05' AND '2025-08-10'))
                );
                """
            },
            2: {
                "titulo": "Reservas feitas por um determinado hóspede",
                "descricao": "Mostra todas as reservas realizadas por 'Ana Souza'",
                "sql": """
                SELECT r.*, u.nome FROM reserva r
                JOIN usuario u ON r.id_usuario = u.id_usuario
                WHERE u.nome = 'Ana Souza';
                """
            },
            3: {
                "titulo": "Imóveis com média de avaliação acima de 4",
                "descricao": "Lista imóveis bem avaliados pelos hóspedes (nota média > 4)",
                "sql": """
                SELECT i.titulo, AVG(a.nota) as media_avaliacao
                FROM imovel i
                JOIN reserva r ON i.id_imovel = r.id_imovel
                JOIN experiencia_avaliada ea ON r.id_reserva = ea.id_reserva
                JOIN avaliacao a ON ea.id_avaliacao = a.id_avaliacao
                GROUP BY i.titulo, i.id_imovel
                HAVING AVG(a.nota) > 4;
                """
            },
            4: {
                "titulo": "Pagamentos (principais e adicionais) por reserva",
                "descricao": "Relatório completo de pagamentos incluindo valores principais e multas",
                "sql": """
                SELECT r.id_reserva, 'Principal' as tipo, p.valor_total, p.forma_pagamento, p.data_pagamento
                FROM reserva r
                JOIN gera g ON r.id_reserva = g.id_reserva
                JOIN pagamento p ON g.id_pagamento = p.id_pagamento
                UNION ALL
                SELECT r.id_reserva, 'Multa' as tipo, p.valor_total, p.forma_pagamento, p.data_pagamento
                FROM reserva r
                JOIN reserva_cancelada rc ON EXISTS (
                    SELECT 1 FROM gera g2 WHERE g2.id_reserva = r.id_reserva AND g2.id_pagamento = rc.id_pagamento
                )
                JOIN gera_multa gm ON rc.id_cancelamento = gm.id_cancelamento
                JOIN gera_pag_multa gpm ON gm.id_multa = gpm.id_multa
                JOIN pagamento p ON gpm.id_pagamento = p.id_pagamento;
                """
            },
            5: {
                "titulo": "Hóspedes que contrataram serviços extras",
                "descricao": "Lista de hóspedes e os serviços extras contratados",
                "sql": """
                SELECT DISTINCT u.nome AS hospede, se.nome AS servico
                FROM reserva r
                JOIN servicos_vinculados sv ON r.id_reserva = sv.id_reserva
                JOIN servico_extra se ON sv.id_servico = se.id_servico
                JOIN usuario u ON r.id_usuario = u.id_usuario;
                """
            },
            6: {
                "titulo": "Imóveis com mais comodidades",
                "descricao": "Ranking de imóveis por quantidade de comodidades oferecidas",
                "sql": """
                SELECT i.titulo, COUNT(c.comodidade) AS qtd_comodidades
                FROM imovel i
                JOIN comodidades c ON i.id_imovel = c.id_imovel
                GROUP BY i.titulo, i.id_imovel
                ORDER BY qtd_comodidades DESC;
                """
            },
            7: {
                "titulo": "Reservas canceladas com multa aplicada",
                "descricao": "Reservas canceladas que resultaram em aplicação de multa",
                "sql": """
                SELECT r.id_reserva, u.nome AS hospede, m.valor_multa
                FROM reserva r
                JOIN usuario u ON r.id_usuario = u.id_usuario
                JOIN gera g ON r.id_reserva = g.id_reserva
                JOIN reserva_cancelada rc ON g.id_pagamento = rc.id_pagamento
                JOIN gera_multa gm ON rc.id_cancelamento = gm.id_cancelamento
                JOIN multa m ON gm.id_multa = m.id_multa
                WHERE r.status = 'cancelada';
                """
            },
            8: {
                "titulo": "Parcelas em aberto (com vencimento futuro)",
                "descricao": "Lista de parcelas ainda não vencidas",
                "sql": """
                SELECT p.id_pagamento, p.num_parcelas, p.valor_parcela, p.data_vencimento
                FROM parcela p
                WHERE p.data_vencimento > CURRENT_DATE;
                """
            },
            9: {
                "titulo": "Total arrecadado por imóvel",
                "descricao": "Ranking de imóveis por receita total gerada",
                "sql": """
                SELECT i.titulo, SUM(p.valor_total) AS total_recebido
                FROM imovel i
                JOIN reserva r ON i.id_imovel = r.id_imovel
                JOIN gera g ON r.id_reserva = g.id_reserva
                JOIN pagamento p ON g.id_pagamento = p.id_pagamento
                WHERE r.status = 'confirmada'
                GROUP BY i.titulo, i.id_imovel
                ORDER BY total_recebido DESC;
                """
            },
            10: {
                "titulo": "Hóspedes que mais reservaram imóveis",
                "descricao": "Ranking de hóspedes por quantidade de reservas realizadas",
                "sql": """
                SELECT u.nome, COUNT(*) AS total_reservas
                FROM usuario u
                JOIN reserva r ON u.id_usuario = r.id_usuario
                GROUP BY u.nome, u.id_usuario
                ORDER BY total_reservas DESC;
                """
            },
            11: {
                "titulo": "Verificar disponibilidade de imóvel em período específico",
                "descricao": "Imóveis disponíveis no período de 01/08 a 10/08/2025",
                "sql": """
                SELECT i.titulo, i.id_imovel
                FROM imovel i
                WHERE i.id_imovel NOT IN (
                    SELECT r.id_imovel 
                    FROM reserva r 
                    WHERE r.status IN ('confirmada', 'pendente')
                    AND (
                        ('2025-08-01' BETWEEN r.data_inicio AND r.data_fim) OR
                        ('2025-08-10' BETWEEN r.data_inicio AND r.data_fim) OR
                        (r.data_inicio BETWEEN '2025-08-01' AND '2025-08-10')
                    )
                );
                """
            },
            12: {
                "titulo": "Receita total por anfitrião (incluindo serviços extras)",
                "descricao": "Ranking de anfitriões por receita total gerada",
                "sql": """
                SELECT u.nome AS anfitriao, 
                       SUM(p.valor_total) AS receita_total
                FROM usuario u
                JOIN anfitriao a ON u.id_usuario = a.id_usuario
                JOIN imovel i ON a.id_usuario = i.id_usuario
                JOIN reserva r ON i.id_imovel = r.id_imovel
                JOIN gera g ON r.id_reserva = g.id_reserva
                JOIN pagamento p ON g.id_pagamento = p.id_pagamento
                WHERE r.status = 'confirmada'
                GROUP BY u.nome
                ORDER BY receita_total DESC;
                """
            },
            13: {
                "titulo": "Cancelamentos por tipo de política",
                "descricao": "Análise de cancelamentos agrupados por política de cancelamento",
                "sql": """
                SELECT pc.tipo_politica, COUNT(*) AS total_cancelamentos
                FROM politica_cancelamento pc
                JOIN imovel i ON pc.id_politica = i.id_politica
                JOIN reserva r ON i.id_imovel = r.id_imovel
                WHERE r.status = 'cancelada'
                GROUP BY pc.tipo_politica;
                """
            },
            14: {
                "titulo": "Serviços extras mais contratados",
                "descricao": "Ranking de serviços extras por demanda",
                "sql": """
                SELECT se.nome, COUNT(*) AS vezes_contratado
                FROM servico_extra se
                JOIN servicos_vinculados sv ON se.id_servico = sv.id_servico
                GROUP BY se.nome
                ORDER BY vezes_contratado DESC;
                """
            },
            15: {
                "titulo": "Parcelas em atraso",
                "descricao": "Lista de parcelas com vencimento em atraso",
                "sql": """
                SELECT pp.id_pagamento, pp.num_parcelas, pp.valor_parcela, pp.data_vencimento
                FROM parcela pp
                WHERE pp.data_vencimento < CURRENT_DATE;
                """
            },
            16: {
                "titulo": "Imóveis disponíveis por capacidade e cidade",
                "descricao": "Imóveis em São Paulo com capacidade >= 4 pessoas disponíveis hoje",
                "sql": """
                SELECT i.titulo, i.capacidade_max, i.cidade, i.valor_diaria
                FROM imovel i
                WHERE i.capacidade_max >= 4 
                AND i.cidade = 'São Paulo'
                AND i.id_imovel NOT IN (
                    SELECT r.id_imovel FROM reserva r 
                    WHERE r.status IN ('confirmada', 'pendente')
                    AND CURRENT_DATE BETWEEN r.data_inicio AND r.data_fim
                );
                """
            },
            17: {
                "titulo": "Histórico completo de um imóvel (reservas, cancelamentos, avaliações)",
                "descricao": "Histórico detalhado da 'Casa da Praia'",
                "sql": """
                SELECT 
                    i.titulo,
                    r.id_reserva,
                    u.nome as hospede,
                    r.data_inicio,
                    r.data_fim,
                    r.status,
                    a.nota,
                    a.comentario,
                    CASE 
                        WHEN r.status = 'cancelada' THEN c.data_cancelamento
                        ELSE NULL 
                    END as data_cancelamento
                FROM imovel i
                LEFT JOIN reserva r ON i.id_imovel = r.id_imovel
                LEFT JOIN usuario u ON r.id_usuario = u.id_usuario
                LEFT JOIN experiencia_avaliada ea ON r.id_reserva = ea.id_reserva
                LEFT JOIN avaliacao a ON ea.id_avaliacao = a.id_avaliacao
                LEFT JOIN gera g ON r.id_reserva = g.id_reserva
                LEFT JOIN reserva_cancelada rc ON g.id_pagamento = rc.id_pagamento
                LEFT JOIN cancelamento c ON rc.id_cancelamento = c.id_cancelamento
                WHERE i.titulo = 'Casa da Praia'
                ORDER BY r.data_inicio;
                """
            },
            18: {
                "titulo": "Receita mensal por anfitrião",
                "descricao": "Receita mensal detalhada por anfitrião",
                "sql": """
                SELECT 
                    u.nome as anfitriao,
                    EXTRACT(YEAR FROM p.data_pagamento) as ano,
                    EXTRACT(MONTH FROM p.data_pagamento) as mes,
                    SUM(p.valor_total) as receita_mensal
                FROM usuario u
                JOIN anfitriao a ON u.id_usuario = a.id_usuario
                JOIN imovel i ON a.id_usuario = i.id_usuario
                JOIN reserva r ON i.id_imovel = r.id_imovel
                JOIN gera g ON r.id_reserva = g.id_reserva
                JOIN pagamento p ON g.id_pagamento = p.id_pagamento
                WHERE r.status = 'confirmada'
                GROUP BY u.nome, u.id_usuario, EXTRACT(YEAR FROM p.data_pagamento), EXTRACT(MONTH FROM p.data_pagamento)
                ORDER BY ano DESC, mes DESC, receita_mensal DESC;
                """
            },
            19: {
                "titulo": "Análise de estornos por política de cancelamento",
                "descricao": "Estatísticas de estornos agrupadas por tipo de política",
                "sql": """
                SELECT 
                    pc.tipo_politica,
                    COUNT(*) as total_estornos,
                    AVG(e.valor_estorno) as valor_medio_estorno,
                    SUM(e.valor_estorno) as valor_total_estornos
                FROM politica_cancelamento pc
                JOIN imovel i ON pc.id_politica = i.id_politica
                JOIN reserva r ON i.id_imovel = r.id_imovel
                JOIN gera g ON r.id_reserva = g.id_reserva
                JOIN reserva_cancelada rc ON g.id_pagamento = rc.id_pagamento
                JOIN gera_estorno ge ON rc.id_cancelamento = ge.id_cancelamento
                JOIN estorno e ON ge.id_estorno = e.id_estorno
                GROUP BY pc.tipo_politica;
                """
            },
            20: {
                "titulo": "Relatório de ocupação por imóvel",
                "descricao": "Estatísticas completas de ocupação e utilização dos imóveis",
                "sql": """
                SELECT 
                    i.titulo,
                    COUNT(CASE WHEN r.status = 'confirmada' THEN 1 END) as reservas_confirmadas,
                    COUNT(CASE WHEN r.status = 'cancelada' THEN 1 END) as reservas_canceladas,
                    COUNT(CASE WHEN r.status = 'pendente' THEN 1 END) as reservas_pendentes,
                    AVG(r.num_hospedes) as media_hospedes_por_reserva,
                    SUM(CASE WHEN r.status = 'confirmada' THEN (r.data_fim - r.data_inicio) ELSE 0 END) as total_dias_ocupados
                FROM imovel i
                LEFT JOIN reserva r ON i.id_imovel = r.id_imovel
                GROUP BY i.titulo, i.id_imovel
                ORDER BY reservas_confirmadas DESC;
                """
            }
        }
    
    def executar_consulta(self, numero_consulta: int) -> Tuple[pd.DataFrame, float]:
        """Executa uma consulta específica e retorna resultados + tempo de execução"""
        consulta_info = self.consultas[numero_consulta]
        
        try:
            with self.conexao_bd() as conn:
                inicio = time.time()
                
                # Executar consulta usando pandas para melhor formatação
                df = pd.read_sql_query(consulta_info["sql"], conn)
                
                tempo_execucao = time.time() - inicio
                
                self.logger.info(f"✅ Consulta {numero_consulta} executada em {tempo_execucao:.3f}s")
                return df, tempo_execucao
                
        except Exception as e:
            self.logger.error(f"❌ Erro na consulta {numero_consulta}: {e}")
            raise
    
    def executar_todas_consultas(self):
        """Executa todas as 20 consultas sequencialmente"""
        self.logger.info("🔍 Iniciando execução de todas as consultas...")
        
        for i in range(1, 21):
            self.logger.info(f"📊 Executando Consulta {i}: {self.consultas[i]['titulo']}")
            
            try:
                df, tempo = self.executar_consulta(i)
                self.resultados_consultas[i] = df
                self.estatisticas_execucao[i] = tempo
                
            except Exception as e:
                self.logger.error(f"❌ Falha na consulta {i}: {e}")
                continue
        
        self.logger.info("✅ Todas as consultas foram executadas!")
    
    def obter_estatisticas_gerais(self) -> Dict[str, int]:
        """Obtém estatísticas gerais do banco de dados"""
        try:
            with self.conexao_bd() as conn:
                cursor = conn.cursor()
                
                tabelas = [
                    'usuario', 'telefone_usuario', 'anfitriao', 'hospede',
                    'politica_cancelamento', 'imovel', 'comodidades', 'reserva',
                    'pagamento', 'parcela', 'servico_extra', 'servicos_vinculados',
                    'avaliacao', 'experiencia_avaliada', 'cancelamento',
                    'reserva_cancelada', 'multa', 'estorno'
                ]
                
                estatisticas = {}
                for tabela in tabelas:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {tabela};")
                        resultado = cursor.fetchone()
                        count = resultado[0] if resultado else 0
                        estatisticas[tabela] = count
                    except:
                        estatisticas[tabela] = 0
                
                return estatisticas
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter estatísticas: {e}")
            return {}
    
    def formatar_resultado_consulta(self, numero: int, df: pd.DataFrame, tempo: float) -> str:
        """Formata resultado de uma consulta para exibição"""
        consulta_info = self.consultas[numero]
        
        separador = "=" * 80
        resultado = f"\n{separador}\n"
        resultado += f"CONSULTA {numero}: {consulta_info['titulo'].upper()}\n"
        resultado += f"{separador}\n"
        resultado += f"Descrição: {consulta_info['descricao']}\n"
        resultado += f"Tempo de execução: {tempo:.3f} segundos\n"
        resultado += f"Registros retornados: {len(df)}\n"
        resultado += f"{'-' * 80}\n"
        
        if len(df) > 0:
            # Configurar pandas para melhor exibição
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', 50)
            
            resultado += df.to_string(index=False)
        else:
            resultado += "⚠️  Nenhum registro encontrado."
        
        resultado += f"\n{'-' * 80}\n"
        return resultado
    
    def gerar_resumo_executivo(self) -> str:
        """Gera resumo executivo dos principais resultados"""
        if not self.resultados_consultas:
            return "⚠️  Nenhum resultado disponível para resumo."
        
        resumo = "\n" + "=" * 80 + "\n"
        resumo += "RESUMO EXECUTIVO - SISTEMA DE LOCAÇÃO DE IMÓVEIS POR TEMPORADA\n"
        resumo += "=" * 80 + "\n"
        
        # Estatísticas gerais
        estatisticas = self.obter_estatisticas_gerais()
        resumo += "\n📊 ESTATÍSTICAS GERAIS DO BANCO:\n"
        resumo += "-" * 40 + "\n"
        
        for tabela, count in estatisticas.items():
            resumo += f"{tabela.replace('_', ' ').title()}: {count:,} registros\n"
        
        # Tempo total de execução
        tempo_total = sum(self.estatisticas_execucao.values())
        resumo += f"\n⏱️  TEMPO TOTAL DE EXECUÇÃO: {tempo_total:.3f} segundos\n"
        
        # Principais insights
        resumo += "\n🎯 PRINCIPAIS INSIGHTS:\n"
        resumo += "-" * 40 + "\n"
        
        try:
            # Imóvel mais rentável (Consulta 9)
            if 9 in self.resultados_consultas and len(self.resultados_consultas[9]) > 0:
                imovel_top = self.resultados_consultas[9].iloc[0]
                resumo += f"💰 Imóvel mais rentável: {imovel_top['titulo']} (R$ {imovel_top['total_recebido']:,.2f})\n"
            
            # Hóspede mais ativo (Consulta 10)
            if 10 in self.resultados_consultas and len(self.resultados_consultas[10]) > 0:
                hospede_top = self.resultados_consultas[10].iloc[0]
                resumo += f"🏆 Hóspede mais ativo: {hospede_top['nome']} ({hospede_top['total_reservas']} reservas)\n"
            
            # Anfitrião com maior receita (Consulta 12)
            if 12 in self.resultados_consultas and len(self.resultados_consultas[12]) > 0:
                anfitriao_top = self.resultados_consultas[12].iloc[0]
                resumo += f"👑 Anfitrião top: {anfitriao_top['anfitriao']} (R$ {anfitriao_top['receita_total']:,.2f})\n"
            
            # Serviço extra mais popular (Consulta 14)
            if 14 in self.resultados_consultas and len(self.resultados_consultas[14]) > 0:
                servico_top = self.resultados_consultas[14].iloc[0]
                resumo += f"🎯 Serviço mais popular: {servico_top['nome']} ({servico_top['vezes_contratado']} contratações)\n"
                
        except Exception as e:
            resumo += f"⚠️  Erro ao gerar insights: {e}\n"
        
        resumo += "\n" + "=" * 80 + "\n"
        return resumo
    
    def salvar_resultados_arquivo(self, nome_arquivo: Optional[str] = None):
        """Salva todos os resultados em arquivo de texto"""
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"resultados_ldi_{timestamp}.txt"
        
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                # Cabeçalho
                arquivo.write("RELATÓRIO COMPLETO - SISTEMA DE LOCAÇÃO DE IMÓVEIS POR TEMPORADA\n")
                arquivo.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                arquivo.write("=" * 80 + "\n")
                
                # Resumo executivo
                arquivo.write(self.gerar_resumo_executivo())
                
                # Resultados detalhados de cada consulta
                for i in range(1, 21):
                    if i in self.resultados_consultas:
                        df = self.resultados_consultas[i]
                        tempo = self.estatisticas_execucao.get(i, 0)
                        resultado_formatado = self.formatar_resultado_consulta(i, df, tempo)
                        arquivo.write(resultado_formatado)
                
            self.logger.info(f"📄 Resultados salvos em: {nome_arquivo}")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar arquivo: {e}")
    
    def salvar_resultados_csv(self):
        """Salva cada consulta em arquivo CSV separado"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for numero, df in self.resultados_consultas.items():
            try:
                nome_arquivo = f"consulta_{numero:02d}_{timestamp}.csv"
                df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
                self.logger.info(f"📊 Consulta {numero} salva em: {nome_arquivo}")
                
            except Exception as e:
                self.logger.error(f"❌ Erro ao salvar CSV da consulta {numero}: {e}")
    
    def exibir_resultados(self):
        """Exibe todos os resultados formatados no console"""
        print("\n" + "🚀 INICIANDO APRESENTAÇÃO DOS RESULTADOS".center(80, "="))
        
        # Resumo executivo primeiro
        print(self.gerar_resumo_executivo())
        
        # Resultados detalhados
        for i in range(1, 21):
            if i in self.resultados_consultas:
                df = self.resultados_consultas[i]
                tempo = self.estatisticas_execucao.get(i, 0)
                resultado_formatado = self.formatar_resultado_consulta(i, df, tempo)
                print(resultado_formatado)
                
                # Pausa entre consultas para melhor leitura
                if i % 5 == 0:
                    input("\nPressione Enter para continuar...")
    
    def executar_processo_completo(self):
        """Executa o processo completo de automação"""
        print("\n" + "🎯 AGENTE DE AUTOMAÇÃO DE BANCO DE DADOS LDI".center(80, "="))
        print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 80)
        
        try:
            # 1. Testar conexão
            print("\n🔍 ETAPA 1: Testando conexão com banco de dados...")
            if not self.testar_conexao():
                raise Exception("Falha na conexão com banco de dados")
            
            # 2. Criar e popular banco
            print("\n🏗️  ETAPA 2: Criando e populando banco de dados...")
            self.executar_criacao_populacional()
            
            # 3. Executar consultas
            print("\n📊 ETAPA 3: Executando consultas analíticas...")
            self.executar_todas_consultas()
            
            # 4. Exibir resultados
            print("\n📋 ETAPA 4: Apresentando resultados...")
            self.exibir_resultados()
            
            # 5. Salvar arquivos
            print("\n💾 ETAPA 5: Salvando resultados em arquivos...")
            self.salvar_resultados_arquivo()
            self.salvar_resultados_csv()
            
            print("\n✅ PROCESSO COMPLETO FINALIZADO COM SUCESSO!")
            print("=" * 80)
            
        except Exception as e:
            self.logger.error(f"❌ ERRO CRÍTICO: {e}")
            print(f"\n❌ PROCESSO INTERROMPIDO: {e}")
            raise


def main():
    """Função principal"""
    print("🤖 AGENTE DE AUTOMAÇÃO DE BANCO DE DADOS - SISTEMA LDI")
    print("=" * 60)
    print("Sistema: Locação de Imóveis por Temporada")
    print("Versão: 1.0")
    print("Data: 19/07/2025")
    print("=" * 60)
    
    # Perguntar se quer recriar tabelas
    resposta = input("\n🔄 Deseja recriar as tabelas? (s/N): ").lower().strip()
    recriar = resposta == 's' or resposta == 'sim'
    
    # Configurar e executar automação
    config = ConfiguradorBD()
    automatizador = AutomatizadorBDLDI(config, recriar_tabelas=recriar)
    
    try:
        automatizador.executar_processo_completo()
        
    except KeyboardInterrupt:
        print("\n⚠️  Processo interrompido pelo usuário.")
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
