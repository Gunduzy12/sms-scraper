import pywhatkit
import time
import os

def format_phone(phone):
    phone = str(phone).replace(" ", "").replace("-", "")
    if not phone.startswith("+"):
        if phone.startswith("0") and len(phone) == 11:
            phone = "+90" + phone[1:]
        elif len(phone) == 10: 
            phone = "+90" + phone
        elif phone.startswith("90") and len(phone) == 12:
            phone = "+" + phone
        elif phone.startswith("0090") and len(phone) == 13:
            phone = "+" + phone[2:]
        elif len(phone) == 12 and phone[:3] in ["+90", "+966", "+971", "+973", "+974", "+965", "+968", "+970",
        "+1", "+44", "+49", "+33", "+39", "+34", "+31", "+41", "+32",
        "+7", "+86", "+81", "+82", "+91", "+65", "+60", "+63", "+66",
        "+55", "+54", "+52", "+51", "+56", "+57", "+58"]:
            phone = "+" + phone  
    return phone


def send_whatsapp_messages(data, message, file_paths, log_func=print):
    
    allowed_country_codes = [
        "+90", "+966", "+971", "+973", "+974", "+965", "+968", "+970",
        "+1", "+44", "+49", "+33", "+39", "+34", "+31", "+41", "+32",
        "+7", "+86", "+81", "+82", "+91", "+65", "+60", "+63", "+66",
        "+55", "+54", "+52", "+51", "+56", "+57", "+58"
    ]
    
    delay_between_messages = 15
    sent_numbers = set()
    
    try:
        for i, entry in enumerate(data):
            raw_phone = entry.get("Telefon", "")
            phone = format_phone(raw_phone)

            is_valid_country_code = any(phone.startswith(code) for code in allowed_country_codes)

            if not is_valid_country_code or not phone[1:].isdigit():
                log_func(f"Geçersiz veya hatalı formatlı telefon numarası atlanıyor: {raw_phone}\n")
                continue

            if phone in sent_numbers:
                log_func(f"Bu numaraya ({phone}) daha önce mesaj gönderildiği için atlanıyor.\n")
                continue
                
            isim = entry.get("İsim", "Değerli Müşteri")
            custom_message = message.replace("{isim}", isim)
            
          
            if file_paths:
                log_func(f"{phone} numarasına dosya ve metin gönderiliyor...\n")
           
                try:
                   
                    file_path = file_paths[0]
                
                    file_path = os.path.abspath(file_path)
                    
               
                    pywhatkit.sendwhats_image(phone, file_path, custom_message, 15, True)
                    log_func(f"Dosya ve metin mesajı {phone} numarasına başarıyla gönderildi.\n")
                except Exception as e:
                    log_func(f"Dosya gönderirken hata oluştu: {e}. Sadece metin gönderiliyor...\n")
                    pywhatkit.sendwhatmsg_instantly(phone, custom_message)
                    log_func(f"Sadece metin mesajı {phone} numarasına başarıyla gönderildi.\n")
            else:
           
                log_func(f"{phone} numarasına anında metin mesajı gönderiliyor...\n")
                pywhatkit.sendwhatmsg_instantly(phone, custom_message)
                log_func(f"Metin mesajı {phone} numarasına başarıyla gönderildi.\n")

            sent_numbers.add(phone)
            log_func(f"⏳ Sonraki numara için {delay_between_messages} saniye bekleniyor...\n")
            time.sleep(delay_between_messages)

    except Exception as e:
        log_func(f"Hata oluştu: {e}\n")
    finally:
        log_func("Tüm işlemler tamamlandı. Lütfen tarayıcının kendi kendine kapanmasını bekleyin.\n")