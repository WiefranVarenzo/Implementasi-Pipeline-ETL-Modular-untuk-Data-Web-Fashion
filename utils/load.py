from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def store_to_csv(data):
    try:
        data.to_csv('products.csv', index=False)
        print("[SUCCESS] Data berhasil disimpan ke CSV (products.csv).")
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan CSV: {e}")

def store_to_postgre(data, db_url):
    try:
        engine = create_engine(db_url)
        with engine.begin() as conn:
            data.to_sql('fashion_data', con=conn, if_exists='append', index=False)
        print("[SUCCESS] Data berhasil disimpan ke PostgreSQL.")
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan ke PostgreSQL: {e}")
        raise

def store_to_sheets(data):
    try:
        SERVICE_ACCOUNT_FILE = './google-sheets-api.json'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        SPREADSHEET_ID = '18ltomYAv0G3NBuNdCEVJtU0Iyv7gv_F7xoG2nMDRwTM'
        RANGE_NAME = 'Sheet1!A2'

        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        values = [list(row) for row in data.values]
        body = {'values': values}

        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"[SUCCESS] Data berhasil dikirim ke Google Sheets ({result.get('updatedCells')} sel diperbarui).")

    except Exception as e:
        print(f"[ERROR] Gagal menyimpan ke Google Sheets: {e}")
        raise
