import os
import re
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY yok")

client = Groq(api_key=api_key)

with open("task.md", "r", encoding="utf-8") as f:
    gorev = f.read()

models = ["openai/gpt-oss-20b", "llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

final_html = None

for model in models:
    try:
        print(f"Deniyorum: {model}")
        res = client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": f"""Sen bir frontend uzmanisin. Gorev: {gorev}
Kurallar: Sadece tek dosya index.html uret. Tam calisan kod. Aciklama yazma, sadece HTML ver. Harici kutuphane kullanma."""
            }],
            temperature=0.7
        )
        content = res.choices[0].message.content
        low = content.lower()
        # Reddetme kontrolu
        if "i'm sorry" in low or "can't help" in low or "i cannot" in low or "i can't help" in low:
            print(f"{model} reddetti")
            continue

        m = re.search(r"```(?:html)?\s*(.*?)```", content, re.DOTALL | re.IGNORECASE)
        if m:
            content = m.group(1)
        content = content.strip()

        if "<html" not in low and "<!doctype" not in low and "<body" not in low:
            continue

        if "<!DOCTYPE" in content.upper():
            idx = content.upper().find("<!DOCTYPE")
            content = content[idx:]

        final_html = content
        print(f"Basarili: {model}")
        break
    except Exception as e:
        print(f"{model} hata: {e}")
        continue

if not final_html:
    final_html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Hata</title></head>
<body style="background:#111;color:#fff;font-family:system-ui;padding:40px;text-align:center">
<h2 style="color:#ff4444">Gorev anlasilamadi</h2>
<p>task.md icindeki gorev cok karmasik veya yasakli kelime iceriyor olabilir.</p>
<p style="opacity:.6">Mevcut gorev: {gorev}</p>
<p>Lutfen daha net yaz: Ornegin 'modern bir hava durumu uygulamasi yap' gibi.</p>
</body></html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("OK - index.html yazildi")