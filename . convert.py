
import json
import urllib.request

API = "https://lemajekaat.streamxlive.workers.dev"

req = urllib.request.Request(
    API,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode("utf-8"))

if isinstance(data, dict):
    data = data.get("channels", data.get("data", []))

m3u = ["#EXTM3U"]

for ch in data:
    name = ch.get("name", "Unknown")
    url = ch.get("url", "")
    logo = ch.get("logo", "")
    category = ch.get("category", "Other")

    if not url:
        continue

    m3u.append(
        f'#EXTINF:-1 tvg-logo="{logo}" '
        f'group-title="{category}",{name}'
    )
    m3u.append(url)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(m3u))

print("M3U playlist created successfully!")
