# Script para automatizar git add, commit e push
Write-Host "🔄 Adicionando arquivos..." -ForegroundColor Green
git add .

Write-Host "💾 Fazendo commit..." -ForegroundColor Green
git commit -m "Atualização automática: adiciona e atualiza arquivos"

Write-Host "📤 Enviando para o repositório remoto..." -ForegroundColor Green
git push

Write-Host "✅ Concluído!" -ForegroundColor Green 