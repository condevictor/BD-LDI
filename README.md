# Sistema de Locação de Imóveis - BD-LDI

Sistema de banco de dados PostgreSQL com 21 consultas SQL para gerenciamento de locação de imóveis.

## 🚀 Como Executar

### Opção 1: Usando requirements (Recomendado)
```bash
# Instalar dependências
pip install -r requirements_clean.txt

# Iniciar PostgreSQL  
docker-compose up -d

# Executar sistema
cd src
python apresentacao_clean.py
```

### Opção 2: Instalação manual - Terminal apenas
```bash
# Dependências mínimas para terminal
pip install psycopg2-binary

# Iniciar PostgreSQL
docker-compose up -d

# Executar sistema
cd src
python apresentacao_clean.py
```

### Opção 3: Com Streamlit (Interface Web)
```bash
# Dependências completas
pip install psycopg2-binary streamlit pandas plotly

# Iniciar PostgreSQL
docker-compose up -d

# Executar interface web
cd scripts
python executar_streamlit.py
```

### Opção 4: Apenas arquivos essenciais (PDF/Entrega)
```bash
# Se você tem apenas: apresentacao_ldi.py, database.py e v2-ldi.sql

# 1. Instalar dependência
pip install psycopg2-binary

# 2. Configurar caminhos nos arquivos Python:
#    - Em database.py linha ~22: altere para o caminho do seu .env
#    - Em apresentacao_ldi.py linha ~49: altere para o caminho do seu v2-ldi.sql
#    - Em apresentacao_ldi.py linha ~89: altere para o caminho do seu v2-ldi.sql

# 3. Criar .env com suas credenciais PostgreSQL

# 4. Executar
python apresentacao_ldi.py
```

## ⚙️ Configuração

Arquivo `.env`:
```env
POSTGRES_PASSWORD=ldi123
POSTGRES_USER=ldi
POSTGRES_DB=ldi

PGADMIN_DEFAULT_EMAIL=ldi@gmail.com
PGADMIN_DEFAULT_PASSWORD=ldi123

DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=ldi
DB_USER=ldi
DB_PASSWORD=ldi123
```

## 📁 Arquivos Principais

```
BD-LDI/
├── .env                      # Configurações
├── requirements.txt    # Dependências  
├── src/
│   ├── database.py    # Conexão com banco
│   └── apresentacao_ldi.py # Sistema principal
└── SQL/v2-ldi.sql           # Schema e dados
```

## 🗄️ Consultas Implementadas

**21 consultas organizadas em 6 categorias:**
1. **Operacionais** - Gestão diária (3 consultas)
2. **Usuários** - Perfis e cadastros (4 consultas)  
3. **Financeiras** - Pagamentos e receitas (4 consultas)
4. **Business Intelligence** - Métricas e KPIs (4 consultas)
5. **Executivas** - Visão estratégica (3 consultas)
6. **Administrativas** - Controles internos (3 consultas)

## 🔧 Solução de Problemas

**Erro de conexão:** `docker-compose up -d`  
**Usuário não existe:** Aguarde container inicializar completamente  
**Porta ocupada:** Altere DB_PORT em .env

---
**Projeto Acadêmico** - Demonstração PostgreSQL
