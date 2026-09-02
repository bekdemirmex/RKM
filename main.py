import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY bulunamadi!")

client = Groq(api_key=api_key)

with open("task.md","r",encoding="utf-8") as f:
    gorev = f.read()

print(f"Gorev: {gorev}")

prompt = f"""
Gorev: {gorev}
Sadece tek bir dosya olacak: index.html
Sadece HTML, CSS, JS kodu ver. Aciklama yazma, ``` kullanma.
Modern, calisan bir uygulama yap.
"""

res = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role":"user","content": prompt}]
)

content = res.choices[0].message.content.strip()

# ``` varsa temizle
if "```" in content:
    if "```html" in content:
        content = content.split("```html")[1].split("```")[0]
    else:
        content = content.split("```")[1].split("```")[0]

open("index.html","w",encoding="utf-8").write(content)
print("index.html yazildi!")