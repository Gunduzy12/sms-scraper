import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

def normalize_phone(phone):
    """Sadece rakamları al, karşılaştırma için son 10 haneyi kullan."""
    if not phone or phone in ("Bilgi Yok", ""):
        return ""
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) >= 10:
        return digits[-10:]  
    return digits

def scrape_Maps(sektor, sehir, wait_time=10, seen_records=None):
    """
    Döner: (data_list, seen_records_set)
    - seen_records: isteğe bağlı; pass edersen fonksiyon onu günceller (global dedup için kullan).
    """
    if seen_records is None:
        seen_records = set()

    data = []
    driver = webdriver.Chrome()
    driver.maximize_window()

    url = f"https://www.google.com/maps/search/{sektor}+{sehir}"
    driver.get(url)
    time.sleep(5)

    
    panel_selector = 'div[role="feed"]'
    try:
        scrollable_panel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, panel_selector))
        )
    except TimeoutException:
        
        scrollable_panel = driver.find_element(By.CSS_SELECTOR, panel_selector)

   
    print("Liste kaydırılıyor...")
    last_count = 0
    stable_rounds = 0
    while True:
        cards = driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc')
        count = len(cards)


        try:
            driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight;", scrollable_panel)
        except Exception:
           
            try:
                scrollable_panel.send_keys("\ue00f") 
            except Exception:
                pass

        time.sleep(random.uniform(1.5, 2.5))

        if count == last_count:
            stable_rounds += 1
        else:
            stable_rounds = 0
            last_count = count

        if stable_rounds >= 6:
            print(f"Listenin sonuna ulaşıldı, toplam kart: {len(cards)}")
            break

   
    business_cards = driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc')
    print(f"{len(business_cards)} işletme bulundu. Şimdi açılıyor...")

    prev_panel_name = ""
    prev_phone_norm = ""

    for i in range(len(business_cards)):
        try:
            business_cards = driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc')
            if i >= len(business_cards):
                break
            card = business_cards[i]

            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
            driver.execute_script("arguments[0].click();", card)
            print(f"[{i+1}] Kart tıklandı, detay bekleniyor...")

            try:
                prev_elem = driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf')
                prev_panel_name = prev_elem.text.strip()
            except Exception:
                prev_panel_name = ""

            def panel_updated(d):
                try:
                    el = d.find_element(By.CSS_SELECTOR, 'h1.DUwDvf')
                    txt = el.text.strip()

                    return txt != "" and txt != prev_panel_name
                except Exception:
                    return False

            try:
                WebDriverWait(driver, wait_time).until(panel_updated)
            except TimeoutException:

                pass

 
            try:
                name_elem = driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf')
                name = name_elem.text.strip()
            except Exception:
                name = "Bilgi Yok"

            phone = "Bilgi Yok"
            phone_norm = ""
            for attempt in range(3):
                try:

                    tel_link = driver.find_element(By.CSS_SELECTOR, 'a[href^="tel:"]')
                    phone = tel_link.get_attribute("href").replace("tel:", "").strip()
                except NoSuchElementException:

                    try:
                        divs = driver.find_elements(By.CSS_SELECTOR, 'div.Io6YTe')
                        found = False
                        for d in divs:
                            text = d.text.strip()
                            digits = ''.join(filter(str.isdigit, text))
                            if (text.startswith("0") or text.startswith("+")) and len(digits) >= 10:
                                phone = text
                                found = True
                                break
                        if not found:
                            phone = "Bilgi Yok"
                    except Exception:
                        phone = "Bilgi Yok"
                phone_norm = normalize_phone(phone)

                if phone_norm and phone_norm != prev_phone_norm:
                    break
                time.sleep(1 + attempt)

            prev_phone_norm = phone_norm

 
            key = (str(name).strip().lower(), phone_norm)

            if key not in seen_records and (phone_norm or name.strip()):
                seen_records.add(key)
                data.append({"Sektör": sektor, "İsim": name, "Telefon": phone})
                print(f"[{i+1}] Kayıt eklendi: {name} - {phone}")
            else:
                print(f"[{i+1}] {name} - {phone} (ZATEN VAR veya eksik, atlandı)")

        except StaleElementReferenceException:
            print(f"[{i+1}] StaleElementReference hatası, atlandı.")
            continue
        except Exception as e:
            print(f"[{i+1}] Hata: {e}")
            continue
        finally:
            time.sleep(random.uniform(3, 5))

    driver.quit()
    print(f"Toplam {len(data)} yeni işletme bilgisi çekildi.")
    return data, seen_records
