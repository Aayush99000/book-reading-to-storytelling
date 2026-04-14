#!/bin/bash
# ── One-time environment setup on Northeastern Explorer HPC ───────────────────
# Run once after cloning the repo:
#   bash setup_env.sh

set -e

ENV_NAME="book2comic"

echo "==> Loading anaconda module..."
module load anaconda3/2022.05

echo "==> Creating conda environment: $ENV_NAME (Python 3.10)..."
conda create -y -n $ENV_NAME python=3.10

echo "==> Activating environment..."
source activate $ENV_NAME

echo "==> Installing PyTorch with CUDA 11.8..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

echo "==> Installing project dependencies..."
pip install -r requirements.txt

echo "==> Creating .env file (fill in your keys)..."
if [ ! -f backend/.env ]; then
    cat > backend/.env <<EOF
GROQ_API_KEY=your_groq_api_key_here
MANGA_LORA_ID=
HF_HOME=/scratch/$USER/hf_cache
EOF
    echo "    Created backend/.env — add your GROQ_API_KEY"
else
    echo "    backend/.env already exists, skipping"
fi

echo "==> Setting HuggingFace cache to scratch (avoids home quota)..."
mkdir -p /scratch/$USER/hf_cache

echo ""
echo "Setup complete. Next steps:"
echo "  1. Edit backend/.env and add your GROQ_API_KEY"
echo "  2. Submit a job:  sbatch slurm_job.sh"
echo "  3. Or run interactively: srun --partition=gpu --gres=gpu:1 --mem=32G --time=02:00:00 --pty bash"
