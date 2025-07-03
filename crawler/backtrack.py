# Pengembang: Revandi Faudiamar Putra Sitepu
# Tanggal: 2025-07-01

# Deskripsi: Kode ini digunakan untuk mengambil artikel dari situs berita Bisnis.com
# dengan menggunakan Selenium. Kode ini akan mengambil artikel berdasarkan rentang tanggal yang diberikan
import sys
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core import get_driver, parse_article, save_json

def crawl_by_date_range(start_date_str, end_date_str):
    driver = get_driver(headless=True)
    output = []

    try:
        start = datetime.strptime(start_date_str, "%Y-%m-%d")
        end = datetime.strptime(end_date_str, "%Y-%m-%d")
        delta = timedelta(days=1)

        while start <= end:
            iso_format = start.strftime("%Y-%m-%d")
            print(f"\n📅 Mengambil artikel untuk tanggal {iso_format}...")

            # Gunakan URL dengan parameter tanggal
            tanggal_url = f"https://www.bisnis.com/index?categoryId=0&type=indeks&date={iso_format}&type=indeks"
            driver.get(tanggal_url)

            try:
                # Tunggu hingga daftar artikel muncul
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#indeksListView .artItem"))
                )

                # Ambil semua URL artikel
                links = driver.find_elements(By.CSS_SELECTOR, "#indeksListView .artItem a.artLink[href]")
                urls = list({a.get_attribute("href") for a in links if a.get_attribute("href")})

                print(f"🔗 Ditemukan {len(urls)} artikel")

                for i, url in enumerate(urls, 1):
                    print(f"  ⏳ ({i}/{len(urls)}) Memproses: {url}")
                    article = parse_article(driver, url)
                    if article:
                        output.append(article)

            except Exception as e:
                print(f"⚠️ Tidak ada artikel atau gagal parsing tanggal {iso_format}: {e}")

            start += delta

    finally:
        driver.quit()
        save_json(output, "output/backtrack_output.json")
        print("\n✅ Selesai. Hasil disimpan ke output/backtrack_output.json")

# --- CLI Entrypoint ---
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("❗ Cara pakai: python backtrack.py 2025-07-01 2025-07-02")
        sys.exit(1)

    crawl_by_date_range(sys.argv[1], sys.argv[2])
