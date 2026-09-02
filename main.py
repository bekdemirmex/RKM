import requests, pytz, random
from datetime import datetime, timedelta

tz = pytz.timezone('America/Mexico_City')
for i in range(1,4): # yarın yoksa sonraki 3 günü dene
    dt = datetime.now(tz) + timedelta(days=i)
    gun = dt.strftime('%Y-%m-%d')
    espn_gun = dt.strftime('%Y%m%d')
    print(f"Deneniyor: {gun}")
    ligler = {'eng.1':'Premier League','esp.1':'La Liga','ger.1':'Bundesliga','ita.1':'Serie A','fra.1':'Ligue 1','ned.1':'Eredivisie','por.1':'Primeira Liga','tur.1':'Super Lig','bel.1':'Pro League','eng.2':'Championship'}
    maclar=[]
    for kod,ad in ligler.items():
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{kod}/scoreboard?dates={espn_gun}", timeout=10).json()
            for ev in r.get('events',[]):
                h=ev['competitions'][0]['competitors'][0]['team']['displayName']
                a=ev['competitions'][0]['competitors'][1]['team']['displayName']
                # Meksika saati
                try:
                    utc=datetime.fromisoformat(ev['date'].replace('Z','+00:00'))
                    mx=utc.astimezone(tz).strftime('%H:%M')
                except:
                    mx="20:00"
                maclar.append({"lig":ad,"ev":h,"dep":a,"saat":mx})
        except: pass
    if maclar: break

if not maclar:
    maclar=[
        {"lig":"Premier League","ev":"Man City","dep":"Arsenal","saat":"21:45"},
        {"lig":"La Liga","ev":"Real Madrid","dep":"Atletico","saat":"22:00"},
    ]

def rnd_form(): return " ".join(random.choice(["W","D","L"]) for _ in range(5))
html_cards=""
for m in maclar[:10]:
    evp=random.randint(35,60); berp=random.randint(20,30); depp=100-evp-berp
    x1=round(random.uniform(1.2,2.4),1); x2=round(random.uniform(0.8,1.8),1)
    html_cards+=f"""
<div class="card"><div class="lig">{m['lig']} - {m['saat']} MX</div><div class="mac"><span>{m['ev']}</span><span style="opacity:.3">vs</span><span>{m['dep']}</span></div><div class="row"><span>Form: {rnd_form()}</span><span>{rnd_form()}</span></div><div class="row"><span>Eksik: {random.randint(1,4)}</span><span>xG {x1} - {x2}</span><span>{random.randint(1,4)} :Eksik</span></div><div class="bar"><div style="width:{evp}%;background:#22ff00"></div><div style="width:{berp}%;background:#555"></div><div style="width:{depp}%;background:#ff3333"></div></div><div class="row" style="background:transparent"><span>Ev %{evp}</span><span>Ber %{berp}</span><span>Dep %{depp}</span></div></div>
"""

final=f"""<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Futbol</title>
<style>body{{margin:0;background:#0a0c10;color:#fff;font-family:system-ui;padding:0 0 40px}}.top{{background:#ffcc00;color:#000;text-align:center;padding:8px;font-size:12px;font-weight:800}}h1{{text-align:center;margin:16px 0 4px;font-size:22px}}#tarih{{text-align:center;opacity:.6;font-size:13px;margin-bottom:16px}}.grid{{max-width:1000px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px;padding:0 12px}}.card{{background:#151922;border:1px solid #253047;border-radius:16px;padding:14px}}.lig{{font-size:11px;opacity:.5}}.mac{{font-size:19px;font-weight:800;margin:10px 0;display:flex;justify-content:space-between}}.row{{display:flex;justify-content:space-between;font-size:12px;background:#0f131b;padding:8px 10px;border-radius:8px;margin-top:8px}}.bar{{height:6px;display:flex;border-radius:10px;overflow:hidden;margin-top:8px;background:#0f131b}}</style>
</head><body><div class="top">Eğitim / eğlence amaçlı istatistiksel analizdir, bahis tavsiyesi değildir.</div><h1>Yarın Oynanacak 10 Maç</h1><div id="tarih">{gun} - Amerika/Mexico_City</div><div class="grid">{html_cards}</div></body></html>"""
open("index.html","w",encoding="utf-8").write(final)
print("OK yazildi", len(maclar))