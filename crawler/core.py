from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import dateparser
import json
import os

def get_driver(headless=True):
    options = webdriver.ChromeOptions()
    # hanya Sebagian load agar lebih cepat
    options.page_load_strategy = 'eager'
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")  # Supaya log SSL warning hilang

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def parse_article(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.detailsTitleCaption"))
        )

        # Judul Artikel
        title = driver.find_element(By.CSS_SELECTOR, "h1.detailsTitleCaption").text.strip()

        # Isi Artikel
        paragraphs = driver.find_elements(By.CSS_SELECTOR, "article.detailsContent p")
        content = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())

        try:
            # === Percobaan utama: .detailsAttributeDates ===
            try:
                tanggal_elem = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".detailsAttributeDates"))
                )
                tanggal_text = tanggal_elem.text.strip()
            except:
                # === Fallback: cari span.detailsAttributeItem yang mengandung ikon kalender ===
                tanggal_items = driver.find_elements(By.CSS_SELECTOR, ".detailsAttributeItem")
                tanggal_text = ""
                for item in tanggal_items:
                    if "icoCal" in item.get_attribute("innerHTML"):
                        tanggal_text = item.text.strip()
                        break

            if not tanggal_text:
                raise ValueError("Tanggal tidak ditemukan.")

            # Pastikan hapus 'WIB' jika ada
            tanggal_clean = tanggal_text.split(",")[1].strip().replace(" WIB", "")
            dt = dateparser.parse(tanggal_clean)
            published_at = dt.isoformat() if dt else None

        except Exception as e:
            print(f"Gagal parsing tanggal dari teks '{tanggal_text if 'tanggal_text' in locals() else ''}': {e}")
            published_at = None

        return {
            "title": title,
            "url": url,
            "content": content,
            "published_at": published_at
        }

    except Exception as e:
        print(f"Gagal mengambil artikel dari {url}: {e}")
        return None

def save_json(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)