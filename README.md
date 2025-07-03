# Technical-Test-NoLimit-Indonesia

# Bisnis.com Crawler (Standard & Backtrack Mode)

Proyek ini adalah implementasi crawler untuk situs [bisnis.com](https://www.bisnis.com), dengan dua mode utama:

- **Standard Mode**: Long-running crawler untuk mendeteksi dan menyimpan artikel terbaru secara berkala.
- **Backtrack Mode**: Penarikan artikel berdasarkan rentang tanggal historis tertentu.

---

## 📁 Struktur Folder

```
.
├── core.py               # Modul utama untuk parsing & setup driver
├── standard.py           # Crawler long-running mode
├── backtrack.py          # Crawler rentang tanggal historis
├── .env                  # Konfigurasi environment (INTERVAL & LIMIT)
├── output/               # Folder hasil JSON
├── requirements.txt      # Dependency Python
└── README.md             # Dokumentasi
```

---

## ⚙️ Konfigurasi

Gunakan file `.env` untuk mengatur interval dan jumlah maksimum artikel per scraping:

```env
INTERVAL=600      # waktu jeda antar scraping (dalam detik)
LIMIT=10          # jumlah artikel yang diambil setiap siklus
```

---

## 🚀 Cara Menjalankan

### 1. **Instalasi Dependency**

```bash
pip install -r requirements.txt
```

### 2. **Menjalankan Standard Mode**

Crawler akan berjalan terus dan menyimpan artikel hanya jika ada pembaruan.

```bash
python standard.py
```

Opsi tambahan:

```bash
python standard.py --interval 300 --limit 5
```

---

### 3. **Menjalankan Backtrack Mode**

Menarik artikel dari tanggal tertentu (dalam format `YYYY-MM-DD`):

```bash
python backtrack.py 2025-07-01 2025-07-02
```

---

## 🏗️ Arsitektur Crawler

### 1. `core.py`
Modul inti yang berisi:
- `get_driver()`: Setup browser headless (Chrome via Selenium)
- `parse_article(url)`: Scrape judul, isi, dan tanggal dari halaman artikel
- `save_json(data, filename)`: Menyimpan data ke file JSON

### 2. `standard.py`
- Crawler berjalan terus-menerus berdasarkan interval waktu tertentu.
- Gunakan *hashing* daftar URL untuk mendeteksi perubahan.
- Tidak menyimpan data jika tidak ada berita baru.

### 3. `backtrack.py`
- Mendukung scraping berdasarkan rentang tanggal (`index?date=...`).
- Setiap artikel dikunjungi dan diparse seperti pada mode standar.

---

## 📝 Output

- Semua artikel disimpan dalam format `.json` di folder `output/`.
- Nama file dilabeli timestamp: `standard_output_YYYYMMDD_HHMMSS.json`.

---

## 📦 Dependency

```
selenium
webdriver-manager
beautifulsoup4
python-dotenv
dateparser
```

---

## 🧪 Catatan Tambahan

- Pastikan versi Chrome dan ChromeDriver sinkron (ditangani otomatis oleh `webdriver-manager`).
- Hanya artikel dengan struktur valid yang akan diproses.
- Proyek ini tidak menyimpan duplikat dan efisien secara I/O karena membandingkan hash artikel terakhir.

---

## 📬 Kontak

Pengembang: Revandi Faudiamar  
PKL – Data Engineer – NoLimit Indonesia