import os, requests, json, re

# Aranacak ana depolar ve dallar
REPOS = [
    {"base": "https://raw.githubusercontent.com/sarapcanagii/Pitipitii", "branches": ["main", "master"], "pkg": "pitipitii"},
    {"base": "https://raw.githubusercontent.com/keyiflerolsun/Kekik-cloudstream", "branches": ["master", "main"], "pkg": "kekik"}
]

with open('linkler.json', 'r', encoding='utf-8') as f:
    target_sites = json.load(f)

for site, url in target_sites.items():
    print(f"🛠️ {site} aranıyor...")
    success = False
    
    for repo in REPOS:
        for branch in repo['branches']:
            # Farklı dosya isimlerini ve yollarını dene
            filenames = [f"{site}.kt", f"{site}Provider.kt"]
            for fname in filenames:
                src_url = f"{repo['base']}/{branch}/{site}/src/main/kotlin/com/{repo['pkg']}/{fname}"
                try:
                    res = requests.get(src_url, timeout=10)
                    if res.status_code == 200:
                        code = res.text
                        # Linkleri degistir
                        code = code.replace('mainUrl = "', f'mainUrl = "{url}')
                        code = code.replace('baseUrl = "', f'baseUrl = "{url}')
                        # Paket ismini senin adina cevir
                        code = re.sub(r'package\s+com\.[a-zA-Z0-9\.]+', 'package com.emin', code)
                        
                        path = f"{site}/src/main/kotlin/com/emin"
                        os.makedirs(path, exist_ok=True)
                        with open(f"{path}/{site}Provider.kt", "w", encoding='utf-8') as f:
                            f.write(code)
                        print(f"✅ {site} bulundu ve {repo['base'].split('/')[-1]} üzerinden kuruldu!")
                        success = True
                        break
                except: continue
            if success: break
        if success: break
    
    if not success:
        print(f"❌ {site} hiçbir adreste bulunamadı! İsmi kontrol et.")
