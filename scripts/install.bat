@echo off
setlocal

:: Step 1: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and run this script again.
    exit /b 1
)

cd /d %~dp0

:: Step 2: Download and unzip the GitHub repository
echo Downloading and extracting the GitHub repository...
curl -LJO https://github.com/rpakishore/ak_sap/archive/main.zip
tar -xf ak_sap-main.zip
del ak_sap-main.zip

:: Step 3: Navigate into the ak_sap directory
cd ak_sap-main

:: Step 4: Set up virtual environment and install dependencies
echo Setting up virtual environment and installing dependencies...
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install flit && flit install --deps production

:: Step 5: Display success message
echo Installation completed successfully.

:: End
exit /b 0
