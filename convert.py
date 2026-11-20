
import json
import urllib.request

SOURCE = "https://lemajekaat.streamxlive.workers.dev"

req = urllib.request.Request(
    SOURCE,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=30) as response:
    data = json.loads(response.read().decode("utf-8"))

if isinstance(data, dict):
    data = data.get("channels", data.get("data", []))

output = ["#EXTM3U"]

for ch in data:
    name = ch.get("name", "Unknown")
    logo = ch.get("logo", "")
    category = ch.get("category", "Other")
    url = ch.get("url", "")

    if not url:
        continue

    output.append(
        f'#EXTINF:-1 tvg-logo="{logo}" '
        f'group-title="{category}",{name}'
    )
    output.append(url)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(output) + "\n")

print(f"Converted {len(output)//2} entries")
