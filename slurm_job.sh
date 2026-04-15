#!/bin/bash
#SBATCH --job-name=book2comic
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:1
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4
#SBATCH --time=04:00:00
#SBATCH --output=logs/book2comic_%j.out
#SBATCH --error=logs/book2comic_%j.err

# ── Load modules ──────────────────────────────────────────────────────────────
module load anaconda3/2022.05
module load cuda/11.8

# ── Activate environment ───────────────────────────────────────────────────────
source $(conda info --base)/etc/profile.d/conda.sh
conda activate book2comic

# ── Set HuggingFace cache to scratch (avoids home directory quota) ─────────────
export HF_HOME=/scratch/$USER/hf_cache
export TRANSFORMERS_CACHE=/scratch/$USER/hf_cache

# ── Move to project directory ──────────────────────────────────────────────────
cd $SLURM_SUBMIT_DIR

mkdir -p logs output/images

# ── Start FastAPI server ───────────────────────────────────────────────────────
echo "Starting Book2Comic API on $(hostname)..."
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
