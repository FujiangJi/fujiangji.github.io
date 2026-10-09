#!/bin/bash
#SBATCH --job-name=research_example
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00
#SBATCH --output=research_%j.out
#SBATCH --error=research_%j.err

# Replace the Conda installation, environment, and analysis paths.
source /path/to/miniconda3/etc/profile.d/conda.sh
conda activate research
cd /scratch/YOUR_NETID/project
python analysis.py
