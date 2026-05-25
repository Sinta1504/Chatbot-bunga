# Data stok dan harga bunga
DAFTAR_BUNGA = {
    "mawar": 50000,
    "tulip": 75000,
    "melati": 30000
}

def dapatkan_daftar_harga():
    teks = "Daftar harga bunga kami:\n"
    for bunga, harga in DAFTAR_BUNGA.items():
        teks += f"- {bunga.capitalize()}: Rp {harga:,}/tangkai\n"
    return teks

def hitung_total(nama_bunga, jumlah):
    bunga_lower = nama_bunga.lower()
    if bunga_lower in DAFTAR_BUNGA:
        total = DAFTAR_BUNGA[bunga_lower] * jumlah
        return total
    return 0