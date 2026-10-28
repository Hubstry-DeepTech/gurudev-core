#!/usr/bin/env bash
# evidence_gate/iniciar_vm.sh — sobe o Evidence Gate na VM, so em 127.0.0.1.
# A chave vem do Secret Manager a cada inicio; nunca fica em arquivo.
# Uso (dentro do repositorio, na VM):
#   bash evidence_gate/iniciar_vm.sh          # sobe o servidor
#   bash evidence_gate/iniciar_vm.sh --demo   # sobe e roda os 3 casos reais
set -euo pipefail
export GURU_MODELO_URL="${GURU_MODELO_URL:-https://ldgllm.digiti.net.br/v1}"
export GURU_MODELO_NOME="${GURU_MODELO_NOME:-glm-5.3}"
export GURU_MODELO_TEMPO="${GURU_MODELO_TEMPO:-300}"
export GURU_MODELO_MAX_TOKENS="${GURU_MODELO_MAX_TOKENS:-8000}"
export GURU_HOST=127.0.0.1
export GURU_PORTA="${GURU_PORTA:-8080}"
GURU_MODELO_API_KEY="$(gcloud secrets versions access latest \
  --secret=digiti-maas-api-key)"
export GURU_MODELO_API_KEY

# Ubuntu 24.04 (PEP 668): instala so para o usuario, sem tocar no sistema
python3 -c "import ply" 2>/dev/null \
  || pip install --user -q --break-system-packages ply

PIDFILE="$HOME/evidence_gate.pid"
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  kill "$(cat "$PIDFILE")"
  sleep 1
fi
nohup python3 -m evidence_gate.servidor > "$HOME/evidence_gate.log" 2>&1 &
echo $! > "$PIDFILE"
sleep 2
curl -fsS "http://127.0.0.1:$GURU_PORTA/saude" && echo " <- servidor no ar"
echo "Registro: $HOME/evidence_gate.log"

# a demo herda as mesmas variaveis (inclusive a chave) deste processo
if [ "${1:-}" = "--demo" ]; then
  python3 -m evidence_gate.demo
fi
