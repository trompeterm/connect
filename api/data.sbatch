#!/bin/bash
#SBATCH --job-name=gen-data
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=teaching
#SBATCH --output=logs/%j.out

uv run -m data.generate_dataset --games 10000