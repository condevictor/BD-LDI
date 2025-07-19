# Script de Configuração PowerShell - BD-LDI
# Agente de Automação de Banco de Dados
# =====================================

Write-Host "================================" -ForegroundColor Cyan
Write-Host "AGENTE DE AUTOMACAO BD-LDI" -ForegroundColor Yellow
Write-Host "Sistema de Locacao de Imoveis" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "[1/4] Verificando Python..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERRO: Python não encontrado. Instale Python 3.8+ antes de continuar." -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""
Write-Host "[2/4] Instalando dependências Python..." -ForegroundColor Green
try {
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependências instaladas com sucesso!" -ForegroundColor Green
    } else {
        throw "Falha na instalação"
    }
} catch {
    Write-Host "❌ ERRO: Falha na instalação das dependências." -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""
Write-Host "[3/4] Verificando Docker..." -ForegroundColor Green
try {
    docker ps | Out-Null
    Write-Host "✅ Docker está rodando" -ForegroundColor Green
    
    # Verificar se o container PostgreSQL está rodando
    $postgresContainer = docker ps --filter "name=LDI-postgres" --format "table {{.Names}}"
    if ($postgresContainer -match "LDI-postgres") {
        Write-Host "✅ Container PostgreSQL já está em execução" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Container PostgreSQL não encontrado. Iniciando..." -ForegroundColor Yellow
        Set-Location SQL
        docker-compose up -d
        Set-Location ..
        Write-Host "✅ Container PostgreSQL iniciado" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  AVISO: Docker não encontrado ou não iniciado." -ForegroundColor Yellow
    Write-Host "Execute 'docker-compose up -d' no diretório SQL antes de executar o script." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[4/4] Configuração concluída!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Para executar o sistema completo:" -ForegroundColor Cyan
Write-Host "   python automatizador_bd_ldi.py" -ForegroundColor White
Write-Host ""
Write-Host "🔍 Para teste rápido:" -ForegroundColor Cyan
Write-Host "   python teste_rapido.py" -ForegroundColor White
Write-Host ""
Write-Host "🛑 Para parar os containers:" -ForegroundColor Cyan
Write-Host "   cd SQL; docker-compose down" -ForegroundColor White
Write-Host ""

# Perguntar se quer executar o sistema agora
$resposta = Read-Host "Deseja executar o sistema agora? (s/N)"
if ($resposta -eq "s" -or $resposta -eq "S" -or $resposta -eq "sim") {
    Write-Host ""
    Write-Host "🚀 Iniciando sistema..." -ForegroundColor Green
    python automatizador_bd_ldi.py
} else {
    Write-Host "✅ Configuração finalizada. Execute quando necessário!" -ForegroundColor Green
}

Read-Host "Pressione Enter para finalizar"
