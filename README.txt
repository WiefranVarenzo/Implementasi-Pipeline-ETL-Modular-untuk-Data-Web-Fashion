# Membuat virtual environment (Windows)
python -m venv myenv
myenv/Scripts/Activate

# Install dependencies
pip install -r requirements.txt

# Menjalankan skrip ETL pipeline
python main.py

# Menjalankan unit test pada folder tests
python -m pytest tests/ -v

# Menjalankan unit test pada folder utils
python -m pytest tests/ --cov=utils --cov-report=html -v

# Menjalankan unit test pada folder utils dan tests sekaligus
python -m pytest tests/ --cov=utils --cov=tests --cov-report=html -v

# Melihat hasil test coverage dalam browser
start htmlcov/index.html

Catatan:
Perlu diingat, hasil index.html coverage test yang dihasilkan bergantung pada perintah yang dijalankan.

Untuk Google Sheet tidak disertakan untuk mencegah Account Key tersebar
