---
name: story-pipeline
description: 一站式绘本分镜生成流水线：遍历 docs/ 目录下所有故事，对每个含 input.txt 的子目录依次自动完成【角色/场景生成 → 分镜规划 → prompt 生成】全流程，输出完整 output.json，无需用户中途确认，每小时通过飞书（lark-cli）发送进度同步消息。每个故事独立存放在 docs/{story-name}/ 目录下。当用户说"跑流水线"、"一键生成分镜"、"帮我生成完整分镜稿"、"从原文生成绘本"、"全流程跑一遍"、"批量跑"、"遍历docs"、"pipeline"、"story pipeline"时触发。只要涉及从英文原著端到端生成绘本分镜，即使用户没说"流水线"，也应触发本 skill。
---

# Story Pipeline — 一站式绘本分镜生成

从英文原著到完整 `output.json`，全自动无确认。四个阶段依次执行：

```
阶段 0  准备          建目录、读原文、初始化飞书通知
阶段 1  角色/场景      char-scene-generator 流程
阶段 2  分镜规划       storyboard-generator 第二~四步
阶段 3  prompt 生成    storyboard-generator 第五~七步（5.3a 直接输出 assets）
```

每小时整点前后通过 **lark-cli** 发送进度消息。风格与媒介字段全部使用占位符 `STYLE_PLACEHOLDER`，不填入真实风格内容。

---

## 调用方式

**自动遍历模式**：扫描 `docs/` 目录下所有包含 `input.txt` 的子目录，按顺序逐个处理。已有 `output.json` 且内容非空的故事自动跳过。

用户只需提供：
- **飞书接收人**：open_id 或 chat_id；若未提供则询问一次

其余全自动推断：故事名称 = 子目录名，原著 = 该目录下的 `input.txt`。

所有中间产物和最终结果均存放在 `docs/{story-name}/`。

---

## 阶段 0 — 准备（主对话完成）

### 0.1 扫描待处理故事列表

```python
import os, json

docs_dir = "docs"
stories = []

for name in sorted(os.listdir(docs_dir)):
    story_dir = os.path.join(docs_dir, name)
    input_file = os.path.join(story_dir, "input.txt")
    output_file = os.path.join(story_dir, "output.json")

    if not os.path.isdir(story_dir) or not os.path.exists(input_file):
        continue  # 跳过没有原著的目录

    # 已有完整 output.json 则跳过
    if os.path.exists(output_file):
        try:
            data = json.load(open(output_file, encoding='utf-8'))
            if data.get('storyboard_assets'):
                print(f"跳过 {name}（已有 {len(data['storyboard_assets'])} 条分镜）")
                continue
        except Exception:
            pass  # 文件损坏则重跑

    stories.append(name)
    print(f"待处理：{name}")

print(f"
共 {len(stories)} 个故事待处理")
```

### 0.2 逐故事初始化目录

对 `stories` 列表中每个 `story_name` 依次执行以下流程：

```python
story_name = "CURRENT_STORY"   # 遍历时替换为实际目录名
project_dir = f"docs/{story_name}"

for d in [project_dir, f"{project_dir}/draft"]:
    os.makedirs(d, exist_ok=True)

out_path = f"{project_dir}/output.json"
if not os.path.exists(out_path):
    with open(out_path, 'w', encoding='utf-8', newline='
') as f:
        json.dump({"storyboard_assets": []}, f, ensure_ascii=False)
        f.write('
')
```

### 0.3 风格设定

在 `docs/{story-name}/style_settings.txt` 写入字面量 `STYLE_PLACEHOLDER`，不向用户询问真实风格。

### 0.4 初始化进度状态

```python
import json, time

progress = {
    "story_name": story_name,
    "project_dir": project_dir,
    "start_time": time.time(),
    "phase": "0-准备",
    "detail": "初始化完成，即将开始角色/场景生成",
    "chapters_total": 0,
    "chapters_done": 0,
    "assets_total": 0,
    "assets_done": 0,
}

with open(f"{project_dir}/draft/progress.json", 'w', encoding='utf-8', newline='\n') as f:
    json.dump(progress, f, ensure_ascii=False, indent=2)
    f.write('\n')
```

### 0.5 发送开始通知（飞书）

```bash
# 替换 RECIPIENT 为 open_id 或 chat_id
lark-cli im message send \
  --to RECIPIENT \
  --type text \
  --content "【{story_name}】流水线启动\n阶段：0-准备\n时间：$(date '+%H:%M')\n原著已就绪，开始生成角色和场景..."
```

---

## 阶段 1 — 角色/场景生成（Workflow）

参照 **char-scene-generator** 流程，但 `style_setting` 固定传入 `STYLE_PLACEHOLDER`。

