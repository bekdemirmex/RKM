import requests, pytz, random
from datetime import datetime, timedelta

tz = pytz.timezone('America/Mexico_City')
now = datetime.now(tz)
end = now + timedelta(hours=24)
print(f"Aralik: {now} -> {end}")

# 35 lig - ESPN key yok
ligler = {
    'eng.1':'Premier League','eng.2':'Championship','eng.3':'League One',
    'esp.1':'La Liga','esp.2':'LaLiga2','ger.1':'Bundesliga','ger.2':'2. Bundesliga',
    'ita.1':'Serie A','fra.1':'Ligue 1','ned.1':'Eredivisie','por.1':'Primeira Liga',
    'tur.1':'Süper Lig','bel.1':'Pro League','sco.1':'Premiership','usa.1':'MLS',
    'mex.1':'Liga MX','bra.1':'Brasileirao','arg.1':'Liga Profesional','uefa.champions':'UCL',
    'uefa.europa':'UEL','uefa.europa_conference':'Conference','conmebol.libertadores':'Libertadores',
    'ger.3':'3. Liga','ita.2':'Serie B','fra.2':'Ligue 2','ned.2':'Eerste Divisie','por.2':'Liga Portugal2',
    'sui.1':'Super League','aut.1':'Bundesliga AT','den.1':'Superliga','nor.1':'Eliteserien','swe.1':'Allsvenskan','gre.1':'Super League GR','pol.1':'Ekstraklasa'
}

maclar=[]
gunler = [now.strftime('%Y%m%d'), (now+timedelta(days=1)).strftime('%Y%m%d')]
for kod, ad in ligler.items():
    for g in gunler:
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{kod}/scoreboard?dates={g}", timeout=