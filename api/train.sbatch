#!/bin/bash
#SBATCH --job-name=connectX
#SBATCH --nodes=1
#SBATCH --gpus=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=dgx
#SBATCH --output=logs/%j.out

uv run train.py \
    --model cnn \
    --epochs 20 \
    --batch_size 64 \
    --learning_rate 0.001 \