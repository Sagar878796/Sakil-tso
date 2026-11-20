
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

if not isinstance(data, list):
    raise ValueError("Unexpected JSON format")

lines = ["#EXTM3U"]
count = 0

for ch in data:
    if not isinstance(ch, dict):
        continue

    # Do not package DRM credentials
    if ch.get("all_keys") or ch.get("cookie"):
        continue

    name = ch.get("name", "Unknown")
    url = ch.get("url", "")
    logo = ch.get("logo", "")
    category = ch.get("category", "Other")

    if not url.startswith("https://"):
        continue

    lines.append(
        f'#EXTINF:-1 tvg-logo="{logo}" '
        f'group-title="{category}",{name}'
    )
    lines.append(url)
    count += 1

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"Conversion completed: {count} channels")
