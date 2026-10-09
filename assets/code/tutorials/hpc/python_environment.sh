# Run after installing Conda according to the CHTC guide.
conda env list
conda create -n research python=3.11
conda activate research
conda install numpy pandas matplotlib
conda env export > environment.yml
conda deactivate
# Run the analysis through a compute job, using the next section.
