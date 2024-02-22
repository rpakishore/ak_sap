@echo off

mode con cols=40 lines=15

cd /d %~dp0
cd ..

rem Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python needs to be installed for this script to work
    pause
    exit /b 1
)

rem Check if .venv folder exists
if not exist .venv (

    echo Virtual environment not found. Creating a new virtual environment.
    
    python -m venv .venv
    call .venv\Scripts\activate.bat

    echo Installing dependencies

    pip install flit
    flit install --pth-file

    deactivate

)

echo Activating virtual environment

call .venv\Scripts\activate.bat

rem Run the streamlit app
python -m streamlit run Start_Here.py