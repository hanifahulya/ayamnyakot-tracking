# Ayam Nyakot Delivery Tracking

Web sederhana berbasis **Streamlit** untuk membantu UMKM Ayam Nyakot dalam proses digitalisasi pengantaran pesanan.

## Fitur Utama

1. Dashboard ringkasan pesanan
2. Input pesanan baru
3. Tracking status pengantaran
4. Update status pembayaran ongkir
5. Edit data pesanan
6. Export data ke CSV dan Excel
7. Halaman analisis INDI 4.0 untuk kebutuhan presentasi project

## Struktur Folder

```text
ayam_nyakot_streamlit/
│
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── ayam_nyakot_delivery.csv
└── .streamlit/
    └── config.toml
```

## Cara Menjalankan di Laptop

1. Install Python.
2. Buka terminal di folder project.
3. Install library:

```bash
pip install -r requirements.txt
```

4. Jalankan aplikasi:

```bash
streamlit run app.py
```

## Cara Upload ke GitHub

1. Buat repository baru di GitHub.
2. Upload semua file dan folder project.
3. Pastikan file `app.py` dan `requirements.txt` ada di root repository.

## Cara Deploy ke Streamlit Community Cloud

1. Buka Streamlit Community Cloud.
2. Login menggunakan akun GitHub.
3. Pilih repository project.
4. Pilih file utama: `app.py`.
5. Klik deploy.

## Catatan Penyimpanan Data

Versi ini memakai file CSV lokal pada folder `data/`.
Untuk demo project kuliah, cara ini sudah cukup.
Untuk penggunaan nyata jangka panjang, sebaiknya gunakan database online seperti:

- Google Sheets
- Firebase
- Supabase
- PostgreSQL