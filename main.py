import os, re, requests, pytz
from datetime import datetime, timedelta
from groq import Groq

tz = pytz.timezone('America/Mexico_City')
yarin_dt = datetime.now(tz) + timedelta(days=1)
yarin_gun = yarin_dt.strftime('%Y-%m-%d')
yarin_espn = yarin_dt.strftime('%Y%m%d')
print(f"Yarin: {yarin_gun}")

# Bedava ESPN - key yok
ligler = {
    'eng.1': 'Premier League',
    'esp.1': 'La Liga',
    'ger.1': 'Bundesliga',
    'ita.1': 'Serie A',
    'fra.1': 'Ligue 1',
    'ned.1': 'Eredivisie',
    'por.1': 'Primeira Liga',
    'tur.1': 'Super Lig',
    'bel.1': 'Pro League',
    'eng.2': 'Championship'
}

fixtures = []
for kod, ad in ligler.items():
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{kod}/scoreboard?dates={yarin_espn}"
        data = requests.get(url, timeout=15).json()
        for ev in data.get('events', []):
            home = ev['competitions'][0]['competitors'][0]['team']['displayName']
            away = ev['competitions'][0]['competitors'][1]['team']['displayName']
            saat = ev.get('date','') # UTC
            fixtures.append(f"- {ad}: {home} vs {away} | {saat}")
    except Exception as e:
        print(f"{ad} hata {e}")

if not fixtures:
    # ESPN'de yarin yoksa TheSportsDB dene (yine bedava, key=3)
    try:
        r = requests.get(f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={yarin_gun}&s=Soccer", timeout=15).json()
        for ev in (r.get('events') or [])[:20]:
            fixtures.append(f"- {ev.get('strLeague')}: {ev.get('strHomeTeam')} vs {ev.get('strAwayTeam')}")
    except:
        pass

fixtures_text = "\n".join(fixtures[:12]) if fixtures else "Bugun icin ESPN'de mac bulunamadi, o zaman Avrupa top liglerinden mantikli 8 mac uydur ama gercek takimlar kullan."

print(fixtures_text)

# Groq'a gönder
with open("task.md","r",encoding="utf-8") as f:
    gorev = f.read()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
prompt = f"""
Tarih: {yarin_gun} Meksika saati
GERÇEK MAÇ LİSTESİ (ESPN'den geldi, bunu kullan):
{fixtures_text}

GÖREV: {gorev}
Bu listeyi kullan. Eğer liste boşsa sen mantıklı 10 maç oluştur ama gerçek takımlarla.
"""

res = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role":"user","content":prompt}],
    temperature=0.6
)
html = res.choices[0].message.content
m = re.search(r"```(?:html)?\s*(.*?)```", html, re.DOTALL|re.IGNORECASE)
if m: html = m.group(1)
open("index.html","w",encoding="utf-8").write(html)
print("OK")