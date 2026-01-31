import os, requests, json, re, zipfile, io

# Kaynak Repolar
SOURCES = [
    "https://github.com/sarapcanagii/Pitipitii/archive/refs/heads/main.zip",
    "https://github.com/keyiflerolsun/Kekik-cloudstream/archive/refs/heads/master.zip"
]

with open('linkler.json', 'r', encoding='utf-8') as f:
    target_sites = json.load(f)

def update_code(code, url, site_name):
    # Linkleri guncelle
    code = code.replace('mainUrl = "', f'mainUrl = "{url}')
    code = code.replace('baseUrl = "', f'baseUrl = "{url}')
    # Paket ismini senin adina cevir
    code = re.sub(r'package\s+com\.[a-zA-Z0-9\.]+', 'package com.emin', code)
    return code

for site, url in target_sites.items():
    print(f"🔍 {site} aranıyor...")
    found = False
    
    for repo_url in SOURCES:
        if found: break
        try:
            r = requests.get(repo_url)
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                for file_info in z.infolist():
                    # Dosya isminde site adı geçiyor mu ve .kt mi?
                    if site.lower() in file_info.filename.lower() and file_info.filename.endswith('.kt'):
                        with z.open(file_info) as f:
                            code = f.read().decode('utf-8')
                            if "Cloudstream" in code or "Provider" in code:
                                print(f"✅ {site} bulundu: {file_info.filename}")
                                updated_code = update_code(code, url, site)
                                
                                path = f"{site}/src/main/kotlin/com/emin"
                                os.makedirs(path, exist_ok=True)
                                with open(f"{path}/{site}Provider.kt", "w", encoding='utf-8') as f:
                                    f.write(updated_code)
                                found = True
                                break
        except Exception as e:
            print(f"⚠️ Hata: {e}")
            
    if not found:
        print(f"❌ {site} hiçbir repoda bulunamadı.")
