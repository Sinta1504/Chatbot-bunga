import re

# Buat Object Engine
class Engine:
    def __init__(self):
        # Array Menu
        self.menu_data = {
            'mawar': {'price': '15000', 'desc': 'Bunga Mawar segar', 'emoji': '🌹'},
            'melati': {'price': '12000', 'desc': 'Bunga Melati harum', 'emoji': '🌼'},
            'tulip': {'price': '20000', 'desc': 'Bunga Tulip warna-warni', 'emoji': '🌷'},
            'anggrek': {'price': '25000', 'desc': 'Bunga Anggrek eksotis', 'emoji': '🪷'},
        }
        # Regex Patterns
        self.re_number = r"\b(\d+)\b"  # Untuk mencari angka dalam kalimat
        menu_keys = "|".join(self.menu_data.keys())
        self.re_menu = rf"\b({menu_keys})\b"
        self.re_split = r"[,.]|\bdan\b|\b&\b"  # Pemisah kalimat
        self.re_cancel_all = r"\b(batalkan semua|hapus semua|reset keranjang|kosongkan)\b"
        self.re_reduce = r"\b(batalkan|kurangi|tidak jadi|hapus|cancel)\b"

    def _parse_single_segment(self, text):
        text = text.lower().strip()
        item_match = re.search(self.re_menu, text)
        if not item_match:
            return None
        item_key = item_match.group(1)
        qty_match = re.search(self.re_number, text)
        qty = int(qty_match.group(1)) if qty_match else 1
        return {
            'item': item_key,
            'qty': qty,
            'price': self.menu_data[item_key]['price'],
            'emoji': self.menu_data[item_key]['emoji'],
        }

    def parse_orders(self, full_text):
        segments = re.split(self.re_split, full_text)
        found_orders = []
        for segment in segments:
            if segment.strip():
                order = self._parse_single_segment(segment)
                if order:
                    found_orders.append(order)
        return found_orders

    def detect_intent(self, text):
        text = text.lower()
        if re.search(r"\b(reset|ulang|batal semua)\b", text):
            return "RESET"
        if re.search(self.re_cancel_all, text):
            return "CANCEL_ALL"
        if re.search(self.re_reduce, text):
            return "REDUCE_ITEM"
        if re.search(r"\b(menu|daftar|apa saja|jual apa|list)\b", text):
            return "ASK_MENU"
        if re.search(r"\b(selesai|bayar|checkout|cukup)\b", text):
            return "CHEECKOUT"
        if re.search(r"\b(ya|yes|oke|betul|siap|baik)\b", text):
            return "YES"
        if re.search(r"\b(tidak|enggak|batal|no|salah)\b", text):
            return "NO"
        return "UNKNOW"

    def print_menu(self):
        for item, info in self.menu_data.items():
            print(f"{item.title()} ({info['emoji']}): {info['desc']} - Rp{info['price']}")