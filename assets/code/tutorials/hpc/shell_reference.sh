# Navigate and inspect files.
pwd
cd project
ls -lh
cat notes.txt
readlink -f notes.txt
wc -l notes.txt
grep "pattern" notes.txt
echo "A B B A C C" > example.txt
python3 wc.py example.txt

# Archives: write an archive outside the directory being archived.
zip -r example.zip example/
unzip -l example.zip
unzip example.zip
tar -cvf data.tar data_folder/
tar -xvf data.tar -C destination/
tar -xzf data.tar.gz -C destination/

# Compile and run the original ecosystem-model example.
g++ xtem423e4.cpp -o temmodel
./temmodel tem4.para tem4.log
module avail
make

# Shell configuration and aliases.
nano ~/.bashrc
source ~/.bashrc
# On macOS with Zsh, use ~/.zshrc instead.

# Conda environment management.
conda env list
conda activate research
conda deactivate

# Interactive Slurm testing (adapt the resource request).
srun --partition=int --nodes=1 --ntasks=1 --cpus-per-task=4 --time=00:30:00 --pty bash

# In the vi editor: :wq saves and exits; :q! exits without saving.
