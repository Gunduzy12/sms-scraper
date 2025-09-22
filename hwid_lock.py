
import os, sys, uuid, hashlib
from typing import Set

def get_hwid() -> str:
    """
    Cihazın kimliğini üret: MAC tabanlı ve sabit bir hash.
    """
    mac = uuid.getnode()  # int
    return hashlib.sha256(str(mac).encode()).hexdigest().upper()

def load_allowed(file_path: str) -> Set[str]:
    """
    Belirtilen dosyadan yetkili HWID'leri yükle.
    Bu fonksiyon şimdi bir dosya yolu parametresi (file_path) alıyor.
    """
    print(f"Kontrol edilecek dosya yolu: {file_path}")
    allowed = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                v = line.strip().upper()
                if v:
                    allowed.add(v)
        print(f"Okunan HWID'ler: {allowed}")
    except FileNotFoundError:
        print(f"Hata: Dosya bulunamadı! {file_path}")
        
        pass
    return allowed

def enforce_hwid(allowed: Set[str]):
    """
    Eğer mevcut HWID, allowed listesinde değilse programı kapat.
    GUI varsa uyarı kutusu, yoksa print.
    """
    current = get_hwid()
    if current not in allowed:
        msg = (f"❌ Yetkisiz cihaz!\n"
               f"Bu cihazın HWID'i: {current}\n"
               f"Lütfen satıcıyla iletişime geçin.")
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk(); root.withdraw()
            messagebox.showerror("Yetkisiz Cihaz", msg)
        except Exception:
            print(msg)
        sys.exit(0)