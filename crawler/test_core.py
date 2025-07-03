# Pengembang: Revandi Faudiamar Putra Sitepu
# Tanggal: 2025-07-01

# Deskripsi: Kode ini digunakan untuk testing fungsi-fungsi di core.py
# dengan mengambil contoh artikel dari situs berita Bisnis.com.

from core import get_driver, parse_article, save_json

test_url = "https://market.bisnis.com/read/20250703/235/1890046/harga-emas-antam-turun-jadi-rp191-juta-per-gram-mau-borong"

driver = get_driver(headless=False)  # headless=False agar bisa melihat prosesnya
article = parse_article(driver, test_url)
driver.quit()

if article:
    print("\n=== HASIL PARSING ===")
    print(f"Judul       : {article['title']}")
    print(f"URL         : {article['url']}")
    print(f"Published   : {article['published_at']}")
    print(f"Isi Artikel :\n{article['content'][:500]}...")  # Tampilkan 500 karakter pertama dari isi artikel
    save_json([article], "output/test_article.json")
else:
    print("❌ Gagal mengambil artikel.")
