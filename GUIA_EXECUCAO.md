🚀 GUIA DE INSTALAÇÃO E EXECUÇÃO - BD-LDI
==========================================

## 📋 PASSO A PASSO PARA EXECUÇÃO

### 1️⃣ INSTALAÇÃO DAS DEPENDÊNCIAS

```powershell
# Instalar dependências Python
pip install psycopg2-binary pandas numpy

# OU usar o arquivo requirements.txt
pip install -r requirements.txt
```

### 2️⃣ CONFIGURAÇÃO DO BANCO DE DADOS

```powershell
# Navegar para o diretório SQL
cd SQL

# Iniciar container PostgreSQL
docker-compose up -d

# Verificar se está rodando
docker ps
```

### 3️⃣ EXECUÇÃO

#### Opção A: Script Principal (Completo)
```powershell
python automatizador_bd_ldi.py
```

#### Opção B: Teste Rápido
```powershell
python teste_rapido.py
```

#### Opção C: Configuração Automática
```powershell
# Windows (Batch)
setup.bat

# Windows (PowerShell)
.\setup.ps1
```

### 4️⃣ VERIFICAÇÃO DE PROBLEMAS

#### Se der erro de importação:
```
ModuleNotFoundError: No module named 'psycopg2'
```
**Solução:**
```powershell
pip install psycopg2-binary
```

#### Se der erro de conexão:
```
could not connect to server
```
**Solução:**
```powershell
cd SQL
docker-compose up -d
# Aguardar alguns segundos e tentar novamente
```

#### Se der erro de encoding:
```
UnicodeDecodeError
```
**Solução:** O script já está configurado para UTF-8, mas verifique se o arquivo SQL está salvo em UTF-8.

### 5️⃣ ESTRUTURA DE ARQUIVOS GERADOS

Após a execução, serão criados:

```
📁 BD-LDI/
├── 📄 resultados_ldi_YYYYMMDD_HHMMSS.txt    # Relatório completo
├── 📊 consulta_01_YYYYMMDD_HHMMSS.csv       # Consulta 1 em CSV
├── 📊 consulta_02_YYYYMMDD_HHMMSS.csv       # Consulta 2 em CSV
├── ...                                      # (20 arquivos CSV)
└── 📝 ldi_automation.log                    # Log de execução
```

### 6️⃣ FUNCIONALIDADES DO SCRIPT

✅ **Automação Completa:**
- Criação/recriação de tabelas
- População com dados de teste
- Execução de 20 consultas analíticas
- Relatórios formatados

✅ **Saídas Profissionais:**
- Console interativo com cores
- Relatório TXT consolidado
- Arquivos CSV individuais
- Log detalhado de execução

✅ **Tratamento de Erros:**
- Verificação de conexão
- Rollback automático
- Logs de erro detalhados
- Encoding UTF-8

### 7️⃣ EXEMPLOS DE USO

#### Execução Padrão (Recriar tudo):
```powershell
python automatizador_bd_ldi.py
# Responder 's' para recriar tabelas
```

#### Execução Apenas com Consultas:
```powershell
python automatizador_bd_ldi.py
# Responder 'n' para manter dados existentes
```

#### Verificação Rápida:
```powershell
python teste_rapido.py
```

### 8️⃣ MONITORAMENTO

#### Ver logs em tempo real:
```powershell
Get-Content ldi_automation.log -Wait
```

#### Verificar containers Docker:
```powershell
docker ps
docker logs LDI-postgres
```

#### Acessar PgAdmin (Interface Web):
```
URL: http://localhost:8080
Email: ldi@gmail.com
Senha: ldi123
```

### 9️⃣ DICAS DE PERFORMANCE

- **Primeira execução:** Pode demorar mais devido ao download da imagem Docker
- **Execuções seguintes:** Muito mais rápidas (~2-3 segundos)
- **Dados grandes:** Use LIMIT nas consultas se necessário
- **Memória:** Container PostgreSQL usa ~100MB RAM

### 🔟 TROUBLESHOOTING AVANÇADO

#### Resetar completamente:
```powershell
# Parar containers
cd SQL
docker-compose down

# Remover volumes (CUIDADO: apaga dados)
docker-compose down -v

# Recriar tudo
docker-compose up -d
```

#### Verificar conectividade:
```powershell
# Testar conexão direta
python -c "import psycopg2; print('✅ psycopg2 OK')"

# Testar pandas
python -c "import pandas; print('✅ pandas OK')"
```

#### Logs detalhados:
```powershell
# Ver log completo
type ldi_automation.log

# Ver apenas erros
findstr "ERROR" ldi_automation.log
```

---

**🎯 DICA:** Execute primeiro `python teste_rapido.py` para verificar se tudo está funcionando antes de rodar o script principal completo.

**📞 SUPORTE:** Consulte o arquivo `README_AUTOMATIZADOR.md` para documentação detalhada.
