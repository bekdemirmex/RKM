import os
from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
with open("task.md") as f:
    gorev = f.read()

prompt = f"Gorev: {gorev}. Tek bir dosya yap: index.html. Sadece HTML kodunu ver, aciklama yapma."

res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
open("index.html","w", encoding="utf-8").write(res.choices[0].message.content)
print("index.html olustu")