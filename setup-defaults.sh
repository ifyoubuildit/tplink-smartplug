#!/bin/sh
##create directories
mkdir ./config
mkdir ./env
mkdir ./log
mkdir ./output
mkdir ./temp_today

##create files
touch ./temp_today/temp_today_a.md
touch ./temp_today/temp_today_b.md
touch ./temp_today/temp_today_a.py
touch ./temp_today/temp_today_b.py
touch ./temp_today/temp_today_a.txt
touch ./temp_today/temp_today_b.txt
touch ./temp_today/temp_today_a.sql
touch ./temp_today/temp_today_b.sql
touch ./temp_today/temp_today_a.json
touch ./temp_today/temp_today_b.json
touch ./requirements.txt

## populate requirements.txt
echo "pylint" >> requirements.txt

##populate .gitignore
touch .gitignore
echo "#lb_defaults" >> .gitignore
echo "config/" >> .gitignore
echo "env/" >> .gitignore
echo "log/" >> .gitignore
echo "temp_today/" >> .gitignore
echo ".vscode/" >> .gitignore
echo "output/" >> .gitignore
echo "project-defualts.sh" >> .gitignore
echo ".DS_Store" >> .gitignore

##python virualenv
virtualenv env
source env/bin/activate

##requirements.txt
pip install -r ./requirements.txt