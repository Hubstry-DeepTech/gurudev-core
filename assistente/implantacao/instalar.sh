#!/usr/bin/env bash
# Instala o Assistente GuruDev numa maquina Ubuntu (ex.: Magalu Cloud BV8-32-40).
#
# Uso (na maquina, como root):
#   bash instalar.sh [modelo]          # padrao: qwen3:1.7b
#
# O que faz:
#   - cria o usuario de servico "guru", sem privilegios e sem login;
#   - instala o Ollama (servidor local de modelos, ouvindo so em 127.0.0.1);
#   - baixa o modelo escolhido;
#   - clona ou atualiza o gurudev-core em /opt/gurudev-core;
#   - cria o servico assistente-gurudev (porta 8000), com restricoes do systemd.
set -euo pipefail

MODELO="${1:-qwen3:1.7b}"
DESTINO=/opt/gurudev-core
REPO=https://github.com/Hubstry-DeepTech/gurudev-core

if [ "$(id -u)" -ne 0 ]; then
  echo "Rode como root: sudo bash instalar.sh [modelo]" >&2
  exit 1
fi

echo ">> Pacotes do sistema"
apt-get update -y
apt-get install -y git python3 python3-venv curl

echo ">> Usuario de servico"
id guru >/dev/null 2>&1 || useradd --system --create-home --shell /usr/sbin/nologin guru

echo ">> Ollama"
command -v ollama >/dev/null 2>&1 || curl -fsSL https://ollama.com/install.sh | sh
systemctl enable --now ollama
echo ">> Baixando o modelo $MODELO (pode levar alguns minutos)"
ollama pull "$MODELO"

echo ">> Codigo do gurudev-core"
if [ -d "$DESTINO/.git" ]; then
  git -C "$DESTINO" pull --ff-only
else
  git clone --depth 1 "$REPO" "$DESTINO"
fi
python3 -m venv "$DESTINO/.venv"
"$DESTINO/.venv/bin/pip" install -q -e "$DESTINO"
chown -R root:root "$DESTINO"   # o servico apenas le o codigo

echo ">> Servico assistente-gurudev"
cat > /etc/systemd/system/assistente-gurudev.service <<EOF
[Unit]
Description=Assistente GuruDev
After=network-online.target ollama.service
Wants=ollama.service

[Service]
User=guru
WorkingDirectory=$DESTINO
Environment=GURU_MODELO_URL=http://127.0.0.1:11434/v1
Environment=GURU_MODELO_NOME=$MODELO
Environment=GURU_SEM_RACIOCINIO=1
Environment=GURU_HOST=0.0.0.0
Environment=GURU_PORTA=8000
Environment=PYTHONDONTWRITEBYTECODE=1
ExecStart=$DESTINO/.venv/bin/python -m assistente.servidor
Restart=on-failure
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
IPAddressDeny=169.254.169.254/32

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now assistente-gurudev
systemctl restart assistente-gurudev

sleep 3
if curl -fsS http://127.0.0.1:8000/saude >/dev/null; then
  echo ">> Pronto: Assistente GuruDev no ar na porta 8000 (modelo $MODELO)"
else
  echo ">> O servico nao respondeu. Veja: journalctl -u assistente-gurudev -n 50" >&2
  exit 1
fi
