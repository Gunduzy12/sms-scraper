import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import threading
import time
import os
import sys
import pandas as pd

# Pillow ile logo desteği
from PIL import Image, ImageTk

try:
    import ttkbootstrap as tb
    bootstrap_available = True
except ImportError:
    from ttkthemes import ThemedTk
    bootstrap_available = False

from scraper import scrape_Maps
from exporter import save_to_excel
from messenger import send_whatsapp_messages
from hwid_lock import enforce_hwid, load_allowed

# Dosyanın bulunduğu dizini dinamik olarak al
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# HWID kontrolü artık dosya yolunu dinamik olarak buluyor
enforce_hwid(load_allowed(resource_path("allowed_hwids.txt")))

ICON_WHATSAPP = "\U0001F4AC"    # 💬
ICON_FILE = "\U0001F4C4"       # 📄
ICON_EXCEL = "\U0001F4C8"      # 📊
ICON_SEARCH = "\U0001F50D"     # 🔍
ICON_DONE = "\u2714"           # ✔️
ICON_LOADING = "\u23F3"        # ⏳
ICON_ERROR = "\u26A0"          # ⚠️
ICON_SEND = "\u27A1"           # ➡

def scraping_yap(sektor, sehir, mesaj, file_paths, log_func, update_listbox_func, update_status_func):
    update_status_func(f"{ICON_LOADING} {sektor} - {sehir} için scraping başlıyor...")
    log_func(f"{sektor} - {sehir} için scraping başlıyor...\n")
    try:
        data, _ = scrape_Maps(sektor, sehir)
        if data:
            update_status_func(f"{ICON_DONE} {len(data)} adet veri çekildi, Excel'e kaydediliyor...")
            log_func(f"{len(data)} adet veri çekildi.\n")
            save_to_excel(data, "output_gui.xlsx")
            log_func(f"Veriler Excel'e kaydedildi: output_gui.xlsx\n")
            update_listbox_func(data)
            update_status_func(f"{ICON_WHATSAPP} WhatsApp mesajları gönderiliyor...")
            if file_paths:
                log_func(f"Dosyalarla gönderiliyor: {file_paths}\n")
            else:
                log_func("Dosya olmadan gönderiliyor\n")
            send_whatsapp_messages(data, mesaj, file_paths, log_func)

            log_func("WhatsApp mesajları gönderildi!\n")
            update_status_func(f"{ICON_DONE} İşlem tamamlandı!")
        else:
            update_status_func(f"{ICON_ERROR} Hiç veri bulunamadı!")
            log_func("Hiç veri bulunamadı!\n")
    except Exception as e:
        update_status_func(f"{ICON_ERROR} Hata oluştu: {e}")
        log_func(f"Hata oluştu: {e}\n")
    log_func("Scraping bitti!\n")

    update_status_func(f"{ICON_LOADING} {sektor} - {sehir} için scraping başlıyor...")
    log_func(f"{sektor} - {sehir} için scraping başlıyor...\n")
    try:
        data, _ = scrape_Maps(sektor, sehir)
        if data:
            update_status_func(f"{ICON_DONE} {len(data)} adet veri çekildi, Excel'e kaydediliyor...")
            log_func(f"{len(data)} adet veri çekildi.\n")
            save_to_excel(data, "output_gui.xlsx")
            log_func(f"Veriler Excel'e kaydedildi: output_gui.xlsx\n")
            update_listbox_func(data)
            update_status_func(f"{ICON_WHATSAPP} WhatsApp mesajları gönderiliyor...")
            if file_paths:
                log_func(f"Dosyalarla gönderiliyor: {file_paths}\n")
            else:
                log_func("Dosya olmadan gönderiliyor\n")
            send_whatsapp_messages(data, mesaj, file_paths, log_func)

            log_func("WhatsApp mesajları gönderildi!\n")
            update_status_func(f"{ICON_DONE} İşlem tamamlandı!")
        else:
            update_status_func(f"{ICON_ERROR} Hiç veri bulunamadı!")
            log_func("Hiç veri bulunamadı!\n")
    except Exception as e:
        update_status_func(f"{ICON_ERROR} Hata oluştu: {e}")
        log_func(f"Hata oluştu: {e}\n")
    log_func("Scraping bitti!\n")


