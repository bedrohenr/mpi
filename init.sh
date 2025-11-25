#!/bin/bash

# Interrompe o script se houver erro
set -e

echo "--- 🚀 Iniciando Instalação do Ambiente MPI ---"

# 1. Atualizar repositórios e sistema
echo "[1/5] Atualizando repositórios..."
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependências do sistema (OpenMPI, SSH, Compiladores, Python dev)
echo "[2/5] Instalando OpenMPI, SSH e ferramentas de desenvolvimento..."
sudo apt install -y build-essential python3-dev python3-pip openmpi-bin libopenmpi-dev openssh-server

# 3. Instalar mpi4py
# No Ubuntu 24.04, é mais seguro instalar via APT para evitar conflitos de ambiente (PEP 668)
echo "[3/5] Instalando biblioteca mpi4py..."
sudo apt install -y python3-mpi4py

# Se preferir instalar via PIP (versão mais recente), descomente a linha abaixo:
# pip3 install mpi4py --break-system-packages

# 4. Configuração do SSH (Geração de Chaves)
echo "[4/5] Configurando SSH..."

# Verifica se a chave já existe, se não, cria uma nova sem senha (-N "")
if [ ! -f ~/.ssh/id_rsa ]; then
    echo "Gerando par de chaves SSH..."
    ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
else
    echo "Chaves SSH já existem. Pulando geração."
fi

# Adiciona a própria chave ao authorized_keys (permite rodar mpirun localmente sem senha)
if ! grep -q "$(cat ~/.ssh/id_rsa.pub)" ~/.ssh/authorized_keys; then
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    chmod 600 ~/.ssh/authorized_keys
    echo "Chave autorizada para localhost."
fi

# Garante que o serviço SSH está rodando
sudo systemctl enable ssh
sudo systemctl start ssh

# 5. Verificação
echo "[5/5] Verificando instalação..."
echo "------------------------------------------------"
echo "Versão do MPI:"
mpirun --version | head -n 1
echo "------------------------------------------------"
echo "Teste rápido do mpi4py:"
python3 testando.py
echo "------------------------------------------------"

echo "✅ Instalação Concluída!"
echo ""
echo "⚠️  PRÓXIMOS PASSOS PARA CLUSTER (Várias Máquinas):"
echo "1. Execute este script em TODAS as máquinas (VMs)."
echo "2. Copie a chave desta máquina para as outras:"
echo "   ssh-copy-id usuario@IP_DA_OUTRA_MAQUINA"
echo "3. Crie um arquivo 'hosts' com os IPs das máquinas."
echo "4. Como você está na faculdade, use o IP da rede Host-Only (192.168.56.x)!"
echo ""