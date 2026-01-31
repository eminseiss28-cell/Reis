import os, requests, json, re, zipfile, io

SOURCES = [
    "https://github.com/sarapcanagii/Pitipitii/archive/refs/heads/main.zip",
    "https://github.com/keyiflerolsun/Kekik-cloudstream/archive/refs/heads/master.zip",
    "https://github.com/recloudstream/cloudstream-extensions/archive/refs/heads/master.zip"
]

with open('linkler.json', 'r', encoding='utf-8') as f:
    target_sites = json.load(f)

# Marş basan dosyanın şablonu (Plugin.kt)
PLUGIN_TEMPLATE = """package com.emin
import com.lagradost.cloudstream3.plugins.CloudstreamPlugin
import com.lagradost.cloudstream3.plugins.Plugin
import android.content.Context

@CloudstreamPlugin
class {site}Plugin: Plugin() {{
    override fun load(context: Context) {{
        registerMainAPI({site}())
    }}
}}
"""

for site, url in target_sites.items():
    print(f"🔍 {site} montaj hattına girdi...")
    found = False
    for repo_url in SOURCES:
        if found: break
        try:
            r = requests.get(repo_url, timeout=15)
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                for file_info in z.infolist():
                    if site.lower() in file_info.filename.lower() and file_info.filename.endswith('.kt'):
                        with z.open(file_info) as f:
                            code = f.read().decode('utf-8')
                            if "MainAPI" in code or "Provider" in code:
                                print(f"✅ {site} motoru bulundu!")
                                # Linki ve paket adını güncelle
                                code = code.replace('mainUrl = "', f'mainUrl = "{url}')
                                code = code.replace('baseUrl = "', f'baseUrl = "{url}')
                                code = re.sub(r'package\s+com\.[a-zA-Z0-9\.]+', 'package com.emin', code)
                                
                                path = f"{site}/src/main/kotlin/com/emin"
                                os.makedirs(path, exist_ok=True)
                                
                                # 1. Motoru (Provider) kaydet
                                with open(f"{path}/{site}Provider.kt", "w", encoding='utf-8') as f_out:
                                    f_out.write(code)
                                
                                # 2. Kontağı (Plugin) kaydet (Senin attığın dosya)
                                with open(f"{path}/{site}Plugin.kt", "w", encoding='utf-8') as f_out:
                                    f_out.write(PLUGIN_TEMPLATE.format(site=site))
                                
                                found = True; break
        except: continue
    if not found: print(f"❌ {site} bulunamadı.")
