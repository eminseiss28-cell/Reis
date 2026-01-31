import os, requests, json, re

# Aramanın yapılacağı ana depolar ve paket isimleri
REPOS = [
    {"n": "Pitipitii", "b": "https://raw.githubusercontent.com/sarapcanagii/Pitipitii/master", "p": "pitipitii"},
    {"n": "Kekik", "b": "https://raw.githubusercontent.com/keyiflerolsun/Kekik-cloudstream/master", "p": "kekik"},
    {"n": "Nikyokki", "b": "https://raw.githubusercontent.com/Nikyokki/Turkish-Providers/main", "p": "nikyokki"},
    {"n": "Pitipitii_Main", "b": "https://raw.githubusercontent.com/sarapcanagii/Pitipitii/main", "p": "pitipitii"},
    {"n": "Kraptor", "b": "https://raw.githubusercontent.com/Kraptor123/cs-kraptor/master", "p": "kraptor"}
]

with open('linkler.json', 'r', encoding='utf-8') as f:
    target_sites = json.load(f)

for site, url in target_sites.items():
    print(f"🛠️ {site} aranıyor...")
    success = False
    for repo in REPOS:
        # Farklı dosya yolu kombinasyonlarını dener
        patterns = [
            f"{repo['b']}/{site}/src/main/kotlin/com/{repo['p']}/{site}.kt",
            f"{repo['b']}/{site}/src/main/kotlin/com/{repo['p']}/{site}Provider.kt",
            f"{repo['b']}/Providers/{site}/src/main/kotlin/com/{repo['p']}/{site}Provider.kt"
        ]
        for src_url in patterns:
            try:
                res = requests.get(src_url, timeout=10)
                if res.status_code == 200:
                    code = res.text
                    # Link ve Paket Güncelleme (Cerrahi Müdahale)
                    code = code.replace('mainUrl = "', f'mainUrl = "{url}')
                    code = code.replace('baseUrl = "', f'baseUrl = "{url}')
                    code = re.sub(r'package\s+com\.[a-zA-Z0-9\.]+', 'package com.emin', code)
                    
                    path = f"{site}/src/main/kotlin/com/emin"
                    os.makedirs(path, exist_ok=True)
                    with open(f"{path}/{site}Provider.kt", "w", encoding='utf-8') as f:
                        f.write(code)
                    print(f"✅ {site} [{repo['n']}] üzerinden kuruldu!")
                    success = True; break
            except: continue
        if success: break
    if not success: print(f"❌ {site} hiçbir kaynakta bulunamadı.")
