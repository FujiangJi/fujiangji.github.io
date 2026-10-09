git clone https://github.com/ESCOMP/CTSM.git
cd CTSM
git log --oneline

# Updated version in the original example.
git switch -c abz_updates dd0cbec
git log --oneline -5

# Version before the original update series.
git switch -c no_abz 384c726
git branch
git diff no_abz..abz_updates
