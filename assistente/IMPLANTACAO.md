# Implantação do Assistente GuruDev na Magalu Cloud

Roteiro para colocar o Assistente V0 no ar numa máquina da Magalu Cloud. Tempo estimado: 30 a 45 minutos, sendo a maior parte download do modelo.

## Custo

Máquina BV8-32-40 (8 processadores, 32 GB de memória, 40 GB de disco): cerca de R$ 0,68 por hora, ou R$ 16 por dia ligada (tabela oficial da Magalu Cloud, vigente em outubro de 2026). Regra: **ligar para trabalhar ou demonstrar, desligar depois.**

## 1. Criar a máquina (console da Magalu Cloud)

- Tipo: **BV8-32-40**
- Imagem: **Ubuntu 24.04**
- Região: br-se1 (Sudeste)
- Acesso: sua chave SSH pública
- IP público: sim

## 2. Liberar o acesso (grupo de segurança)

- Porta **22** (SSH): somente o seu IP.
- Porta **8000** (Assistente): liberar apenas durante demonstrações.

## 3. Instalar (no PowerShell do seu computador)

Entre na máquina (o usuário padrão aparece no console; normalmente `ubuntu`):

```powershell
ssh ubuntu@IP_DA_MAQUINA
```

Já dentro da máquina, rode:

```bash
curl -fsSL https://raw.githubusercontent.com/Hubstry-DeepTech/gurudev-core/main/assistente/implantacao/instalar.sh -o instalar.sh
sudo bash instalar.sh qwen3:1.7b
```

Ao final deve aparecer: `Pronto: Assistente GuruDev no ar na porta 8000`.

## 4. Testar

- No navegador: `http://IP_DA_MAQUINA:8000`
- Medição dos 8 roteiros, dentro da máquina:

```bash
cd /opt/gurudev-core && .venv/bin/python -m assistente.medir
```

A medição V0 registra o tempo **total** de cada resposta (o servidor ainda não envia a resposta em partes); é um critério mais rigoroso que o SLO de primeira resposta em até 8 s.

## 5. Trocar de modelo (se o 1.7B gerar código ruim)

```bash
sudo bash instalar.sh qwen3:4b
```

## 6. Desligar

Pelo console da Magalu Cloud, desligue a máquina ao terminar. Confira no console o que continua sendo cobrado com a máquina desligada (disco e IP público podem ter cobrança própria).

## Segurança aplicada

- O serviço roda com o usuário `guru`, sem privilégios e sem login.
- O código do repositório fica somente leitura para o serviço.
- O modelo (Ollama) ouve apenas em 127.0.0.1, sem exposição externa.
- O acesso ao serviço de metadados da nuvem (169.254.169.254) é bloqueado para o serviço.
- Políticas POL-01 a POL-03 (`assistente/politica.py`): subescritas nunca executam; limites de tempo, tamanho e pedidos por minuto.
- O registro do servidor não guarda o conteúdo das perguntas.