> 规则文件路径：char-scene-generator skill 的 `references/5.1_characters.md` 和 `references/5.2_scenes.md`。
> 需要在主对话中找到 char-scene-generator skill 的安装目录并读取这两个文件。

### 1.1 并行 Workflow

```javascript
export const meta = {
  name: 'story-pipeline-phase1',
  description: '并行生成角色和场景设定卡',
  phases: [{ title: '角色/场景', detail: '并行生成角色和场景' }],
}

const projectDir = args.projectDir
const charSceneSkillDir = args.charSceneSkillDir  // char-scene-generator skill 目录
const inputText = args.inputText

await parallel([
  () => agent(
    `你负责生成角色设定卡。
1. Read ${charSceneSkillDir}/references/5.1_characters.md，提取 ### 系统提示词 下方完整规则
2. 按规则分析以下原著，style_setting 固定为字符串 "STYLE_PLACEHOLDER"：
---
${inputText}
---
3. Write 到 ${projectDir}/draft/tmp_characters.json，格式：{"character_assets": [...]}
   只输出 JSON，绝对不含 \`\`\` 代码块包裹`,
    { label: '角色生成', phase: '角色/场景' }
  ),
  () => agent(
    `你负责生成场景设定卡。
1. Read ${charSceneSkillDir}/references/5.2_scenes.md，提取 ### 系统提示词 下方完整规则
2. 按规则分析以下原著，style_setting 固定为字符串 "STYLE_PLACEHOLDER"：
---
${inputText}
---
3. Write 到 ${projectDir}/draft/tmp_scenes.json，格式：{"scene_assets": [...]}
   只输出 JSON，绝对不含 \`\`\` 代码块包裹`,
    { label: '场景生成', phase: '角色/场景' }
  ),
])
```

### 1.2 合并输出（主对话 Python）

```python
import json

chars = json.load(open(f'{project_dir}/draft/tmp_characters.json', encoding='utf-8'))
scenes = json.load(open(f'{project_dir}/draft/tmp_scenes.json', encoding='utf-8'))

output = {
    'style_setting': 'STYLE_PLACEHOLDER',
    'character_assets': chars['character_assets'],
    'scene_assets': scenes['scene_assets'],
}

