import os
from scraper import scrape_Maps
from exporter import save_to_excel
from messenger import send_whatsapp_messages
from hwid_lock import enforce_hwid, load_allowed
enforce_hwid(load_allowed())

if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')

    keyword = input("Aranacak sektör/işletme türü: ")
    location = input("Şehir/Bölge: ")

    print("Veriler çekiliyor, lütfen bekleyin...")
    data = scrape_Maps(keyword, location)

    if data:
        save_to_excel(data, "data/output.xlsx")
        
       
        whatsapp_mesaji = input("WhatsApp'tan göndermek istediğiniz mesajı girin: ")
        
   
        send_whatsapp_messages(data, whatsapp_mesaji) 
    else:
        print("Hiçbir işletme verisi çekilemedi. İşlem sonlandırıldı.")