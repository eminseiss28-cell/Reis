import os
import requests
import json

# Ana kaynakların kök adresleri
KEKIK_BASE = "https://raw.githubusercontent.com/keyiflerolsun/Kekik-cloudstream/master"
PITIPITII_BASE = "https://raw.githubusercontent.com/sarapcanagii/Pitipitii/main"

with open('linkler.json', 'r', encoding='utf-8') as f:
    target_sites = json.load(f)

for site, url in target_sites.items():
    print(f"🛠️ {site} hazırlanıyor...")
    # Klasör yolunu senin kullanıcı adına (emin) göre ayarlar
    path = f"{site}/src/main/kotlin/com/emin"
    os.makedirs(path, exist_ok=True)

    # Denenecek muhtemel dosya yolları (Büyük/Küçük harf duyarlılığı için)
    sources = [
        f"{PITIPITII_BASE}/{site}/src/main/kotlin/com/pitipitii/{site}.kt",
        f"{PITIPITII_BASE}/{site}/src/main/kotlin/com/pitipitii/{site}Provider.kt",
        f"{KEKIK_BASE}/{site}/src/main/kotlin/com/kekik/{site}.kt",
        f"{KEKIK_BASE}/{site}/src/main/kotlin/com/kekik/{site}Provider.kt"
    ]

    success = False
    for src_url in sources:
        try:
            res = requests.get(src_url)
            if res.status_code == 200:
                code = res.text
                # Linkleri cerrahi müdahale ile değiştir
                code = code.replace('mainUrl = "', f'mainUrl = "{url}')
                code = code.replace('baseUrl = "', f'baseUrl = "{url}')
                # Paket ismini senin adına (com.emin) çevir ki TV'de çakışmasın
                code = code.replace('package com.pitipitii', 'package com.emin')
                code = code.replace('package com.kekik', 'package com.emin')
                
                with open(f"{path}/{site}Provider.kt", "w", encoding='utf-8') as f:
                    f.write(code)
                print(f"✅ {site} başarıyla kuruldu!")
                success = True
                break
        except:
            continue
    
    if not success:
        print(f"❌ {site} için kaynak kod bulunamadı! Linki veya ismi kontrol et.")
