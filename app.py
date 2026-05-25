import streamlit as st
from engine import Engine
# from st_pages import add_page_title

st.set_page_config(page_title="Flower Store Chatbot", page_icon=":seedling:", layout="centered")
# add_page_title()

st.markdown("""
<style>
body, .stApp {
    background-color: #f8f9fa;
    color: #222;
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
}
.stButton>button {
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    color: #222;
    padding: 0.5em 1.5em;
    font-size: 1.1em;
    transition: box-shadow 0.2s;
}
.stButton>button:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    border-color: #aaa;
}
.stTextInput>div>div>input {
    border-radius: 8px;
    border: 1px solid #ddd;
    padding: 0.5em 1em;
    font-size: 1.1em;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #222;
}
.menu-card {
    background: #fff;
    border: 1px solid #eee;
    border-radius: 10px;
    padding: 1em;
    margin-bottom: 1em;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    display: flex;
    align-items: center;
}
.menu-icon {
    width: 36px;
    height: 36px;
    margin-right: 1em;
}
</style>
""", unsafe_allow_html=True)

if 'engine' not in st.session_state:
    st.session_state['engine'] = Engine()

st.title('Flower Store Chatbot')
st.write('Selamat datang di Toko Bunga! Silakan pesan bunga dengan mengetik di bawah.')

user_input = st.text_input('Ketik pesan Anda di sini...')

if user_input:
    engine = st.session_state['engine']
    intent = engine.detect_intent(user_input)
    if intent == 'ASK_MENU':
        st.subheader('Menu Bunga')
        icons = {
            'mawar': 'https://cdn-icons-png.flaticon.com/512/616/616494.png',
            'melati': 'https://cdn-icons-png.flaticon.com/512/616/616492.png',
            'tulip': 'https://cdn-icons-png.flaticon.com/512/616/616495.png',
            'anggrek': 'https://cdn-icons-png.flaticon.com/512/616/616491.png',
        }
        for item, info in engine.menu_data.items():
            st.markdown(f"""
            <div class='menu-card'>
                <img src='{icons[item]}' class='menu-icon' />
                <div>
                    <b>{item.title()}</b><br>
                    <span style='color:#888'>{info['desc']}</span><br>
                    <b>Rp{info['price']}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
    elif intent == 'RESET' or intent == 'CANCEL_ALL':
        st.success('Keranjang telah dikosongkan.')
    elif intent == 'CHEECKOUT':
        st.success('Terima kasih atas pesanan Anda!')
    else:
        orders = engine.parse_orders(user_input)
        if orders:
            st.subheader('Pesanan Anda:')
            for order in orders:
                st.info(f"{order['qty']} x {order['item'].title()} (Rp{order['price']})")
        else:
            st.warning('Maaf, saya tidak mengerti. Coba lagi.')
