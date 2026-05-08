import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, date
import random
import io

# =========================================================
# AYAM NYAKOT - ADMIN DELIVERY TRACKING
# Web admin/owner untuk mencatat pesanan, pengantaran, dan ongkir
# =========================================================

st.set_page_config(
    page_title="Ayam Nyakot Admin",
    page_icon="🍗",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "ayam_nyakot_delivery.csv"

STATUS_OPTIONS = [
    "Pesanan Dibuat",
    "Disiapkan",
    "Dalam Pengantaran",
    "Terkirim",
    "Selesai",
    "Dibatalkan"
]

PAYMENT_OPTIONS = [
    "Belum Dibayar",
    "Sudah Dibayar"
]

COURIER_OPTIONS = [
    "Kurir Internal",
    "Ojek Online",
    "Ambil Sendiri",
    "Lainnya"
]

PAKET_MENU = {
    "Ayam Geprek Tanpa Nasi": 10000,
    "Ayam Geprek Pakai Nasi": 15000
}

LEVEL_PEDAS = [
    "Tidak Pedas",
    "Level 1",
    "Level 2",
    "Level 3",
    "Level 4",
    "Level 5"
]

COLUMNS = [
    "order_id",
    "tanggal",
    "nama_pelanggan",
    "no_hp",
    "alamat_pengantaran",
    "menu_pesanan",
    "jumlah",
    "total_pesanan",
    "ongkir",
    "metode_kurir",
    "nama_kurir",
    "status_pengantaran",
    "status_pembayaran_ongkir",
    "estimasi_sampai",
    "catatan",
    "updated_at"
]


# =========================
# STYLE / CSS
# =========================
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(180deg, #fffaf3 0%, #ffffff 35%);
    }

    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2rem;
    }

    .hero {
        padding: 26px 28px;
        border-radius: 28px;
        background: linear-gradient(135deg, #ff8c00 0%, #ff4d00 55%, #7a1d00 100%);
        color: white;
        box-shadow: 0 18px 40px rgba(255, 91, 0, .22);
        margin-bottom: 22px;
    }

    .hero h1 {
        font-size: 2.4rem;
        margin-bottom: 6px;
    }

    .hero p {
        font-size: 1.02rem;
        opacity: .96;
        margin: 0;
    }

    .menu-price-card {
        padding: 18px 20px;
        border-radius: 22px;
        background: #fff7ed;
        border: 1px solid #fed7aa;
        margin-bottom: 12px;
    }

    .menu-title {
        font-weight: 900;
        color: #431407;
        font-size: 1.1rem;
    }

    .menu-price {
        color: #ea580c;
        font-weight: 900;
        font-size: 1.4rem;
    }

    .metric-card {
        padding: 18px;
        border-radius: 22px;
        background: #fff7ed;
        border: 1px solid #fed7aa;
        height: 100%;
    }

    .metric-label {
        color: #7c2d12;
        font-size: .9rem;
        font-weight: 700;
    }

    .metric-value {
        color: #431407;
        font-size: 1.7rem;
        font-weight: 900;
        margin-top: 2px;
    }

    .status-pill {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: .82rem;
        font-weight: 800;
    }

    .pill-progress { background: #dbeafe; color: #1e40af; }
    .pill-done { background: #dcfce7; color: #166534; }
    .pill-unpaid { background: #fee2e2; color: #991b1b; }
    .pill-paid { background: #dcfce7; color: #166534; }
    .pill-cancel { background: #f3f4f6; color: #374151; }

    div[data-testid="stMetricValue"] {
        font-weight: 900;
    }

    .footer-box {
        padding: 18px;
        border-radius: 18px;
        background: #292524;
        color: white;
        margin-top: 24px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# HELPER FUNCTIONS
# =========================
def rupiah(value):
    try:
        value = int(float(value))
        return f"Rp{value:,.0f}".replace(",", ".")
    except Exception:
        return "Rp0"


def now_string():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_order_id():
    today = datetime.now().strftime("%Y%m%d")
    suffix = random.randint(1000, 9999)
    return f"AN-{today}-{suffix}"


def ensure_data_file():
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        sample = pd.DataFrame(
            [
                {
                    "order_id": "AN-20260508-1001",
                    "tanggal": "2026-05-08",
                    "nama_pelanggan": "Rina",
                    "no_hp": "081234567890",
                    "alamat_pengantaran": "Jl. Merdeka No. 10",
                    "menu_pesanan": "Ayam Geprek Pakai Nasi - Level 3",
                    "jumlah": 2,
                    "total_pesanan": 30000,
                    "ongkir": 8000,
                    "metode_kurir": "Kurir Internal",
                    "nama_kurir": "Bang Andi",
                    "status_pengantaran": "Dalam Pengantaran",
                    "status_pembayaran_ongkir": "Belum Dibayar",
                    "estimasi_sampai": "18:30",
                    "catatan": "Tolong antar ke pos satpam.",
                    "updated_at": now_string(),
                },
                {
                    "order_id": "AN-20260508-1002",
                    "tanggal": "2026-05-08",
                    "nama_pelanggan": "Dimas",
                    "no_hp": "082111223344",
                    "alamat_pengantaran": "Kampus / Gedung B",
                    "menu_pesanan": "Ayam Geprek Tanpa Nasi - Level 2",
                    "jumlah": 1,
                    "total_pesanan": 10000,
                    "ongkir": 5000,
                    "metode_kurir": "Ojek Online",
                    "nama_kurir": "Driver Online",
                    "status_pengantaran": "Selesai",
                    "status_pembayaran_ongkir": "Sudah Dibayar",
                    "estimasi_sampai": "17:15",
                    "catatan": "-",
                    "updated_at": now_string(),
                },
                {
                    "order_id": "AN-20260508-1003",
                    "tanggal": "2026-05-08",
                    "nama_pelanggan": "Salsa",
                    "no_hp": "085266778899",
                    "alamat_pengantaran": "Kos Melati, Kamar 12",
                    "menu_pesanan": "Ayam Geprek Pakai Nasi - Level 5",
                    "jumlah": 3,
                    "total_pesanan": 45000,
                    "ongkir": 10000,
                    "metode_kurir": "Kurir Internal",
                    "nama_kurir": "Bang Budi",
                    "status_pengantaran": "Disiapkan",
                    "status_pembayaran_ongkir": "Belum Dibayar",
                    "estimasi_sampai": "19:00",
                    "catatan": "Pedas maksimal.",
                    "updated_at": now_string(),
                },
            ],
            columns=COLUMNS
        )
        sample.to_csv(DATA_FILE, index=False)


@st.cache_data(show_spinner=False)
def load_data():
    ensure_data_file()
    df = pd.read_csv(DATA_FILE)
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = ""
    df = df[COLUMNS]
    df["jumlah"] = pd.to_numeric(df["jumlah"], errors="coerce").fillna(0).astype(int)
    df["total_pesanan"] = pd.to_numeric(df["total_pesanan"], errors="coerce").fillna(0).astype(int)
    df["ongkir"] = pd.to_numeric(df["ongkir"], errors="coerce").fillna(0).astype(int)
    return df


def save_data(df):
    DATA_DIR.mkdir(exist_ok=True)
    df = df[COLUMNS]
    df.to_csv(DATA_FILE, index=False)
    st.cache_data.clear()


def add_order(new_row):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)


def update_order(order_id, fields):
    df = load_data()
    idx = df.index[df["order_id"] == order_id]
    if len(idx) == 0:
        return False
    for key, value in fields.items():
        df.loc[idx, key] = value
    df.loc[idx, "updated_at"] = now_string()
    save_data(df)
    return True


def delete_order(order_id):
    df = load_data()
    df = df[df["order_id"] != order_id]
    save_data(df)


def get_status_badge(status):
    if status in ["Selesai", "Terkirim"]:
        return f"<span class='status-pill pill-done'>{status}</span>"
    if status == "Dibatalkan":
        return f"<span class='status-pill pill-cancel'>{status}</span>"
    return f"<span class='status-pill pill-progress'>{status}</span>"


def get_payment_badge(status):
    if status == "Sudah Dibayar":
        return f"<span class='status-pill pill-paid'>{status}</span>"
    return f"<span class='status-pill pill-unpaid'>{status}</span>"


def make_csv_download(df):
    return df.to_csv(index=False).encode("utf-8")


def make_excel_download(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Tracking Ayam Nyakot")
    return output.getvalue()


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🍗 Ayam Nyakot")
    st.caption("Admin Delivery Tracking")
    st.divider()

    page = st.radio(
        "Menu",
        [
            "Dashboard",
            "Tambah Pesanan",
            "Tracking Pesanan",
            "Update Status",
            "Data & Export"
        ]
    )

    st.divider()
    st.markdown("### Daftar Menu")
    st.markdown(
        """
        <div class="menu-price-card">
            <div class="menu-title">Ayam Geprek Tanpa Nasi</div>
            <div class="menu-price">Rp10.000</div>
        </div>
        <div class="menu-price-card">
            <div class="menu-title">Ayam Geprek Pakai Nasi</div>
            <div class="menu-price">Rp15.000</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# HEADER
# =========================
st.markdown(
    """
    <div class="hero">
        <h1>🍗 Ayam Nyakot Admin</h1>
        <p>Web admin untuk mencatat pesanan ayam geprek, memantau pengantaran, dan mengecek pembayaran ongkir.</p>
    </div>
    """,
    unsafe_allow_html=True
)

df = load_data()


# =========================
# PAGE: DASHBOARD
# =========================
if page == "Dashboard":
    total_order = len(df)
    ongoing_order = len(df[df["status_pengantaran"].isin(["Pesanan Dibuat", "Disiapkan", "Dalam Pengantaran"])])
    done_order = len(df[df["status_pengantaran"].isin(["Terkirim", "Selesai"])])
    unpaid_ongkir = len(df[df["status_pembayaran_ongkir"] == "Belum Dibayar"])
    total_omzet = df.loc[df["status_pengantaran"] != "Dibatalkan", "total_pesanan"].sum()
    total_ongkir = df["ongkir"].sum()
    paid_ongkir_value = df.loc[df["status_pembayaran_ongkir"] == "Sudah Dibayar", "ongkir"].sum()
    unpaid_ongkir_value = df.loc[df["status_pembayaran_ongkir"] == "Belum Dibayar", "ongkir"].sum()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Total Pesanan</div><div class='metric-value'>{total_order}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Sedang Diproses</div><div class='metric-value'>{ongoing_order}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Selesai/Terkirim</div><div class='metric-value'>{done_order}</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Ongkir Belum Dibayar</div><div class='metric-value'>{unpaid_ongkir}</div></div>", unsafe_allow_html=True)

    st.markdown("### Ringkasan Penjualan & Ongkir")
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Total Omzet Pesanan", rupiah(total_omzet))
    col_b.metric("Total Ongkir", rupiah(total_ongkir))
    col_c.metric("Ongkir Sudah Dibayar", rupiah(paid_ongkir_value))
    col_d.metric("Ongkir Belum Dibayar", rupiah(unpaid_ongkir_value))

    st.markdown("### Pesanan Terbaru")
    if df.empty:
        st.info("Belum ada data pesanan.")
    else:
        latest = df.sort_values("updated_at", ascending=False).head(8).copy()
        latest["total_pesanan"] = latest["total_pesanan"].apply(rupiah)
        latest["ongkir"] = latest["ongkir"].apply(rupiah)
        st.dataframe(
            latest[
                [
                    "order_id",
                    "tanggal",
                    "nama_pelanggan",
                    "menu_pesanan",
                    "jumlah",
                    "total_pesanan",
                    "status_pengantaran",
                    "status_pembayaran_ongkir",
                    "ongkir",
                    "updated_at"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.markdown("### Grafik Status Pengantaran")
    status_count = df["status_pengantaran"].value_counts().reset_index()
    status_count.columns = ["Status", "Jumlah"]
    if not status_count.empty:
        st.bar_chart(status_count.set_index("Status"))

    st.markdown(
        """
        <div class="footer-box">
        <b>Catatan admin:</b> Pesanan yang sudah dibayar ongkirnya sebaiknya langsung diubah menjadi “Sudah Dibayar” agar tidak tertukar saat rekap harian.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# PAGE: TAMBAH PESANAN
# =========================
elif page == "Tambah Pesanan":
    st.markdown("## ➕ Tambah Pesanan Baru")
    st.caption("Gunakan form ini setiap ada pesanan ayam geprek yang perlu dicatat dan dipantau.")

    with st.form("form_tambah_pesanan", clear_on_submit=True):
        c1, c2 = st.columns(2)

        with c1:
            tanggal = st.date_input("Tanggal Pesanan", value=date.today())
            nama_pelanggan = st.text_input("Nama Pelanggan")
            no_hp = st.text_input("Nomor HP / WhatsApp")
            alamat_pengantaran = st.text_area("Alamat Pengantaran")

            paket = st.selectbox("Pilih Menu", list(PAKET_MENU.keys()))
            level = st.selectbox("Level Pedas", LEVEL_PEDAS)
            harga_satuan = PAKET_MENU[paket]
            jumlah = st.number_input("Jumlah Porsi", min_value=1, value=1, step=1)

            total_pesanan = harga_satuan * int(jumlah)

            st.info(f"Harga satuan: {rupiah(harga_satuan)}")
            st.success(f"Total harga pesanan otomatis: {rupiah(total_pesanan)}")

        with c2:
            ongkir = st.number_input("Ongkir / Bill Pengantaran (Rp)", min_value=0, value=0, step=1000)
            metode_kurir = st.selectbox("Metode Kurir", COURIER_OPTIONS)
            nama_kurir = st.text_input("Nama Kurir / Driver")
            status_pengantaran = st.selectbox("Status Pengantaran Awal", STATUS_OPTIONS, index=0)
            status_pembayaran_ongkir = st.selectbox("Status Pembayaran Ongkir", PAYMENT_OPTIONS, index=0)
            estimasi_sampai = st.text_input("Estimasi Sampai", placeholder="Contoh: 18:30")
            catatan = st.text_area("Catatan", placeholder="Contoh: ongkir dibayar saat pesanan sampai")

            total_bayar = total_pesanan + int(ongkir)
            st.warning(f"Total bayar termasuk ongkir: {rupiah(total_bayar)}")

        submitted = st.form_submit_button("Simpan Pesanan", type="primary", use_container_width=True)

        if submitted:
            if not nama_pelanggan or not no_hp or not alamat_pengantaran:
                st.error("Nama pelanggan, nomor HP, dan alamat wajib diisi.")
            else:
                menu_pesanan = f"{paket} - {level}"

                new_order = {
                    "order_id": generate_order_id(),
                    "tanggal": str(tanggal),
                    "nama_pelanggan": nama_pelanggan,
                    "no_hp": no_hp,
                    "alamat_pengantaran": alamat_pengantaran,
                    "menu_pesanan": menu_pesanan,
                    "jumlah": int(jumlah),
                    "total_pesanan": int(total_pesanan),
                    "ongkir": int(ongkir),
                    "metode_kurir": metode_kurir,
                    "nama_kurir": nama_kurir if nama_kurir else "-",
                    "status_pengantaran": status_pengantaran,
                    "status_pembayaran_ongkir": status_pembayaran_ongkir,
                    "estimasi_sampai": estimasi_sampai if estimasi_sampai else "-",
                    "catatan": catatan if catatan else "-",
                    "updated_at": now_string()
                }
                add_order(new_order)
                st.success(f"Pesanan berhasil disimpan dengan ID: {new_order['order_id']}")
                st.info(f"Total pesanan: {rupiah(total_pesanan)} | Ongkir: {rupiah(ongkir)} | Total bayar: {rupiah(total_bayar)}")


# =========================
# PAGE: TRACKING PESANAN
# =========================
elif page == "Tracking Pesanan":
    st.markdown("## 🔎 Tracking Pesanan")
    st.caption("Cari pesanan berdasarkan ID, nama pelanggan, nomor HP, alamat, atau menu.")

    keyword = st.text_input("Masukkan kata kunci pencarian", placeholder="Contoh: AN-20260508-1001 / Rina / Level 3")
    status_filter = st.multiselect("Filter Status Pengantaran", STATUS_OPTIONS, default=[])
    payment_filter = st.multiselect("Filter Pembayaran Ongkir", PAYMENT_OPTIONS, default=[])

    filtered = df.copy()

    if keyword:
        keyword_lower = keyword.lower()
        filtered = filtered[
            filtered.apply(
                lambda row: keyword_lower in " ".join(row.astype(str).str.lower().tolist()),
                axis=1
            )
        ]

    if status_filter:
        filtered = filtered[filtered["status_pengantaran"].isin(status_filter)]

    if payment_filter:
        filtered = filtered[filtered["status_pembayaran_ongkir"].isin(payment_filter)]

    st.write(f"Jumlah data ditemukan: **{len(filtered)}**")

    if filtered.empty:
        st.warning("Data tidak ditemukan.")
    else:
        for _, row in filtered.sort_values("updated_at", ascending=False).iterrows():
            with st.container(border=True):
                top1, top2, top3 = st.columns([2, 1, 1])
                with top1:
                    st.markdown(f"### {row['order_id']} - {row['nama_pelanggan']}")
                    st.caption(f"Terakhir diperbarui: {row['updated_at']}")
                with top2:
                    st.markdown(get_status_badge(row["status_pengantaran"]), unsafe_allow_html=True)
                with top3:
                    st.markdown(get_payment_badge(row["status_pembayaran_ongkir"]), unsafe_allow_html=True)

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.write("**Tanggal:**", row["tanggal"])
                    st.write("**No. HP:**", row["no_hp"])
                    st.write("**Menu:**", row["menu_pesanan"])
                    st.write("**Jumlah:**", row["jumlah"])
                with c2:
                    st.write("**Alamat:**", row["alamat_pengantaran"])
                    st.write("**Kurir:**", row["nama_kurir"])
                    st.write("**Metode Kurir:**", row["metode_kurir"])
                    st.write("**Estimasi Sampai:**", row["estimasi_sampai"])
                with c3:
                    st.write("**Total Pesanan:**", rupiah(row["total_pesanan"]))
                    st.write("**Ongkir:**", rupiah(row["ongkir"]))
                    st.write("**Total Bayar + Ongkir:**", rupiah(row["total_pesanan"] + row["ongkir"]))
                    st.write("**Catatan:**", row["catatan"])


# =========================
# PAGE: UPDATE STATUS
# =========================
elif page == "Update Status":
    st.markdown("## ✏️ Update Status Pesanan")
    st.caption("Admin/owner dapat mengubah status pengantaran dan status pembayaran ongkir.")

    if df.empty:
        st.info("Belum ada data pesanan.")
    else:
        selected_order = st.selectbox(
            "Pilih Order ID",
            df.sort_values("updated_at", ascending=False)["order_id"].tolist()
        )

        order_data = df[df["order_id"] == selected_order].iloc[0]

        with st.container(border=True):
            st.markdown(f"### Detail Saat Ini: {selected_order}")
            st.write("**Nama Pelanggan:**", order_data["nama_pelanggan"])
            st.write("**Menu:**", order_data["menu_pesanan"])
            st.write("**Jumlah:**", order_data["jumlah"])
            st.write("**Total Pesanan:**", rupiah(order_data["total_pesanan"]))
            st.write("**Ongkir:**", rupiah(order_data["ongkir"]))
            st.write("**Status Pengantaran:**", order_data["status_pengantaran"])
            st.write("**Status Pembayaran Ongkir:**", order_data["status_pembayaran_ongkir"])

        with st.form("form_update_status"):
            c1, c2 = st.columns(2)

            with c1:
                new_status = st.selectbox(
                    "Update Status Pengantaran",
                    STATUS_OPTIONS,
                    index=STATUS_OPTIONS.index(order_data["status_pengantaran"])
                    if order_data["status_pengantaran"] in STATUS_OPTIONS else 0
                )
                new_payment = st.selectbox(
                    "Update Status Pembayaran Ongkir",
                    PAYMENT_OPTIONS,
                    index=PAYMENT_OPTIONS.index(order_data["status_pembayaran_ongkir"])
                    if order_data["status_pembayaran_ongkir"] in PAYMENT_OPTIONS else 0
                )
                new_eta = st.text_input("Update Estimasi Sampai", value=str(order_data["estimasi_sampai"]))

            with c2:
                new_courier_method = st.selectbox(
                    "Metode Kurir",
                    COURIER_OPTIONS,
                    index=COURIER_OPTIONS.index(order_data["metode_kurir"])
                    if order_data["metode_kurir"] in COURIER_OPTIONS else 0
                )
                new_courier = st.text_input("Nama Kurir", value=str(order_data["nama_kurir"]))
                new_notes = st.text_area("Catatan", value=str(order_data["catatan"]))

            update_btn = st.form_submit_button("Simpan Perubahan", type="primary", use_container_width=True)

            if update_btn:
                success = update_order(
                    selected_order,
                    {
                        "status_pengantaran": new_status,
                        "status_pembayaran_ongkir": new_payment,
                        "estimasi_sampai": new_eta,
                        "metode_kurir": new_courier_method,
                        "nama_kurir": new_courier,
                        "catatan": new_notes,
                    }
                )
                if success:
                    st.success("Status pesanan berhasil diperbarui.")
                    st.rerun()
                else:
                    st.error("Order ID tidak ditemukan.")

        st.divider()
        st.markdown("### Hapus Data Pesanan")
        st.warning("Gunakan fitur ini hanya jika data salah input.")
        confirm_delete = st.checkbox(f"Saya yakin ingin menghapus {selected_order}")
        if confirm_delete:
            if st.button("Hapus Pesanan", type="secondary"):
                delete_order(selected_order)
                st.success("Data pesanan berhasil dihapus.")
                st.rerun()


# =========================
# PAGE: DATA & EXPORT
# =========================
elif page == "Data & Export":
    st.markdown("## 📦 Data & Export")
    st.caption("Gunakan halaman ini untuk melihat, mengedit langsung, dan mengunduh data pesanan.")

    st.markdown("### Tabel Data Pesanan")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "status_pengantaran": st.column_config.SelectboxColumn(
                "status_pengantaran",
                options=STATUS_OPTIONS,
                required=True
            ),
            "status_pembayaran_ongkir": st.column_config.SelectboxColumn(
                "status_pembayaran_ongkir",
                options=PAYMENT_OPTIONS,
                required=True
            ),
            "metode_kurir": st.column_config.SelectboxColumn(
                "metode_kurir",
                options=COURIER_OPTIONS,
                required=True
            ),
            "total_pesanan": st.column_config.NumberColumn(
                "total_pesanan",
                format="Rp %d"
            ),
            "ongkir": st.column_config.NumberColumn(
                "ongkir",
                format="Rp %d"
            ),
        }
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Simpan Perubahan Tabel", type="primary", use_container_width=True):
            edited_df["updated_at"] = now_string()
            save_data(edited_df)
            st.success("Perubahan tabel berhasil disimpan.")
            st.rerun()

    with c2:
        st.download_button(
            "Download CSV",
            data=make_csv_download(df),
            file_name="ayam_nyakot_tracking.csv",
            mime="text/csv",
            use_container_width=True
        )

    with c3:
        st.download_button(
            "Download Excel",
            data=make_excel_download(df),
            file_name="ayam_nyakot_tracking.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.info(
        "Catatan: Versi ini cocok untuk demo project dan penggunaan sederhana. "
        "Untuk penggunaan jangka panjang, data sebaiknya disimpan di database online seperti Google Sheets, Firebase, Supabase, atau PostgreSQL."
    )