import time
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetch_html(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logging.error(f"Gagal mengambil data dari {url}: {e}")
        return None

def parse_product_element(product_div):
    def safe_text(element):
        return element.text.strip() if element else None

    data = {
        "Title": None,
        "Price": None,
        "Rating": None,
        "Colors": None,
        "Size": None,
        "Gender": None,
    }

    try:
        data["Title"] = safe_text(product_div.find("h3", class_="product-title"))

        price_container = product_div.find("div", class_="price-container")
        price_tag = price_container.find("span", class_="price") if price_container else product_div.find("p", class_="price")
        data["Price"] = safe_text(price_tag)

        for p in product_div.find_all("p"):
            lower_text = p.text.lower()
            if "rating" in lower_text:
                data["Rating"] = safe_text(p)
            elif "color" in lower_text:
                data["Colors"] = safe_text(p)
            elif "size" in lower_text:
                data["Size"] = safe_text(p)
            elif "gender" in lower_text:
                data["Gender"] = safe_text(p)

    except Exception as e:
        logging.warning(f"Gagal parsing produk: {e}")

    return data

def extract_all_products(html):
    soup = BeautifulSoup(html, "html.parser")
    product_divs = soup.find_all("div", class_="product-details")

    if not product_divs:
        logging.warning("Tidak ditemukan elemen produk pada halaman ini.")
        return []

    logging.info(f"[DEBUG] Jumlah produk ditemukan: {len(product_divs)}")
    return [parse_product_element(prod) for prod in product_divs]

def scrape_fashion_products(url, delay=1):
    """Scrape produk fashion dari satu halaman."""
    logging.info(f"[INFO] Mengambil data dari: {url}")
    html = fetch_html(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    products = extract_all_products(html)

    time.sleep(delay)
    return products
