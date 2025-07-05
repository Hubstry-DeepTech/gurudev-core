# Script para publicar Alexandria no PyPI
# Autor: Guilherme Gonçalves Machado
# Empresa: Hubstry-DeepTech

Write-Host "🚀 Publicando Alexandria no PyPI..." -ForegroundColor Green
Write-Host "Autor: Guilherme Gonçalves Machado" -ForegroundColor Cyan
Write-Host "Empresa: Hubstry-DeepTech" -ForegroundColor Cyan
Write-Host "=" * 50

# Verificar se está no diretório correto
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "❌ Erro: pyproject.toml não encontrado!" -ForegroundColor Red
    Write-Host "Execute este script na raiz do projeto Alexandria." -ForegroundColor Yellow
    exit 1
}

# Limpar builds anteriores
Write-Host "🧹 Limpando builds anteriores..." -ForegroundColor Yellow
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
if (Test-Path "*.egg-info") {
    Remove-Item -Recurse -Force "*.egg-info"
}

# Instalar dependências de build
Write-Host "📦 Instalando dependências de build..." -ForegroundColor Yellow
pip install --upgrade build twine

# Construir o pacote
Write-Host "🔨 Construindo pacote..." -ForegroundColor Yellow
python -m build

# Verificar se o build foi bem-sucedido
if (-not (Test-Path "dist")) {
    Write-Host "❌ Erro: Build falhou!" -ForegroundColor Red
    exit 1
}

# Verificar o pacote
Write-Host "🔍 Verificando pacote..." -ForegroundColor Yellow
twine check dist/*

# Perguntar se quer publicar
Write-Host ""
Write-Host "⚠️  ATENÇÃO: Você está prestes a publicar no PyPI!" -ForegroundColor Red
Write-Host "Isso tornará a biblioteca Alexandria disponível publicamente." -ForegroundColor Yellow
$confirmation = Read-Host "Deseja continuar? (s/N)"

if ($confirmation -eq "s" -or $confirmation -eq "S") {
    Write-Host "📤 Publicando no PyPI..." -ForegroundColor Green
    
    # Publicar no PyPI
    twine upload dist/*
    
    Write-Host ""
    Write-Host "✅ Alexandria foi publicada com sucesso no PyPI!" -ForegroundColor Green
    Write-Host "📦 Nome do pacote: alexandria-lang" -ForegroundColor Cyan
    Write-Host "🔗 URL: https://pypi.org/project/alexandria-lang/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🎉 Agora os usuários podem instalar com: pip install alexandria-lang" -ForegroundColor Green
}
else {
    Write-Host "❌ Publicação cancelada." -ForegroundColor Yellow
    Write-Host "💡 Para testar localmente, use: pip install dist/alexandria_lang-*.whl" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "📝 Informações de Autoria:" -ForegroundColor Cyan
Write-Host "   Autor: Guilherme Gonçalves Machado" -ForegroundColor White
Write-Host "   Empresa: Hubstry-DeepTech" -ForegroundColor White
Write-Host "   Desenvolvido com auxílio de Claude AI" -ForegroundColor White 