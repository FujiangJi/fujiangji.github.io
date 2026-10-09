git switch -c feature-analysis
# Edit your analysis, then review and record the changes.
git diff
git add analysis.py
git commit -m "Add analysis workflow"
git push -u origin feature-analysis

# After review, merge the branch into main.
git switch main
git merge feature-analysis
git push origin main
git branch -d feature-analysis
