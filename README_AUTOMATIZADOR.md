# 🏠 Agente de Automação BD-LDI
## Sistema de Locação de Imóveis por Temporada

### 📋 Descrição
Este é um **Agente de Automação de Banco de Dados** especializado em PostgreSQL que automatiza completamente a execução e apresentação dos resultados do sistema de locação de imóveis por temporada (LDI).

### ✨ Funcionalidades

#### 🔧 Automação Completa
- ✅ Conexão automática com PostgreSQL
- ✅ Criação e população de todas as tabelas
- ✅ Execução sequencial de 20 consultas analíticas
- ✅ Formatação profissional dos resultados
- ✅ Geração de relatórios e estatísticas

#### 📊 Relatórios Incluídos
1. **Imóveis com Wi-Fi disponíveis** - Disponibilidade por período
2. **Reservas por hóspede** - Histórico individual
3. **Imóveis bem avaliados** - Média de notas > 4
4. **Pagamentos completos** - Principais + multas
5. **Serviços extras** - Contratações por hóspede
6. **Ranking de comodidades** - Imóveis mais equipados
7. **Multas aplicadas** - Cancelamentos com penalidade
8. **Parcelas futuras** - Controle financeiro
9. **Receita por imóvel** - Performance financeira
10. **Hóspedes ativos** - Ranking de reservas
11. **Disponibilidade específica** - Períodos livres
12. **Receita por anfitrião** - Performance dos proprietários
13. **Cancelamentos por política** - Análise de políticas
14. **Serviços populares** - Demanda por extras
15. **Parcelas em atraso** - Inadimplência
16. **Disponibilidade por filtros** - Capacidade + localização
17. **Histórico completo** - Timeline de imóvel específico
18. **Receita mensal** - Análise temporal
19. **Estornos por política** - Impacto financeiro
20. **Ocupação geral** - Estatísticas de utilização

#### 💾 Formatos de Saída
- **Console interativo** - Visualização em tempo real
- **Arquivo TXT completo** - Relatório único consolidado
- **Arquivos CSV individuais** - Uma planilha por consulta
- **Log de execução** - Histórico detalhado

### 🚀 Instalação e Configuração

#### 📋 Pré-requisitos
- Python 3.8 ou superior
- Docker e Docker Compose
- PostgreSQL (via container)

#### ⚡ Configuração Rápida

1. **Execute o script de configuração:**
   ```bash
   setup.bat
   ```

2. **Ou configure manualmente:**
   ```bash
   # Instalar dependências
   pip install -r requirements.txt
   
   # Iniciar banco PostgreSQL
   cd SQL
   docker-compose up -d
   cd ..
   ```

#### 🔧 Configurações do Banco
- **Host:** localhost
- **Porta:** 5432
- **Database:** ldi
- **Usuário:** ldi
- **Senha:** ldi123

### 🎯 Execução

#### 🖥️ Modo Interativo
```bash
python automatizador_bd_ldi.py
```

O sistema oferece as seguintes opções:
- **Recriar tabelas:** Remove dados existentes e recria tudo
- **Manter dados:** Usa dados existentes e executa apenas consultas

#### 📊 Exemplo de Saída

```
🎯 AGENTE DE AUTOMAÇÃO DE BANCO DE DADOS LDI
================================================================================
Iniciado em: 19/07/2025 14:30:45
================================================================================

🔍 ETAPA 1: Testando conexão com banco de dados...
✅ Conexão com banco de dados estabelecida
📊 PostgreSQL Version: PostgreSQL 16.3

🏗️  ETAPA 2: Criando e populando banco de dados...
📁 Script SQL carregado: c:\...\SQL\v2-ldi.sql
🗑️  Removendo tabelas existentes...
📝 Executando script de criação e população...
✅ Banco de dados criado e populado com sucesso!

📊 ETAPA 3: Executando consultas analíticas...
📊 Executando Consulta 1: Imóveis com Wi-Fi disponíveis entre datas específicas
✅ Consulta 1 executada em 0.045s
...

📋 ETAPA 4: Apresentando resultados...
================================================================================
CONSULTA 1: IMÓVEIS COM WI-FI DISPONÍVEIS ENTRE DATAS ESPECÍFICAS
================================================================================
Descrição: Lista imóveis que possuem Wi-Fi e estão disponíveis no período de 05/08 a 10/08/2025
Tempo de execução: 0.045 segundos
Registros retornados: 3
--------------------------------------------------------------------------------
id_imovel    titulo         capacidade_max    cidade    valor_diaria
1           Casa da Praia          6         Rio de Janeiro   350.00
2           Apartamento Centro     4         São Paulo        200.00
3           Chalé Montanha         8         Campos do Jordão 450.00
```