def excel_mesaj_gonder(excel_file_path, mesaj, file_paths, log_func, update_listbox_func, update_status_func):
    if not excel_file_path:
        log_func(f"{ICON_ERROR} Lütfen bir Excel dosyası seçin.\n")
        update_status_func(f"{ICON_ERROR} Hata: Excel dosyası seçilmedi.")
        return

    update_status_func(f"{ICON_LOADING} Excel dosyası okunuyor: {os.path.basename(excel_file_path)}...")
    log_func(f"Excel dosyasından veriler okunuyor: {os.path.basename(excel_file_path)}\n")
    
    try:
        df = pd.read_excel(excel_file_path)
        data = df.to_dict('records')
        
        if not data:
            log_func(f"{ICON_ERROR} Excel dosyasında veri bulunamadı.\n")
            update_status_func(f"{ICON_ERROR} Hata: Excel dosyası boş.")
            return

        update_status_func(f"{ICON_DONE} {len(data)} adet numara okundu, mesajlar gönderiliyor...")
        log_func(f"{len(data)} adet numara okundu.\n")
        update_listbox_func(data)
        
        send_whatsapp_messages(data, mesaj, file_paths, log_func)

        
        log_func("WhatsApp mesajları Excel listesine gönderildi!\n")
        update_status_func(f"{ICON_DONE} Toplu mesaj gönderimi tamamlandı!")

    except Exception as e:
        log_func(f"{ICON_ERROR} Hata oluştu: Excel dosyası okunamadı veya gönderim başarısız oldu. Hata: {e}\n")
        update_status_func(f"{ICON_ERROR} Hata oluştu: {e}")

