from utils.extract import scrape_fashion_products
from utils.transform import transform_to_DataFrame, transform_data
from utils.load import store_to_csv, store_to_postgre, store_to_sheets

def main():
    base_url = 'https://fashion-studio.dicoding.dev/'
    all_products = []

    print(f"[INFO] Memulai scraping halaman utama: {base_url}")
    try:
        products = scrape_fashion_products(base_url)
        all_products.extend(products)
    except Exception as e:
        print(f"[ERROR] Gagal scraping halaman utama: {e}")

    for page in range(2, 51):
        url = f"{base_url}page{page}"
        print(f"[INFO] Scraping halaman {page}: {url}")
        try:
            products = scrape_fashion_products(url)
            print(f"[INFO] Halaman {page} berhasil dikumpulkan {len(products)} produk")
            all_products.extend(products)
        except Exception as e:
            print(f"[WARNING] Gagal scraping halaman {page}: {e}")

    if not all_products:
        print("[ERROR] Tidak ada produk ditemukan dari seluruh halaman.")
        return

    print(f"[INFO] Total produk berhasil dikumpulkan: {len(all_products)}")

    df = transform_to_DataFrame(all_products)
    exchange_rate = 16000
    df_transformed = transform_data(df, exchange_rate)

    #Menyimpan ke csv
    store_to_csv(df_transformed)

    #Menyimpan ke database postgresql
    db_url = 'postgresql+psycopg2://developer:Admin23@localhost:5432/fashionstudiodb'
    store_to_postgre(df_transformed, db_url)
    
    #Menyimpan ke google sheets
    store_to_sheets(df_transformed)

if __name__ == '__main__':
    main()
