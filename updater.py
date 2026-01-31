import os
import re
import json

# linkler.json dosyasını oku
with open('linkler.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

def update_provider_url(site_name, new_url):
    # Bu fonksiyon, ilgili klasördeki .kt (Kotlin) dosyasını bulur ve linki günceller
    base_path = site_name
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".kt"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # mainUrl = "..." veya baseUrl = "..." kalıbını bul ve değiştir
                # Regex ile tırnak içindeki linki güncelliyoruz
                new_content = re.sub(r'(mainUrl|baseUrl)\s*=\s*".*?"', f'\\1 = "{new_url}"', content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ {site_name} güncellendi: {new_url}")

# Tüm siteleri tek tek gez ve güncelle
for site, data in config.items():
    if os.path.exists(site):
        update_provider_url(site, data['current_url'])
    else:
        print(f"❌ {site} klasörü bulunamadı, atlanıyor.")
