# --- file: test_core.py ---
from core import get_driver, parse_article, save_json

# Ganti dengan salah satu URL artikel Bisnis.com yang valid
test_url = "https://market.bisnis.com/read/20250703/235/1890046/harga-emas-antam-turun-jadi-rp191-juta-per-gram-mau-borong"

driver = get_driver(headless=False)  # headless=False biar kamu bisa lihat browsernya
article = parse_article(driver, test_url)
driver.quit()

if article:
    print("\n=== HASIL PARSING ===")
    print(f"Judul       : {article['title']}")
    print(f"URL         : {article['url']}")
    print(f"Published   : {article['published_at']}")
    print(f"Isi Artikel :\n{article['content'][:500]}...")  # tampilkan sebagian isi
    save_json([article], "output/test_article.json")
else:
    print("❌ Gagal mengambil artikel.")
