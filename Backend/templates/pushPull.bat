set /p commitMsg=Enter commit message.
git pull
git add .
git commit -m "commitMsg"
git push