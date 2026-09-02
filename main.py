import os
from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
with open("task.md") as f:
    gorev = f.read()
prompt = f"Gorev: {gorev}. Tek bir HTML dosyasi yap, adi index.html olsun. Sadece HTML kodunu ver, aciklama yazma."
res = client.chat.completions.create(model="llama-3.1-8b-instant"", messages=[{"role":"user","content":prompt}])
open("index.html","w",encoding="utf-8").write(res.choices[0].message.content)
print("Bitti")