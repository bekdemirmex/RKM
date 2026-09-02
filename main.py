import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

with open("task.md","r",encoding="utf-8") as f:
    gorev = f.read()

res = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role":"user","content": f"Gorev: {gorev}. Sadece index.html kodu ver, aciklama yazma."}]
)

content = res.choices[0].message.content
if "```" in content:
    content = content.split("```")[1].replace("html","").strip()

open("index.html","w",encoding="utf-8").write(content)
print("OK - index.html yazildi")