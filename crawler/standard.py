# Pengembang: Revandi Faudiamar Putra Sitepu
# Tanggal: 2025-07-02

# Deskripsi: Kode ini digunakan untuk mengambil artikel terbaru dari situs berita Bisnis.com
# dengan menggunakan Selenium. Kode ini akan mengambil artikel terbaru secara berkelanjutan sesuai dengan konfigurasi pada env.
import argparse
import time
import hashlib
from datetime import datetime
from core import get_driver, parse_article, save_json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load konfigurasi dari .env
load_dotenv()
ENV_INTERVAL = int(os.getenv("INTERVAL", 600))  # default 600 detik
ENV_LIMIT = int(os.getenv("LIMIT", 10))         # default 10 artikel

URL_INDEKS = "https://www.bisnis.com/index"
OUTPUT_DIR = "output"

def get_latest_article_urls(driver, limit=10):
    driver.get(URL_INDEKS)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "indeksListView"))
    )
    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = soup.select("div.artItem a.artLink")
    urls = []
    for a in articles:
        href = a.get("href")
        if href and href.startswith("https") and href not in urls:
            urls.append(href)
        if len(urls) >= limit:
            break
    return urls

def crawl_latest(driver, limit=10):
    urls = get_latest_article_urls(driver, limit=limit)
    print(f"📰 Ditemukan {len(urls)} artikel terbaru.")
    result = []
    for i, url in enumerate(urls, start=1):
        print(f"  ⏳ ({i}/{len(urls)}) Memproses: {url}")
        article = parse_article(driver, url)
        if article:
            result.append(article)
    return result

def compute_hash_from_urls(urls):
    joined = "".join(urls)
    return hashlib.md5(joined.encode("utf-8")).hexdigest()

def main(interval, limit):
    driver = get_driver()
    last_hash = None  # Simpan hash artikel terakhir

    print(f"🔁 Memulai crawler standard mode dengan interval {interval} detik...")
    try:
        while True:
            urls = get_latest_article_urls(driver, limit=limit)
            current_hash = compute_hash_from_urls(urls)

            if current_hash != last_hash:
                articles = []
                for i, url in enumerate(urls, start=1):
                    print(f"  ⏳ ({i}/{len(urls)}) Memproses: {url}")
                    article = parse_article(driver, url)
                    if article:
                        articles.append(article)                       
                now = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{OUTPUT_DIR}/standard_output_{now}.json"
                save_json(articles, filename)
                print(f"✅ Disimpan ke {filename}")
                last_hash = current_hash
            else:
                print("🟡 Tidak ada artikel baru. Lewati penulisan file.")

            print(f"🕒 Menunggu {interval} detik untuk penarikan selanjutnya...\n")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("⛔ Dihentikan oleh user (CTRL+C)")
    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Standard Mode Bisnis.com Crawler")
    parser.add_argument("--interval", type=int, help="Interval dalam detik (default dari .env atau 600)")
    parser.add_argument("--limit", type=int, help="Batas jumlah artikel terbaru (default dari .env atau 10)")
    args = parser.parse_args()

    # Gunakan nilai dari CLI jika ada, jika tidak ambil dari .env
    interval = args.interval if args.interval is not None else ENV_INTERVAL
    limit = args.limit if args.limit is not None else ENV_LIMIT

    main(interval, limit)