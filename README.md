# Google Maps Scraper

Bu proje, Google Haritalar üzerinden işletme bilgilerini çekerek Excel'e kaydeder ve isteğe bağlı olarak toplu WhatsApp mesajı gönderir.

## Gereksinimler

- Python 3.12 veya üzeri
- Google Chrome ve uygun ChromeDriver
- pip ile:
    - selenium
    - pandas
    - openpyxl
    - pywhatkit

## Kurulum

Gerekli kütüphaneleri yüklemek için:
```
python -m pip install selenium pandas openpyxl pywhatkit
```

ChromeDriver'ı [buradan](https://chromedriver.chromium.org/downloads) indirip, Chrome sürümüne uygun olanı proje klasörüne ekle.

## Kullanım
1. `main.py` dosyasını çalıştırın:
    ```
    python main.py
    ```
2. Aranacak işletme türü ve şehir girin (örn: "kuaför", "İstanbul")
3. Bilgiler çekilir, Excel'e yazılır ve WhatsApp mesajları gönderilir

WhatsApp mesajları için bilgisayarınızda WhatsApp Web'e giriş yapmış olmalısınız.

## Notlar

- Eğer telefon numarası çekilemiyorsa, Maps’in HTML yapısı değişmiş olabilir. Kodda XPATH’leri güncelleyerek çözebilirsiniz.
- Sıkıntı yaşarsanız, terminalde çıkan hata mesajını inceleyin veya destek alın.