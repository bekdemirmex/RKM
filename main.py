import os
import re
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY bulunamadi")

client = Groq(api_key=api_key)

with open("task.md", "r", encoding="utf-8") as f:
    gorev = f.read()

prompt = f"""
Sen bir frontend uzmanisin.
GOREV: {gorev}

KURALLAR:
- Sadece tek dosya index.html uret
- Tam calisan, responsive, hatasiz kod ver
- Harici kutuphane kullanma, CSS ve JS inline olsun
- Butonlar onclick ile calissin
- Sadece HTML kodunu ver, aciklama yazma
"""

res = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)

content = res.choices[0].message.content

# ```html... ``` bloklarini duzgun temizle
m = re.search(r"```(?:html)?\s*(.*?)```", content, re.DOTALL | re.IGNORECASE)
if m:
    content = m.group(1)

content = content.strip()

# <!DOCTYPE'tan once kalan copu at
if "<!DOCTYPE" in content.upper():
    idx = content.upper().find("<!DOCTYPE")
    content = content[idx:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("OK - index.html yazildi")