### 📈 Resumo Executivo

O sistema gera automaticamente um resumo executivo com:

```
📊 ESTATÍSTICAS GERAIS DO BANCO:
Usuario: 10 registros
Imovel: 5 registros
Reserva: 8 registros
Pagamento: 12 registros
...

⏱️  TEMPO TOTAL DE EXECUÇÃO: 2.347 segundos

🎯 PRINCIPAIS INSIGHTS:
💰 Imóvel mais rentável: Casa da Praia (R$ 2.100,00)
🏆 Hóspede mais ativo: Ana Souza (3 reservas)
👑 Anfitrião top: João Silva (R$ 3.500,00)
🎯 Serviço mais popular: Café da manhã (5 contratações)
```

### 📁 Arquivos Gerados

#### 📄 Relatório Completo
- `resultados_ldi_20250719_143045.txt` - Relatório consolidado

#### 📊 Planilhas CSV
- `consulta_01_20250719_143045.csv` - Imóveis com Wi-Fi
- `consulta_02_20250719_143045.csv` - Reservas por hóspede
- ... (20 arquivos no total)

#### 📝 Log de Execução
- `ldi_automation.log` - Log detalhado do processo

### 🛠️ Estrutura Técnica

#### 🏗️ Arquitetura
```python
AutomatizadorBDLDI
├── ConfiguradorBD          # Configurações de conexão
├── conexao_bd()           # Context manager para BD
├── executar_criacao_populacional()  # Setup inicial
├── executar_todas_consultas()      # Execução das 20 consultas
├── gerar_resumo_executivo()        # Análise consolidada
└── salvar_resultados_arquivo()     # Persistência de dados
```

#### 🔒 Tratamento de Erros
- **Conexão BD:** Validação e retry automático
- **Execução SQL:** Rollback em caso de falha
- **Encoding:** UTF-8 para caracteres especiais
- **Logging:** Rastreamento completo de execução

#### ⚡ Performance
- **Conexões otimizadas:** Context managers
- **Pandas integration:** Formatação eficiente
- **Execução sequencial:** Controle de recursos
- **Medição de tempo:** Profiling automático

### 🎛️ Customização

#### 🔧 Configurações de Conexão
Edite a classe `ConfiguradorBD` para alterar parâmetros:

```python
def __init__(self):
    self.host = "localhost"      # Endereço do servidor
    self.port = 5432            # Porta PostgreSQL
    self.database = "ldi"       # Nome do banco
    self.user = "ldi"           # Usuário
    self.password = "ldi123"    # Senha
```

#### 📊 Novas Consultas
Adicione consultas na função `_definir_consultas()`:

```python
21: {
    "titulo": "Nova Análise",
    "descricao": "Descrição da nova consulta",
    "sql": "SELECT ... FROM ..."
}
```

### 🔍 Troubleshooting

#### ❌ Erro de Conexão
```
❌ Erro na conexão: could not connect to server
```
**Solução:** Verifique se o Docker está rodando:
```bash
cd SQL
docker-compose up -d
```

#### ❌ Erro de Encoding
```
❌ Erro ao carregar SQL: 'charmap' codec can't decode
```
**Solução:** O script já usa UTF-8. Verifique se o arquivo SQL está em UTF-8.

#### ❌ Falta de Dependências
```
❌ No module named 'psycopg2'
```
**Solução:** Execute a instalação:
```bash
pip install -r requirements.txt
```

### 📞 Suporte

Para problemas ou melhorias:
1. Verifique os logs em `ldi_automation.log`
2. Execute `setup.bat` para reconfiguração
3. Consulte a documentação técnica no código

### 📄 Licença

Sistema desenvolvido para automação educacional de banco de dados PostgreSQL.

---

**🚀 Agente de Automação BD-LDI v1.0** - Sistema profissional para análise automatizada de dados de locação de imóveis por temporada.
