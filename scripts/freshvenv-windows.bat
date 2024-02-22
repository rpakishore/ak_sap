cd /d %~dp0
cd ..
RD /S /Q .venv

python -m venv .venv

call .venv\Scripts\activate.bat
python.exe -m pip install --upgrade pip
pip install flit
flit install --pth-file

python -m streamlit run Start_Here.py