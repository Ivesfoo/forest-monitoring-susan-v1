@echo off
cd /d C:\Users\USER\Desktop\EPH CODES\eph-forest-monitoring-v2

call venv\Scripts\activate

start cmd /k streamlit run app.py
start cmd /k python run_live_ingestion_loop.py