@echo off
git pull
ssh huhe@perlman.mathcs.carleton.edu
cd /var/www/html/cs257/huhe
cd web-project-team-b
cd Backend
python3 webapp.py perlman.mathcs.carleton.edu 5113