
import json
import urllib.request

SOURCE = "https://lemajekaat.streamxlive.workers.dev"

req = urllib.request.Request(
    SOURCE,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=30) as r:
    data = json.loads(r.read().decode("utf-8"))

if isinstance(data, dict):
    data = data.get("channels", data.get("data", []))

if not isinstance(data, list):
    raise ValueError("Invalid JSON format")

lines = ["#EXTM3U"]
count = 0

for ch in data:
    if not isinstance(ch, dict):
        continue

    name = str(ch.get("name", "Unknown"))
    logo = str(ch.get("logo", ""))
    category = str(ch.get("category", "Other"))
    url = str(ch.get("url", ""))

    if not url.startswith("https://"):
        continue

    # Skip protected entries
    if ch.get("all_keys") or ch.get("cookie"):
        continue

    lines.append(
        f'#EXTINF:-1 tvg-id="{ch.get("id", "")}" '
        f'tvg-logo="{logo}" group-title="{category}",{name}'
    )
    lines.append(url)
    count += 1

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"Successfully converted {count} channels")
