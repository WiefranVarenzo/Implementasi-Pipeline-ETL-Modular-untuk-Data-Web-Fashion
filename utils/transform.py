import pandas as pd
from datetime import datetime

def transform_to_DataFrame(data):
    try:
        return pd.DataFrame(data)
    except Exception as e:
        print(f"[ERROR] Gagal membuat DataFrame: {e}")
        return pd.DataFrame()

def transform_data(data, exchange_rate):
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['Extraction Timestamp'] = timestamp

        data = data[~data['Title'].str.contains("Unknown Product", na=False)]
        data = data[~data['Rating'].astype(str).str.contains("Invalid Rating", na=False)]
        data = data[~data['Price'].astype(str).str.contains("Price Unavailable", na=False)]

        data = data.drop_duplicates(subset=['Title'], keep='first')

        data['Price'] = data['Price'].replace(r'\$', '', regex=True).astype(float) * exchange_rate
        data['Rating'] = data['Rating'].str.extract(r'(\d+\.\d+)').astype(float)
        data = data.dropna(subset=['Rating']) 
        data['Colors'] = data['Colors'].replace('Colors', '', regex=True).str.strip().astype('int64')
        data['Size'] = data['Size'].replace('Size:', '', regex=True).str.strip()
        data['Gender'] = data['Gender'].replace('Gender:', '', regex=True).str.strip()

        data = data.dropna(subset=['Price', 'Rating','Colors', 'Size', 'Gender'])
        data = data.astype({
            'Title': 'object',
            'Price': 'float64',
            'Rating': 'float64',
            'Colors': 'int64',
            'Size': 'object',
            'Gender': 'object',
            'Extraction Timestamp': 'object'
        })

        print(f"[INFO] Jumlah data setelah transformasi: {len(data)}")

        return data

    except KeyError as e:
        print(f"[ERROR] Kolom tidak ditemukan: {e}")
    except ValueError as e:
        print(f"[ERROR] Gagal konversi nilai: {e}")
    except Exception as e:
        print(f"[ERROR] Kesalahan tidak terduga saat transformasi: {e}")

    return pd.DataFrame()
