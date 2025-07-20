# 🏠 Sistema de Locação de Imóveis - BD-LDI

Sistema de demonstração acadêmica com banco PostgreSQL e 21 consultas organizadas por categoria.

## 🚀 Como Executar

### ⚡ Opção 1: Interface Web (Streamlit)
```bash
# 1. Instalar dependências
pip install -r requirements.txt
pip install streamlit psycopg2 pandas plotly configparser # Caso o comando acima não consiga ser executado

# 2. Executar aplicação web
streamlit run src/app_streamlit.py --browser.gatherUsageStats=false
```
**Acesse:** http://localhost:8501

### 💻 Opção 2: Terminal Python
```bash
# 1. Instalar dependências
pip install psycopg2 configparser

# 2. Executar no terminal
python src/apresentacao_ldi.py
```

## ⚙️ Configuração do Banco

Edite o arquivo `config.ini`:
```ini
[DATABASE]
HOST = localhost
PORT = 5432
DATABASE = ldi
USER = ldi
PASSWORD = ldi123
```

## 📁 Estrutura do Projeto

```
BD-LDI/
├── 📄 README.md           # Este arquivo
├── ⚙️ config.ini          # Configuração do banco
├── 📋 requirements.txt    # Dependências Python
├── 🗂️ src/               # Código fonte
│   ├── app_streamlit.py   # Interface web
│   └── apresentacao_ldi.py # Interface terminal
├── 🗂️ SQL/               # Scripts do banco
│   ├── v2-ldi.sql         # Schema completo
│   └── docker-compose.yaml # Docker PostgreSQL
├── 🗂️ scripts/           # Scripts auxiliares
│   └── executar_streamlit.py # Inicializador
└── 🗂️ docs/              # Documentação
    ├── GUIA_APRESENTACAO.md
    └── STREAMLIT_README.md
```

## 🎯 Funcionalidades

- **21 Consultas SQL** organizadas em 6 categorias
- **Interface Web** moderna com Streamlit
- **Interface Terminal** para demonstrações
- **Visualizações** com gráficos interativos
- **Export CSV** dos resultados
- **PostgreSQL** como banco de dados

## 📊 Categorias de Consultas

1. **📋 Operacionais** - Gestão diária
2. **👥 Usuários e Perfis** - Gerenciamento de users
3. **💰 Financeiras** - Relatórios de receita
4. **📈 Business Intelligence** - KPIs e métricas
5. **👔 Executivas** - Visão estratégica
6. **🏢 Administrativas** - Controles internos

---
🎓 **Projeto Acadêmico** - Sistema de Banco de Dados PostgreSQL
