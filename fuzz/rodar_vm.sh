#!/usr/bin/env bash
# fuzz/rodar_vm.sh — Rodada completa numa VM descartável (Ubuntu 24.04).
#
# Etapas: dependências -> baseline -> fuzzing -> triagem -> cobertura -> pacote.
# Travas de segurança:
#   - fuzzing limitado por HORAS (timeout duro = HORAS + 30 min) e pelos critérios
#     de parada do fuzzer (sem novidade por SEM_NOVIDADE_MIN minutos);
#   - desligamento automático da VM em DESLIGAR_UTC (systemd), mesmo que o
#     script trave;
#   - cada programa roda isolado (fork, timeout, limite de memória: ver executor.py);
#   - pacote de resultados sincronizado a cada SYNC_MIN minutos pelo comando em
#     SYNC_CMD (opcional), para nada se perder se a VM cair.
#
# Uso (dentro do repositório, na VM):
#   HORAS=6 DESLIGAR_UTC="2026-10-30 21:00:00" bash fuzz/rodar_vm.sh
# Variáveis opcionais: PROCESSOS (padrão: nproc), SEM_NOVIDADE_MIN (padrão 60),
#   SAIDA (padrão resultados/vm-<data>), SYNC_CMD (recebe o caminho do .tar.gz em $1),
#   SYNC_MIN (padrão 30), SEMENTE (padrão 1).
set -euo pipefail

HORAS="${HORAS:?defina HORAS, ex.: HORAS=6}"
DESLIGAR_UTC="${DESLIGAR_UTC:?defina DESLIGAR_UTC, ex.: 2026-10-30 21:00:00}"
PROCESSOS="${PROCESSOS:-$(nproc)}"
SEM_NOVIDADE_MIN="${SEM_NOVIDADE_MIN:-60}"
SEMENTE="${SEMENTE:-1}"
SAIDA="${SAIDA:-resultados/vm-$(date -u +%Y%m%d-%H%M)}"
SYNC_MIN="${SYNC_MIN:-30}"
SYNC_CMD="${SYNC_CMD:-}"
mkdir -p "$SAIDA"
LOG="$SAIDA/rodada.log"
exec > >(tee -a "$LOG") 2>&1

echo "== $(date -u +%FT%TZ) rodada: HORAS=$HORAS PROCESSOS=$PROCESSOS SAIDA=$SAIDA"

# 1) desligamento automático (independe deste script)
sudo systemd-run --unit=guru-desligar --on-calendar="$DESLIGAR_UTC UTC" /sbin/poweroff || \
  echo "AVISO: timer de desligamento já existia ou falhou; confira com: systemctl list-timers"
systemctl list-timers --all | grep -i guru-desligar || true

# 2) dependências num ambiente virtual (versões fixas)
if [ ! -d .venv-fuzz ]; then
  sudo apt-get update -qq && sudo apt-get install -y -qq python3-venv >/dev/null
  python3 -m venv .venv-fuzz
fi
# shellcheck disable=SC1091
source .venv-fuzz/bin/activate
pip install -q -r fuzz/requirements-fuzz.txt
python -c "import sys; assert sys.version_info >= (3, 12), 'precisa Python 3.12+ (sys.monitoring)'"

# 3) sincronização periódica em segundo plano
empacotar() {
  tar -czf "$SAIDA.tar.gz" -C "$(dirname "$SAIDA")" "$(basename "$SAIDA")" 2>/dev/null || true
  if [ -n "$SYNC_CMD" ]; then bash -c "$SYNC_CMD \"\$1\"" _ "$SAIDA.tar.gz" || echo "AVISO: sincronização falhou"; fi
}
( while sleep $((SYNC_MIN * 60)); do empacotar; done ) &
SYNC_PID=$!
trap 'kill $SYNC_PID 2>/dev/null || true; empacotar' EXIT

# 4) baseline
python fuzz/baseline.py --saida "$SAIDA/baseline"

# 5) fuzzing (timeout duro além do limite interno)
LIMITE_MIN=$((HORAS * 60))
timeout --signal=TERM --kill-after=120 $((LIMITE_MIN + 30))m \
  python fuzz/fuzzer.py --saida "$SAIDA/fuzz" --processos "$PROCESSOS" --semente "$SEMENTE" \
    --max-minutos "$LIMITE_MIN" --parar-sem-novidade-min "$SEM_NOVIDADE_MIN" --intervalo 120 || \
  echo "AVISO: fuzzer terminou com código $?"

# 6) triagem, cobertura e testes
python fuzz/triagem.py --rodada "$SAIDA/fuzz" --saida "$SAIDA/triagem"
python fuzz/cobertura.py --rodada "$SAIDA/fuzz" --baseline "$SAIDA/baseline" --saida "$SAIDA/cobertura" --processos "$PROCESSOS"

echo "== $(date -u +%FT%TZ) concluído. Pacote: $SAIDA.tar.gz"
