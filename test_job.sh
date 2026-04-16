#!/bin/bash
#SBATCH --job-name=book2comic-test
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:1
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/katoch.aa/book2comic/logs/test_%j.out
#SBATCH --error=/scratch/katoch.aa/book2comic/logs/test_%j.err

mkdir -p /scratch/katoch.aa/book2comic/logs

module load anaconda3/2024.06
module load cuda/11.8

source $(conda info --base)/etc/profile.d/conda.sh
conda activate book2comic

export HF_HOME=/scratch/katoch.aa/hf_cache
export TRANSFORMERS_CACHE=/scratch/katoch.aa/hf_cache

cd /scratch/katoch.aa/book2comic/backend

echo "===== GPU Info ====="
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo "===================="

python test_pipeline.py
