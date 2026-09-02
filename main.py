import os
from groq import Groq

# anahtarını buraya yapıştır
client = Groq(api_key="gsk_...")

with open("tasks.md","r") as f:
    gorev = f.read()

resp = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role":"user","content":f"Görevin: {gorev}. Kodla ve açıkla."}]
)
print(resp.choices[0].message.content)