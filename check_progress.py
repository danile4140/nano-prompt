import json, os, re, datetime, sys

stories_all = ["八十天环游世界","南海奇幻故事","小气财神","校园天外来客","格列佛游记","歌剧魅影","汤姆索亚历险记","爱丽丝梦游仙境","王子复仇记","糖果屋"]
docs_base = "docs"

now = datetime.datetime.now()
if now.hour < 8:
    print("SILENT")
    sys.exit(0)

done_stories = {}
active_story = None
active_info = {}
pending_stories = []

for story in stories_all:
    dd = os.path.join(docs_base, story, "draft")
    op = os.path.join(docs_base, story, "output.json")

    if os.path.exists(op):
        try:
            d = json.load(open(op, encoding="utf-8"))
            cnt = len(d.get("storyboard_assets", []))
            if cnt > 0:
                done_stories[story] = cnt
                continue
        except:
            pass

    if not os.path.exists(dd):
        pending_stories.append(story)
        continue

    plan_files = sorted([f for f in os.listdir(dd) if re.match(r"plan_B\d+\.md", f)])
    if not plan_files:
        pending_stories.append(story)
        continue

    if active_story is None:
        chs = {}
        for pf in plan_files:
            m = re.match(r"plan_B(\d+)\.md", pf)
            n = int(m.group(1))
            c = open(os.path.join(dd, pf), encoding="utf-8").read()
            m2 = re.search(r"共 \*\*(\d+)\*\* 条分镜", c)
            chs[n] = {"total": int(m2.group(1)) if m2 else 0, "dl": 0, "dp": 0}

        # 5.3a: 读批次文件 draft_BN_s_e.json（累加每章完成数）
        for f in os.listdir(dd):
            m = re.match(r"draft_B(\d+)_\d+_\d+\.json$", f)
            if m:
                n = int(m.group(1))
                try:
                    d = json.load(open(os.path.join(dd, f), encoding="utf-8"))
                    if n in chs:
                        chs[n]["dl"] += len(d.get("storyboard_draft", []))
                except:
                    pass

        # 5.3b: 读批次文件 assets_BN_s_e.json（累加每章完成数）
        for f in os.listdir(dd):
            m = re.match(r"assets_B(\d+)_\d+_\d+\.json$", f)
            if m:
                n = int(m.group(1))
                try:
                    d = json.load(open(os.path.join(dd, f), encoding="utf-8"))
                    if n in chs:
                        chs[n]["dp"] += len(d.get("storyboard_assets", []))
                except:
                    pass

        for n in chs:
            ch = chs[n]
            if ch["dp"] >= ch["total"] > 0:
                ch["phase"] = "prompt完成"
            elif ch["dp"] > 0:
                ch["phase"] = f"prompt生成中({ch['dp']}/{ch['total']})"
            elif ch["dl"] >= ch["total"] > 0:
                ch["phase"] = "layout完成，合并拆批中"
            elif ch["dl"] > 0:
                ch["phase"] = f"layout生成中({ch['dl']}/{ch['total']})"
            elif os.path.exists(os.path.join(dd, f"tmp_B{n}_full_cs.json")):
                ch["phase"] = "预提取完成，等待layout"
            else:
                ch["phase"] = "分镜规划完成，等待预提取"

        active_story = story
        active_info = {
            "name": story,
            "chs": chs,
            "total": sum(v["total"] for v in chs.values()),
            "done": sum(v["dp"] for v in chs.values()),
            "layout_done": sum(v["dl"] for v in chs.values()),
        }
    else:
        pending_stories.append(story)

hh = now.strftime("%H:%M")
lines = [f"【绘本流水线】进度同步 ⏰  {hh}", ""]

if active_story:
    p = active_info
    pct = int(p["done"] / p["total"] * 100) if p["total"] else 0
    layout_pct = int(p["layout_done"] / p["total"] * 100) if p["total"] else 0
    lines.append(f"▶ 当前故事：《{p['name']}》  prompt {p['done']}/{p['total']} 条（{pct}%）")
    if p["layout_done"] > p["done"]:
        lines.append(f"  layout已完成 {p['layout_done']}/{p['total']} 条（{layout_pct}%），prompt扩写中")
    lines.append("  各章进度：")
    for n in sorted(p["chs"]):
        ch = p["chs"][n]
        filled = int(ch["dp"] / ch["total"] * 10) if ch["total"] else 0
        bar = "█" * filled + "░" * (10 - filled)
        lines.append(f"    第{n:02d}章  共{ch['total']:3d}条  {bar}  {ch['phase']}")
    lines.append("")

if done_stories:
    lines.append("✅ 已完成故事：")
    for s in stories_all:
        if s in done_stories:
            lines.append(f"  • {s}（{done_stories[s]}条）")
    lines.append("")

if pending_stories:
    lines.append(f"⏳ 待处理（{len(pending_stories)}个）：{'、'.join(pending_stories)}")

print("\n".join(lines))
