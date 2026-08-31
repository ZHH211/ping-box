@echo off
if not exist .env copy .env.example .env
pip install -r requirements.txt
python app.py
