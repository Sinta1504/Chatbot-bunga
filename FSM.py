import engine  # <--- PASTIKAN INI ADA. Jika nama filenya Engine.py, ganti jadi 'import Engine'

def proses_fsm(user_input, current_state, session_data):
    input_lower = user_input.lower()
    response = ""
    next_state = current_state

    # STATE 1: MENU UTAMA / MENYAPA
    if current_state == "MENU_UTAMA":
        if "beli" in input_lower or "pesan" in input_lower:
            response = "Format pemesanan: Silakan ketik nama bunga yang ingin Anda beli.\n*(Pilihan: Mawar, Tulip, Melati)*"
            next_state = "MEMILIH_BUNGA"
        elif "harga" in input_lower or "menu" in input_lower:
            # Jika nama file Anda Engine.py, ganti 'engine' di bawah menjadi 'Engine'
            response = engine.dapatkan_daftar_harga() + "\nKetik 'beli' untuk mulai memesan."
        elif "halo" in input_lower or "hi" in input_lower:
            response = "Halo! Selamat datang di Toko Bunga. Ada yang bisa saya bantu? (Ketik 'harga' atau 'beli')"
        else:
            response = "Maaf, saya tidak mengerti. Coba ketik 'beli' atau 'harga'."

    # STATE 2: USER SEDANG MEMILIH BUNGA
    elif current_state == "MEMILIH_BUNGA":
        if input_lower in engine.DAFTAR_BUNGA:
            session_data["bunga_dipilih"] = input_lower
            response = f"Berapa tangkai bunga **{input_lower.capitalize()}** yang ingin Anda pesan? (Masukkan angka saja)"
            next_state = "MEMASUKKAN_JUMLAH"
        else:
            response = f"Bunga '{user_input}' tidak tersedia. Silakan pilih: Mawar, Tulip, atau Melati."

    # STATE 3: USER MEMASUKKAN JUMLAH PESANAN
    elif current_state == "MEMASUKKAN_JUMLAH":
        if user_input.isdigit() and int(user_input) > 0:
            jumlah = int(user_input)
            bunga = session_data["bunga_dipilih"]
            total_harga = engine.hitung_total(bunga, jumlah)
            
            response = (
                f"Pesanan Berhasil Dicatat! 🎉\n\n"
                f"Detail Pesanan:\n"
                f"- Bunga: {bunga.capitalize()}\n"
                f"- Jumlah: {jumlah} tangkai\n"
                f"- Total Pembayaran: **Rp {total_harga:,}**\n\n"
                f"Terima kasih telah berbelanja! Ketik 'menu' untuk kembali ke awal."
            )
            next_state = "MENU_UTAMA"
            session_data.clear()
        else:
            response = "Mohon masukkan jumlah dalam bentuk angka yang valid (contoh: 3)."

    return response, next_state, session_data