cs_path = f'{project_dir}/char_scene_info.json'
with open(cs_path, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
    f.write('\n')

print(f'角色：{len(output["character_assets"])} 个')
print(f'场景：{len(output["scene_assets"])} 个')

# 编码体检
with open(cs_path, 'rb') as f: raw = f.read()
print('U+FFFD残留:', raw.count(b'\xef\xbf\xbd'))
raw.decode('utf-8', errors='strict')
print('严格UTF-8：通过')
```

### 1.3 进度通知

更新 `draft/progress.json` 的 `phase` 为 `"1-角色场景完成"`，并发送飞书消息：

```bash
lark-cli im message send \
  --to RECIPIENT \
  --type text \
  --content "【{story_name}】阶段1完成\n✅ 角色/场景生成完毕\n角色：N 个，场景：M 个\n下一步：分镜规划"
```

---

## 阶段 2 — 分镜规划（Workflow）

参照 **storyboard-generator** 第二步（生成分拆计划），但：
- `projectDir` 指向 `docs/{story-name}/`
- `char_scene_info.json` 已在阶段 1 生成
- 跳过"等用户确认"步骤，直接继续

### 2.1 解析章节

从 `input.txt` 按 `Chapter` 标题切分章节，记录每章编号和文本。

### 2.2 预提取 char_scene 子集

按照 storyboard-generator 第一步的 Python 逻辑，为每章提取涉及的角色/场景子集，写入 `draft/tmp_B{N}_full_cs.json`。

```python
import json, re, shutil, os

data = json.load(open(f'{project_dir}/char_scene_info.json', encoding='utf-8'))
# 这里写入 STYLE_PLACEHOLDER 而非真实风格，与阶段1保持一致

# 为每章写全量 cs 子集（若章节数多，按实际原文分析涉及角色/场景ID）
# 简化策略：每章使用全量角色和场景（小说通常角色有限）
for n, chapter in enumerate(chapters, 1):
    subset = {
        'style_setting': 'STYLE_PLACEHOLDER',
        'character_assets': data['character_assets'],
        'scene_assets': data['scene_assets'],
    }
    out = f'{project_dir}/draft/tmp_B{n}_full_cs.json'
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(subset, f, ensure_ascii=False, indent=2)
        f.write('\n')
```

### 2.3 Workflow：生成分拆计划（2 章并发）

```javascript
export const meta = {
  name: 'story-pipeline-phase2',
  description: '分镜句子分配，每章生成 plan_B{N}.md',
  phases: [{ title: '分镜规划', detail: '逐章节句子分配' }],
}

const rounds = []  // 按章数分轮，每轮最多2章并发

for (const round of rounds) {
  await parallel(round.map(chapter => () =>
    agent(
      `你的任务是执行5.3a分镜规划的【阶段一：句子分配】，不生成任何layout内容。
1. Read ${projectDir}/workflow/5.3a_storyboard_planning.md → 提取完整规则
2. Read ${projectDir}/draft/tmp_B${chapter.n}_full_cs.json → 获取 style_setting（值为 STYLE_PLACEHOLDER）
3. 对以下章节原文执行阶段一（逐句标注归属分镜，自检未覆盖句数=0）：
---
${chapter.text}
---
4. 写入 ${projectDir}/draft/plan_B${chapter.n}.md
5. 写完后追加每条原文句子的中文译文（在英文句下方加 "译：[译文]"）并写回`,
      { label: `计划-B${chapter.n}`, phase: '分镜规划' }
    )
  ))
}
```

> ⚠️ 规则文件 `workflow/5.3a_storyboard_planning.md` 是项目级文件，位于 `docs/{story-name}/workflow/`。若不存在，需要从全局 workflow/ 目录复制过来，或在 agent prompt 中直接指向全局路径。

### 2.4 进度通知

```bash
lark-cli im message send \
  --to RECIPIENT \
  --type text \
  --content "【{story_name}】阶段2完成\n✅ 分镜规划完毕\n共 N 章，总计 M 条分镜\n下一步：5.3a layout 生成"
```

---

## 阶段 3 — Prompt 生成（Workflow）

参照 **storyboard-generator** 第四~七步，`style_setting` / `⑥风格与媒介` 一律写入 `STYLE_PLACEHOLDER`。

5.3a 节点直接输出 storyboard_assets（含 prompt，layout 为空字符串），无需额外的 prompt 扩写步骤。

### 3.1 预提取批次文件（主对话 Python）

按 storyboard-generator 第四步逻辑，为每章的 5.3a 批次（≤4 条/批）写 `tmp_B{N}_cs_{tag}.json` 和 `tmp_B{N}_plan_{tag}.txt`。

### 3.2 5.3a 生成（Workflow，2 章并发，每批 ≤4 条）

参照 storyboard-generator 第五步模板，额外约束：

- agent prompt 末尾加一行：`⑥风格与媒介段写入字面量 "STYLE_PLACEHOLDER"，不填真实风格内容`

### 3.3 合并 assets，QC，写入 output.json

参照 storyboard-generator 第六、七步，包括 U+FFFD 自动修复流程。

### 3.6 进度通知

```bash
lark-cli im message send \
  --to RECIPIENT \
  --type text \
  --content "【{story_name}】流水线完成 🎉\n✅ output.json 已生成\n共 N 条分镜\n路径：docs/{story_name}/output.json\n风格占位符 STYLE_PLACEHOLDER 待后续填入"
```

---

## 飞书整点定时通知

**规则**：
- **整点触发**：每个故事完成后检查当前小时，若跨过了新的整点（当前小时 ≠ 上次通知小时）则发送
- **静默时段**：0:00–7:59 不发送
- **强制发送**：每个故事完成时强制发一次（静默时段除外）

**消息格式（进行中）**：
```
【绘本流水线】进度同步 ⏰ HH:00

▶ 当前故事：《{story_name}》
  章节结构：
    第1章  18条分镜  ██████████ 已完成
    第2章  22条分镜  ████░░░░░░ 生成中（已完成10/22）
    第3章  15条分镜  ░░░░░░░░░░ 待处理
  当前进度：{done}/{total} 条分镜（{pct}%）

✅ 已完成故事：
  • 绿野仙踪（151条）
  • 八十天环游世界（87条）
```

**消息格式（全部完成）**：
```
【绘本流水线】全部完成 🎉 HH:MM

✅ 已完成（共N个故事）：
  • 故事A（X条分镜）
  • 故事B（Y条分镜）
```

**实现**：在主对话维护 `last_notify_hour`（初始 -1），每个故事完成后执行：

```python
import subprocess, datetime, json, os, re

def build_progress_msg(stories_all, stories_done_map, current_story_progress=None):
    """
    stories_all: 全部故事名列表（按顺序）
    stories_done_map: {story_name: total_count}  已完成
    current_story_progress: {
        'name': str, 'chapters': [{'n':int,'total':int,'done':int}],
        'total': int, 'done': int
    } 或 None
    """
    now = datetime.datetime.now()
    hh = now.strftime('%H:%M')
    lines = [f"【绘本流水线】进度同步 ⏰ {hh}", ""]

    if current_story_progress:
        p = current_story_progress
        lines.append(f"▶ 当前故事：《{p['name']}》")
        lines.append("  章节结构：")
        for ch in p['chapters']:
            filled = int(ch['done'] / ch['total'] * 10) if ch['total'] else 0
            bar = '█' * filled + '░' * (10 - filled)
            if ch['done'] >= ch['total']:
                status = '已完成'
            elif ch['done'] > 0:
                status = f"生成中（{ch['done']}/{ch['total']}）"
            else:
                status = '待处理'
            lines.append(f"    第{ch['n']}章  {ch['total']}条  {bar} {status}")
        pct = int(p['done'] / p['total'] * 100) if p['total'] else 0
        lines.append(f"  整体进度：{p['done']}/{p['total']} 条（{pct}%）")
        lines.append("")

    done = [(s, stories_done_map[s]) for s in stories_all if s in stories_done_map]
    if done:
        lines.append("✅ 已完成故事：")
        for name, cnt in done:
            lines.append(f"  • {name}（{cnt}条）")
    return "
".join(lines)


def send_notify(recipient, msg):
    """发飞书消息（返回当前小时数）"""
    now = datetime.datetime.now()
    if now.hour < 8:
        return None  # 静默时段，不发
    subprocess.run(
        ['lark-cli', 'im', '+messages-send', '--user-id', recipient, '--text', msg],
        check=False
    )
    return now.hour


def check_hourly(last_notify_hour, recipient, msg):
    """整点检查：跨过新整点才发，返回新的 last_notify_hour"""
    now = datetime.datetime.now()
    if now.hour < 8:
        return last_notify_hour
    if now.hour != last_notify_hour:
        send_notify(recipient, msg)
        return now.hour
    return last_notify_hour


# 每个故事完成后的调用示例：
# 1. 强制发（故事完成节点）
send_notify(recipient, build_progress_msg(stories_all, stories_done_map, None))
# 2. 整点检查（各阶段切换时）
last_notify_hour = check_hourly(last_notify_hour, recipient,
                                 build_progress_msg(stories_all, stories_done_map, current_progress))
```


> ⚠️ **Windows 注意**：Python `subprocess.run(['lark-cli', ...])` 在 Windows 下可能找不到 lark-cli。在 Workflow agent 里推荐直接用 Bash 工具执行 `lark-cli im +messages-send ...`，不经过 Python subprocess。
**进度数据来源**：通过读取 `draft/plan_B{N}.md`（获取每章总分镜数）和 `draft/assets_B{N}.json`（获取已完成分镜数）实时统计，写入 `draft/progress.json` 供通知函数读取。
---

## 目录结构总览

```
docs/
└── {story-name}/
    ├── input.txt                    # 原著
    ├── style_settings.txt           # 内容固定为 "STYLE_PLACEHOLDER"
    ├── char_scene_info.json         # 阶段1输出
    ├── output.json                  # 最终输出
    ├── workflow/                    # 指向或复制自全局 workflow/ 目录
    │   ├── 5.3a_storyboard_planning.md
    │   └── 5.3b_prompt_generation.md
    └── draft/
        ├── progress.json
        ├── tmp_characters.json
        ├── tmp_scenes.json
        ├── tmp_B{N}_full_cs.json    # 每章 cs 子集
        ├── plan_B{N}.md             # 每章分镜计划
        ├── draft_B{N}.json          # 每章合并 layout
        ├── assets_B{N}.json         # 每章合并 assets
        └── (批次中间文件...)
```

---

## 关键约束（继承自子 skill）

1. **5.3a 每批 ≤4 条**（合并了规划和 prompt 生成，4 条是实测上限）
2. **Workflow 并发 ≤2 章**
3. **Workflow 运行期间禁止在 IDE 切换/打开文件**
4. **char_scene_info.json 不直接传给 agent**，只传预提取的子集文件
5. **兜底方案禁止超长字符串字面量**，必须用 `"\n".join([...])` 列表方式
6. **⑥风格与媒介 和 style_setting 一律写入 `STYLE_PLACEHOLDER`**，不填真实内容

---

## 故障排查

| 症状 | 原因 | 解法 |
|------|------|------|
| 阶段1 agent stall | 原著太长 | 拆成前后两半并行，结果合并去重 |
| 飞书消息发送失败 | lark-cli 未登录或权限不足 | `lark-cli auth login` 重新授权；检查 `--to` 参数格式 |
| 5.3b stall 超2次 | 输出量超限或 IDE 干扰 | 切换主对话兜底方案，用 `"\n".join([...])` 写 prompt |
| JSON 解析失败 | agent 输出含 Markdown 代码块 | 删除临时文件重跑；agent prompt 末尾加"只输出 JSON，绝对不含 \`\`\`" |
| output.json U+FFFD 残留 | QC agent 写回时字符损坏 | 运行 storyboard-generator 第八步的乱码修复流程 |
| workflow/ 目录找不到 | story 目录下没有规则文件 | 检查全局 workflow/ 路径，在 agent prompt 中使用绝对路径 |
