import os, requests, json, re

# En sağlam kaynakların doğrudan raw linkleri
SOURCES = {
    "DiziPal": "https://raw.githubusercontent.com/sarapcanagii/Pitipitii/main/DiziPal/src/main/kotlin/com/pitipitii/DiziPal.kt",
    "InatBox": "https://raw.githubusercontent.com/sarapcanagii/Pitipitii/main/InatBox/src/main/kotlin/com/pitipitii/InatBox.kt",
    "FilmModu": "https://raw.githubusercontent.com/keyiflerolsun/Kekik-cloudstream/master/FilmModu/src/main/kotlin/com/kekik/FilmModu.kt",
    "FilmMakinesi": "https://raw.githubusercontent.com/keyiflerolsun/Kekik-cloudstream/master/FilmMakinesi/src/main/kotlin/com/kekik/FilmMakinesi.kt",
    "HDFilmCehennemi": "https://raw.githubusercontent.com/keyiflerolsun/Kekik-cloudstream/master/HDFilmCehennemi/src/main/kotlin/com/kekik/HDFilmCehennemi.kt",
    "Vavoo": "https://raw.githubusercontent.com/sarapcanagii/Pitipitii/main/Vavoo/src/main/kotlin/com/pitipitii/Vavoo.kt",
    "NeonSpor": "https://raw.githubusercontent.com/sarapcanagii/Pitipitii/main/NeonSpor/src/main/kotlin/com/pitipitii/NeonSpor.kt",
    "AnimeciX": "https://raw.githubusercontent.com/keyiflerolsun/Kekik-cloudstream/master/AnimeciX/src/main/kotlin/com/kekik/AnimeciX.kt"
}

with open('linkler.json', 'r', encoding='utf-8') as f:
    target_sites = json.load(f)

for site, url in target_sites.items():
    if site in SOURCES:
        print(f"🛠️ {site} kuruluyor...")
        path = f"{site}/src/main/kotlin/com/emin"
        os.makedirs(path, exist_ok=True)
        try:
            res = requests.get(SOURCES[site])
            if res.status_code == 200:
                code = res.text
                # Linkleri yerlestir
                code = code.replace('mainUrl = "', f'mainUrl = "{url}')
                code = code.replace('baseUrl = "', f'baseUrl = "{url}')
                # Paket ismini degistir (Kritik!)
                code = re.sub(r'package\s+com\.[a-zA-Z0-9\.]+', 'package com.emin', code)
                
                with open(f"{path}/{site}Provider.kt", "w", encoding='utf-8') as f:
                    f.write(code)
                print(f"✅ {site} basariyla eklendi.")
        except Exception as e:
            print(f"❌ {site} hatasi: {e}")
