# Ayam Nyakot Admin Delivery Tracking

Web admin sederhana berbasis **Streamlit** untuk membantu UMKM Ayam Nyakot mencatat pesanan ayam geprek, baik pesanan online maupun pembelian langsung di tempat.

## Menu Produk

| Produk | Harga |
|---|---:|
| Ayam Geprek Tanpa Nasi | Rp10.000 |
| Ayam Geprek Pakai Nasi | Rp15.000 |

## Fitur Utama

1. Dashboard ringkasan pesanan
2. Input pesanan ayam geprek
3. Total harga otomatis berdasarkan paket dan jumlah
4. Pilihan tingkat rasa: Tidak Pedas atau Pedas
5. Metode pesanan: diantar, ambil sendiri, atau beli langsung di tempat
6. Tracking status pesanan
7. Update status pembayaran ongkir
6. Edit data pesanan
7. Export data ke CSV dan Excel

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

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Cara Deploy ke Streamlit

1. Upload semua file ke GitHub.
2. Buka Streamlit Community Cloud.
3. Pilih repository GitHub.
4. Main file path: `app.py`
5. Klik deploy.

## Catatan Penyimpanan Data

Versi ini memakai file CSV lokal pada folder `data/`.
Untuk demo project kuliah dan penggunaan sederhana, cara ini sudah cukup.
Untuk penggunaan jangka panjang, gunakan database online seperti Google Sheets, Firebase, Supabase, atau PostgreSQL.