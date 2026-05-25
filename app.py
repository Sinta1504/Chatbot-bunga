import streamlit as st
import FSM
import engine

# Mengatur tata letak halaman Streamlit menjadi "wide" (lebar) agar pas untuk 2 kolom
st.set_page_config(layout="wide")

st.title("🌸 Flower Store Chatbot")
st.write("Selamat datang di Toko Bunga! Silakan pesan bunga melalui chatbot di bawah.")

# 1. Inisialisasi State Session jika belum ada
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_state" not in st.session_state:
    st.session_state.chat_state = "MENU_UTAMA"
if "session_data" not in st.session_state:
    st.session_state.session_data = {}

# ------------------------------------------------------------------
# 2. MEMBUAT TAMPILAN SPLIT (KOLOM KIRI & KOLOM KANAN)
# ------------------------------------------------------------------
kolom_kiri, kolom_kanan = st.columns([3, 2]) # Rasio lebar kolom kiri : kanan = 3 : 2

# === KELOLA KOLOM KIRI (Chatbot Utama) ===
with kolom_kiri:
    st.subheader("💬 Chat dengan Bot")
    
    # Bungkus riwayat chat di dalam container agar rapi
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Handle input dari user baru
    if user_input := st.chat_input("Ketik pesan Anda di sini..."):
        # Tampilkan pesan user ke UI
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Panggil FSM untuk memproses input
        bot_response, next_state, updated_data = FSM.proses_fsm(
            user_input, 
            st.session_state.chat_state, 
            st.session_state.session_data
        )
        
        # Update status state dan data
        st.session_state.chat_state = next_state
        st.session_state.session_data = updated_data
        
        # Tampilkan respons bot ke UI
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Memaksa halaman untuk merender ulang agar kolom kanan langsung ter-update
        st.rerun()


# === KELOLA KOLOM KANAN (Menu Toko & Real-time Keranjang) ===
with kolom_kanan:
    # --- Bagian Atas: Daftar Menu Toko ---
    st.subheader("📋 Daftar Menu Bunga")
    for bunga, harga in engine.DAFTAR_BUNGA.items():
        st.info(f"**{bunga.capitalize()}** \n\n Harga: Rp {harga:,} / tangkai")
    
    st.write("---")
    
    # --- Bagian Bawah: Ringkasan Keranjang / Nota Sementara ---
    st.subheader("🛒 Keranjang Belanja Anda")
    
    data_saat_ini = st.session_state.session_data
    state_saat_ini = st.session_state.chat_state
    
    # Cek apakah user sedang berada di proses transaksi
    if "bunga_dipilih" in data_saat_ini:
        bunga = data_saat_ini["bunga_dipilih"].capitalize()
        
        st.warning(f"⏳ **Status Pemesanan:** Sedang memproses bunga **{bunga}**")
        
        # Buat visualisasi struk sementara jika jumlahnya nanti dimasukkan lewat chat
        st.markdown(f"""
        | Item | Detail |
        | :--- | :--- |
        | **Produk** | {bunga} |
        | **Status** | Menunggu input jumlah tangkai di chat... |
        """)
        
    else:
        st.success("🛒 Keranjang kosong atau transaksi terakhir telah selesai dilakukan. Silakan ketik 'beli' di chatbot untuk mulai memesan.")