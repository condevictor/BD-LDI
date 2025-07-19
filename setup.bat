@echo off
REM Script de configuração do Agente de Automação BD-LDI
REM Windows PowerShell

echo ================================
echo AGENTE DE AUTOMACAO BD-LDI
echo Sistema de Locacao de Imoveis
echo ================================

echo.
echo [1/4] Verificando Python...
python --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado. Instale Python 3.8+ antes de continuar.
    pause
    exit /b 1
)

echo.
echo [2/4] Instalando dependencias Python...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: Falha na instalacao das dependencias.
    pause
    exit /b 1
)

echo.
echo [3/4] Verificando Docker (PostgreSQL)...
docker ps >nul 2>&1
if errorlevel 1 (
    echo AVISO: Docker nao encontrado ou nao iniciado.
    echo Execute 'docker-compose up -d' no diretorio SQL antes de executar o script.
) else (
    echo Docker OK - Verificando container PostgreSQL...
    docker ps | findstr "LDI-postgres" >nul
    if errorlevel 1 (
        echo Container PostgreSQL nao encontrado.
        echo Navegando para diretorio SQL e iniciando container...
        cd SQL
        docker-compose up -d
        cd ..
    ) else (
        echo Container PostgreSQL ja esta em execucao.
    )
)

echo.
echo [4/4] Configuracao concluida!
echo.
echo Para executar o sistema:
echo    python automatizador_bd_ldi.py
echo.
echo Para parar os containers:
echo    cd SQL
echo    docker-compose down
echo.
pause
