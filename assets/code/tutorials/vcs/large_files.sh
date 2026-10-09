git lfs install
git lfs track "data/large_file.zip"
git add .gitattributes
git add "data/large_file.zip"
git commit -m "Track research archive with Git LFS"
git push origin main

# After cloning a repository that uses LFS:
git lfs ls-files
git lfs pull