class ToolTip:
    # Basit tooltip desteği
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + cy + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#23272E", foreground="#00C853",
                         font=("Segoe UI", 10), borderwidth=2, relief="solid", padx=8, pady=4)
        label.pack()

    def hide(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class App:
    def __init__(self):
        if bootstrap_available:
            self.win = tb.Window(themename="darkly")
            self.root = self.win
            self.style = tb.Style()
            self.root.title("GoogleMaps Whatsapp Otomasyonu | Yusuf Gündüz")
        else:
            self.win = ThemedTk(theme="equilux")
            self.root = self.win
            self.root.title("GoogleMaps Whatsapp Otomasyonu | Yusuf Gündüz")
            self.root.set_theme("equilux")
            self.style = ttk.Style(self.win)
            self.style.theme_use("equilux")

        self.root.geometry("1200x670")
        self.root.resizable(False, False)

        self.bg_color = "#23272E"
        self.fg_color = "#F8F8F2"
        self.accent_color = "#00C853"
        self.accent_dark = "#008744"
        self.frame_bg = "#2A2E37"
        self.text_bg = "#23272E"
        self.text_fg = "#F8F8F2"
        self.border_color = "#44475A"

        if not bootstrap_available:
            self.root.configure(bg=self.bg_color)
            self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 12))
            self.style.configure("TFrame", background=self.bg_color)
            self.style.configure("TNotebook", background=self.bg_color, borderwidth=0)
            self.style.configure("TNotebook.Tab", background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 13, "bold"), padding=[12, 7])
            self.style.map("TNotebook.Tab", background=[("selected", self.accent_dark)], foreground=[("selected", self.fg_color)])
            self.style.configure("Modern.TLabelframe", background=self.frame_bg, borderwidth=2, relief="flat", labeloutside=True)
            self.style.configure("Modern.TLabelframe.Label", background=self.frame_bg, foreground=self.accent_color, font=("Segoe UI", 15, "bold"))
            self.style.configure("TEntry", fieldbackground=self.text_bg, foreground=self.text_fg, borderwidth=2, relief="flat")
            self.style.configure("Accent.TButton",
                                 background=self.accent_color,
                                 foreground=self.fg_color,
                                 font=("Segoe UI", 12, "bold"),
                                 borderwidth=0,
                                 focusthickness=0,
                                 relief="flat",
                                 padding=10)
            self.style.map("Accent.TButton",
                           background=[("active", self.accent_dark), ("pressed", self.accent_dark)],
                           foreground=[("active", self.fg_color)])

        self.timer_running = False
        self.timer_seconds = 0
        self.timer_thread = None
        self.selected_file_paths = []
        self.selected_excel_path = None

        # LOGO/AVATAR/BAŞLIK
        logo_frame = ttk.Frame(self.root)
        logo_frame.place(x=20, y=10, width=1160, height=60)

      
        logo_path = resource_path("logo.png") 
        try:
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((56, 56), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_img_label = tk.Label(logo_frame, image=self.logo_photo, bg=self.bg_color)
            logo_img_label.pack(side="left", padx=(10, 16), pady=2)
        except Exception as e:
            print(f"Logo yüklenemedi: {e}")
            logo_img_label = tk.Label(logo_frame, text="YG", font=("Segoe UI", 22, "bold"),
                                     bg=self.bg_color, fg=self.accent_color)
            logo_img_label.pack(side="left", padx=(10, 16), pady=2)

        logo_label = tk.Label(
            logo_frame,
            text="YUSUF GÜNDÜZ YAZILIM | Gündüz Scraper & WhatsApp Otomasyon",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg_color, fg=self.accent_color
        )
        logo_label.pack(side="left", padx=10, pady=10)

        # SEKME PANELİ
        notebook = ttk.Notebook(self.root)
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        notebook.add(tab1, text=f"{ICON_SEARCH} Harita Tarama")
        notebook.add(tab2, text=f"{ICON_WHATSAPP} Whatsapp Mesaj Gönderme")
        notebook.place(x=20, y=80, width=1160, height=570)

        # TAB 1: SCRAPING VE GÖNDERİM
        # SOL PANEL
        frame_left = ttk.LabelFrame(tab1, text="Çıkan Sonuçlar", style="Modern.TLabelframe")
        frame_left.place(x=20, y=20, width=260, height=320)

        ttk.Label(frame_left, text="Sektör:", font=("Segoe UI", 12, "bold")).pack(anchor='w', padx=14, pady=(14, 0))
        self.entry_sector = ttk.Entry(frame_left, font=("Segoe UI", 12), justify='center')
        self.entry_sector.pack(fill='x', padx=14, pady=6)
        ToolTip(self.entry_sector, "Aranacak sektör/iş kolu")

        ttk.Label(frame_left, text="Şehir:", font=("Segoe UI", 12, "bold")).pack(anchor='w', padx=14, pady=(14, 0))
        self.entry_city = ttk.Entry(frame_left, font=("Segoe UI", 12), justify='center')
        self.entry_city.pack(fill='x', padx=14, pady=6)
        ToolTip(self.entry_city, "Aranacak şehir")

        ttk.Label(frame_left, text="Sonuçlar:", font=("Segoe UI", 12, "bold")).pack(anchor='w', padx=14, pady=(18, 0))
        self.listbox = tk.Listbox(frame_left, bg=self.text_bg, fg=self.text_fg, selectbackground=self.accent_color,
                                 selectforeground=self.fg_color, borderwidth=2, highlightthickness=3, highlightcolor=self.border_color,
                                 font=("Segoe UI", 11), relief="flat")
        self.listbox.pack(fill='both', expand=True, padx=14, pady=10)

        # ORTA PANEL
        frame_mid = ttk.LabelFrame(tab1, text="İşlemler", style="Modern.TLabelframe")
        frame_mid.place(x=300, y=20, width=220, height=320)
        btn_scrape = ttk.Button(frame_mid, text=f"{ICON_SEARCH} Harita Üzerinde Başlat", command=self.thread_scraping, style="Accent.TButton")
        btn_scrape.pack(fill='x', pady=16)
        ToolTip(btn_scrape, "Google Maps'ten veri çekmeye başla")

        btn_test = ttk.Button(frame_mid, text=f"{ICON_WHATSAPP} Whatsapp Gönderme Testi", command=self.dummy_func, style="Accent.TButton")
        btn_test.pack(fill='x', pady=16)
        ToolTip(btn_test, "Whatsapp mesaj gönderimini test et")

        btn_attack = ttk.Button(frame_mid, text="🛡️ Topçular Saldır", command=self.dummy_func, style="Accent.TButton")
        btn_attack.pack(fill='x', pady=16)
        ToolTip(btn_attack, "Özel bir fonksiyon. İstersen burada geliştirme yap.")

        btn_param = ttk.Button(frame_mid, text="⚙️ Parametre Çık", command=self.dummy_func, style="Accent.TButton")
        btn_param.pack(fill='x', pady=16)
        ToolTip(btn_param, "Parametreleri dışa aktar.")

        # MESAJ PANELİ
        frame_msg = ttk.LabelFrame(tab1, text="Gönderilecek Mesaj", style="Modern.TLabelframe")
        frame_msg.place(x=540, y=20, width=410, height=320)
        frame_file = ttk.Frame(frame_msg)
        frame_file.pack(fill='x', padx=16, pady=12)
        self.text_message = tk.Text(frame_msg, height=9, width=45, bg=self.text_bg, fg=self.text_fg,
                                 insertbackground=self.fg_color, borderwidth=2, relief="flat",
                                 highlightthickness=2, highlightcolor=self.accent_color,
                                 font=("Segoe UI", 11))
        self.text_message.pack(fill='both', expand=True, padx=16, pady=10)
        ToolTip(self.text_message, "Gönderilecek Whatsapp mesajını buraya yaz")

        # DURUM PANELİ
        frame_status = ttk.LabelFrame(tab1, text="Durum", style="Modern.TLabelframe")
        frame_status.place(x=970, y=20, width=160, height=320)
        ttk.Label(frame_status, text="Son Durum:", font=("Segoe UI", 12, "bold")).pack(anchor='w', padx=16, pady=(16, 0))
        self.status_label = ttk.Label(frame_status, text="Bekliyor...", font=("Segoe UI", 14, "bold"), foreground=self.accent_color)
        self.status_label.pack(anchor='w', padx=16, pady=10)
        self.status_label2 = ttk.Label(frame_status, text="", font=("Segoe UI", 11, "italic"))
        self.status_label2.pack(anchor='w', padx=16, pady=6)
        ttk.Label(frame_status, text="Zaman", font=("Segoe UI", 12, "bold")).pack(anchor='w', padx=16, pady=(32, 0))
        self.timer_label = ttk.Label(frame_status, text="00:00:00", font=("Segoe UI", 15, "bold"), foreground=self.accent_color)
        self.timer_label.pack(anchor='w', padx=16, pady=12)

        # LOG PANELİ
        frame_log = ttk.LabelFrame(tab1, text="Log", style="Modern.TLabelframe")
        frame_log.place(x=20, y=360, width=1110, height=180)
        self.text_log = tk.Text(frame_log, height=6, bg=self.text_bg, fg="#B7B7B7", insertbackground="#B7B7B7",
                                 borderwidth=2, relief="flat", highlightthickness=2, highlightcolor=self.accent_color,
                                 font=("Consolas", 11))
        self.text_log.pack(fill='both', expand=True, padx=14, pady=12)
        ToolTip(self.text_log, "Sistem logu ve uyarılar burada gösterilir")


        # TAB 2: EXCEL'DEN TOPLU MESAJ GÖNDERME
        frame_excel = ttk.LabelFrame(tab2, text="Excel'den Toplu Gönderim", style="Modern.TLabelframe")
        frame_excel.place(x=20, y=20, width=410, height=320)

        ttk.Label(frame_excel, text="1. Excel Dosyası Seçin:", font=("Segoe UI", 12, "bold")).pack(anchor='w', padx=16, pady=(16, 0))
        btn_select_excel = ttk.Button(frame_excel, text=f"{ICON_EXCEL} EXCEL DOSYASI SEÇ", command=self.dosya_sec_excel, style="Accent.TButton")
        btn_select_excel.pack(fill='x', padx=16, pady=6)
        ToolTip(btn_select_excel, "Telefon numaralarını içeren Excel dosyasını seçin")

        self.label_excel_path = ttk.Label(frame_excel, text="❌ Henüz bir Excel dosyası seçilmedi", font=("Segoe UI", 10, "italic"), foreground="#FF5555", background=self.frame_bg)
        self.label_excel_path.pack(anchor='w', padx=16, pady=(0, 16))

        ttk.Label(frame_excel, text="2. Mesajınızı Girin:", font=("Segoe UI", 12, "bold")).pack(anchor='w', padx=16)
        self.text_message_excel = tk.Text(frame_excel, height=5, width=45, bg=self.text_bg, fg=self.text_fg,
                                         insertbackground=self.fg_color, borderwidth=2, relief="flat",
                                         highlightthickness=2, highlightcolor=self.accent_color,
                                         font=("Segoe UI", 11))
        self.text_message_excel.pack(fill='both', expand=True, padx=16, pady=10)
        ToolTip(self.text_message_excel, "Gönderilecek mesajı buraya yazın ({isim} ile isim ekleyebilirsiniz)")

        
        btn_send_excel = ttk.Button(tab2, text=f"{ICON_SEND} EXCEL LİSTESİNE GÖNDER", command=self.thread_excel_send, style="Accent.TButton")
        btn_send_excel.place(x=20, y=360, width=410)
        ToolTip(btn_send_excel, "Seçili Excel dosyasındaki tüm numaralara mesajları gönder")
        
    def log_yaz(self, mesaj):
        self.text_log.insert(tk.END, mesaj)
        self.text_log.see(tk.END)
        self.root.update_idletasks()

    def update_listbox(self, data):
        self.listbox.delete(0, tk.END)
        for row in data:
            text = f"{row.get('İsim','') if row.get('İsim','') else ''} | {row.get('Telefon','')}"
            self.listbox.insert(tk.END, text)

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def update_timer(self):
        while self.timer_running:
            mins, secs = divmod(self.timer_seconds, 60)
            hours, mins = divmod(mins, 60)
            self.timer_label.config(text=f"{hours:02}:{mins:02}:{secs:02}")
            self.timer_seconds += 1
            time.sleep(1)

    def start_timer(self):
        self.timer_running = True
        self.timer_thread = threading.Thread(target=self.update_timer)
        self.timer_thread.daemon = True
        self.timer_thread.start()

    def stop_timer(self):
        self.timer_running = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1)

    

    def dosya_sec_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Dosyaları", "*.xlsx *.xls")])
        if file_path:
            self.selected_excel_path = file_path
            self.label_excel_path.config(text=os.path.basename(file_path), foreground=self.accent_color)
        else:
            self.selected_excel_path = None
            self.label_excel_path.config(text="❌ Henüz bir Excel dosyası seçilmedi", foreground="#FF5555")

    def thread_scraping(self):
        sektor = self.entry_sector.get().strip()
        sehir = self.entry_city.get().strip()
        mesaj = self.text_message.get("1.0", tk.END).strip()
        if not sektor or not sehir:
            self.log_yaz(f"{ICON_ERROR} Sektör ve şehir alanları boş bırakılamaz!\n")
            self.update_status(f"{ICON_ERROR} Hata: Sektör ve şehir alanları boş bırakılamaz.")
            return
        self.stop_timer()
        self.timer_seconds = 0
        self.start_timer()
        self.update_status(f"{ICON_LOADING} İşlem başlatıldı...")
        self.scraping_thread = threading.Thread(target=scraping_yap,
                                                 args=(sektor, sehir, mesaj, self.selected_file_paths,
                                                       self.log_yaz, self.update_listbox,
                                                       self.update_status))
        self.scraping_thread.start()
        
    def thread_excel_send(self):
        mesaj = self.text_message_excel.get("1.0", tk.END).strip()
        if not self.selected_excel_path:
            self.log_yaz(f"{ICON_ERROR} Lütfen önce bir Excel dosyası seçin!\n")
            self.update_status(f"{ICON_ERROR} Hata: Excel dosyası seçilmedi.")
            return
        if not mesaj:
            self.log_yaz(f"{ICON_ERROR} Gönderilecek mesaj boş bırakılamaz!\n")
            self.update_status(f"{ICON_ERROR} Hata: Mesaj boş.")
            return
            
        self.stop_timer()
        self.timer_seconds = 0
        self.start_timer()
        self.update_status(f"{ICON_LOADING} Excel'den gönderim başlıyor...")
        self.excel_thread = threading.Thread(target=excel_mesaj_gonder,
                                             args=(self.selected_excel_path, mesaj, self.selected_file_paths,
                                                   self.log_yaz, self.update_listbox,
                                                   self.update_status))
        self.excel_thread.start()

    def dummy_func(self):
        self.log_yaz(f"{ICON_DONE} Bu butona basıldı!\n")

if __name__ == "__main__":
    app = App()
    app.root.mainloop()