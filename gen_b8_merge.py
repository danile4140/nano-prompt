import json

with open("E:/coze-ai-nanobanana/b8_part1.json", "r", encoding="utf-8") as f:
    part1 = json.load(f)
with open("E:/coze-ai-nanobanana/b8_part2.json", "r", encoding="utf-8") as f:
    part2 = json.load(f)

all_items = part1 + part2
print(f"Total: {len(all_items)}")
print("IDs:", [x["id"] for x in all_items])

# Verify no internal IDs in prompt text
bad = []
import re
id_pattern = re.compile(r'\b(C1b?|C2[0-9]?|C18|C19|C20|S19|S20|S22|B8-\d+)\b')
for item in all_items:
    m = id_pattern.search(item["prompt"])
    if m:
        bad.append((item["id"], m.group()))

if bad:
    print("WARNING - IDs found in prompts:", bad)
else:
    print("OK - no internal IDs in prompts")

# Load existing output.json and update storyboard_assets
with open("E:/coze-ai-nanobanana/output.json", "r", encoding="utf-8") as f:
    output = json.load(f)

output["storyboard_assets"] = all_items

with open("E:/coze-ai-nanobanana/output.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("Written to output.json")
print("storyboard_assets count:", len(output["storyboard_assets"]))
