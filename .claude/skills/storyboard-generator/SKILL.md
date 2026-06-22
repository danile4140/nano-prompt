---
name: storyboard-generator
description: 使用 Nano Banana 2 工作流（5.3a 分镜规划 + 5.3b prompt 生成）从英文原著生成分镜。当用户要求生成分镜、跑流程、处理章节、或从 input.txt 生成 output.json 时使用本 skill。即使用户只说"生成分镜"、"跑一下"、"run"也应触发。
---

# 分镜生成器

将英文章节依次经过 5.3a（分镜规划）→ 5.3b（prompt 生成）→ 质量检查三个阶段。

## 关键约束（必读，违反必失败）

1. **5.3a layout：每批最多 6 条**（12 条会稳定 stall，6 条是实测上限）
2. **5.3b prompt：每批最多 3 条**（prompt 输出量大，超过 3 条必 stall）
3. **Workflow 并发上限：2 个**（更多并发会互相触发中断，哪怕你不动 IDE）
4. **char_scene_info.json 不能直接传给 agent**（51KB 太大）——必须在主对话预提取相关章节的角色/场景子集，写入 `draft/tmp_B{N}_full_cs.json`，让 agent 只读小文件
5. **每个 agent 只读 3 个文件**：规则文件 + 预提取 cs 文件 + draft 批次文件
6. **每个批次文件写入前必须做存在性检查**，已存在且 JSON 合法则跳过（必须同时验证 JSON 可解析，不能只检查文件大小）
7. **不要换模型**：必须用 sonnet，不要改为 haiku（质量不达标）
8. **运行 Workflow 期间禁止在 IDE 切换/打开文件**：IDE 文件操作会触发 `[Request interrupted by user]` 中断 agent，这是最主要的 stall 原因

## 文件约定

| 文件 | 作用 |
|------|------|
| `input.txt` | 原文，章节以 `从 B{N}-1 开始编号` 标记分隔 |
| `char_scene_info.json` | 完整角色/场景/风格数据（不直接传给 agent） |
| `draft/plan_B{N}.md` | 5.3a 阶段一输出：句子分配表（含中文译文） |
| `draft/draft_B{N}_{s}_{e}.json` | 5.3a 批次输出：B{N}-{s} 至 B{N}-{e} 的 layout |
| `draft/draft_B{N}.json` | 合并后的完整 layout |
| `draft/assets_B{N}_{s}_{e}.json` | 5.3b 批次输出：B{N}-{s} 至 B{N}-{e} 的 prompt |
| `draft/assets_B{N}.json` | 合并后的完整 assets |
| `draft/tmp_B{N}_cs_{tag}.json` | 预提取的批次角色/场景子集（5.3a 用） |
| `draft/tmp_B{N}_plan_{tag}.txt` | 预提取的批次分配表条目（5.3a 用） |
| `draft/tmp_B{N}_full_cs.json` | 预提取的章节全量角色/场景子集（5.3b/QC 用） |
| `output.json` | 最终合并结果（`storyboard_assets` 数组） |
| `workflow/5.3a_storyboard_planning.md` | 5.3a 规则（43KB，agent 直接 Read） |
| `workflow/5.3b_prompt_generation.md` | 5.3b 规则（45KB，agent 直接 Read） |

## 第一步 — 准备工作（主对话完成，不启动 agent）

1. **读取 `input.txt`**，按 `从 B(\d+)-1 开始编号` 标记切分章节。
2. **读取 `char_scene_info.json`**，确认存在三个字段。
3. **检查 `output.json`**，不存在则创建 `{ "storyboard_assets": [] }`。
4. **创建 `draft/`** 目录（若不存在）。
5. **过滤章节**：跳过 `output.json` 中已有对应首条 ID（如 `B8-1`）的章节。
6. **预提取 char_scene 子集**（Python 内联完成）：
   - 分析每章涉及的角色和场景 ID，从 `char_scene_info.json` 提取子集
   - 写入 `draft/tmp_B{N}_full_cs.json`（供 5.3b / QC 使用）
   - 每个 5.3a 批次也写对应的 `draft/tmp_B{N}_cs_{tag}.json` 和 `draft/tmp_B{N}_plan_{tag}.txt`

## 第二步 — 生成分拆计划（Workflow，各章并发）

每章 1 个 agent，最多 2 章并发。agent 只读：规则文件 + char_scene_info.json（此步骤可读完整文件，因为不生成大量输出）。

```javascript
export const meta = {
  name: 'storyboard-plan',
  description: '生成分镜分拆计划，仅执行句子分配，不生成 layout',
  phases: [{ title: '分拆计划', detail: '逐章节句子分配并输出计划文件' }],
}

const { chapters, projectDir } = args

await parallel(chapters.map(chapter => async () => {
  await agent(
    `你的任务是执行 5.3a 分镜规划的【阶段一：句子分配】，不生成任何 layout 内容。

1. Read ${projectDir}/workflow/5.3a_storyboard_planning.md
   - 提取 \`### 系统提示词\` 下方 \`\`\`text 块内完整规则
   - 重点：§2 逐句覆盖、§3 节拍切分、§3b 句数上限、§4 必拆充要条件

2. Read ${projectDir}/char_scene_info.json，获取 style_setting

3. 对以下章节原文执行阶段一（逐句标注归属分镜，自检未覆盖句数=0）：

章节内容（第 ${chapter.n} 章，idx=${chapter.idx}）：
---
${chapter.text}
---

4. 写入 ${projectDir}/draft/plan_B${chapter.n}.md，格式：

# 第 ${chapter.n} 章分镜规划

共 **N** 条分镜

## 分配表

**B${chapter.n}-1**（X 句）
- 分组依据：[...]
- 原文：
  1. "..."

（每条都按此格式，不得省略）

5. 写完后重新读取，为每条原文句子追加中文译文（在英文句下方加 "译：[译文]"）并写回。`,
    { label: `计划-B${chapter.n}`, phase: '分拆计划' }
  )
}))
```

## 第三步 — 展示计划并等待确认

读取所有 `draft/plan_B{N}.md`，展示每章分镜数量和文件路径，**等用户确认后**再继续。

## 第四步 — 预提取小文件（主对话完成）

用 Python 内联完成，不启动 agent：

```python
import json, re

d = json.load(open(f'{projectDir}/char_scene_info.json', encoding='utf-8'))

# 分析每章涉及的角色/场景（根据 plan 文件中出现的 ID 或手动指定）
# 为每章写 tmp_B{N}_full_cs.json（全量供 5.3b 使用）
# 为 5.3a 每批写 tmp_B{N}_cs_{tag}.json 和 tmp_B{N}_plan_{tag}.txt

# 示例：
def extract_cs(char_ids, scene_ids):
    return json.dumps({
        'style_setting': d['style_setting'],
        'character_assets': [c for c in d['character_assets'] if c['id'] in char_ids],
        'scene_assets': [s for s in d['scene_assets'] if s['id'] in scene_ids],
    }, ensure_ascii=False)

def extract_plan(plan_file, start, end):
    content = open(plan_file, encoding='utf-8').read()
    pattern = r'(\*\*B\d+-(\d+)\*\*.*?)(?=\*\*B\d+-\d+\*\*|\Z)'
    matches = re.findall(pattern, content, re.DOTALL)
    return '\n\n'.join(text.strip() for text, num in matches if start <= int(num) <= end)
```

## 第五步 — 5.3a layout 生成（Workflow，每批最多 6 条，最多 2 章并发）

> ⚠️ **运行期间请勿在 IDE 切换或打开任何文件，否则会中断 agent。**

**预提取要求**：每批 6 条对应的 `tmp_B{N}_cs_{tag}.json` 和 `tmp_B{N}_plan_{tag}.txt` 必须在第四步提前写好。

**存在性检查（必须同时验证 JSON 合法）**：

```javascript
// 存在性检查函数 —— 同时检查文件存在、非空、JSON 合法
const skip5a = (path) =>
`存在性检查（先执行）：Bash工具运行：
python3 -c "import json,os; p='${path}'; ok=os.path.exists(p) and os.path.getsize(p)>10; v=False; exec('try:\\n  json.load(open(p,encoding=\\"utf-8\\"))\\n  v=True\\nexcept: pass') if ok else None; print('EXISTS' if (ok and v) else 'MISSING')"
含EXISTS→输出"已存在跳过"立即结束。含MISSING→继续。`
```

**每批 agent prompt 模板**：

```javascript
// 每批 agent 只读 3 个文件：规则 + 预提取cs + 预提取plan
const layout5a = (n, idx, s, e, tag) =>
`${skip5a(`${projectDir}/draft/draft_B${n}_${tag}.json`)}
你是5.3a分镜规划节点，为第${n}章B${n}-${s}至B${n}-${e}（共${e-s+1}条）生成完整layout。
1. Read ${projectDir}/workflow/5.3a_storyboard_planning.md → 提取完整规则
2. Read ${projectDir}/draft/tmp_B${n}_cs_${tag}.json → 角色/场景/风格数据（预提取子集）
3. Read ${projectDir}/draft/tmp_B${n}_plan_${tag}.txt → 分配表（B${n}-${s}至B${n}-${e}）
   covered_sentences 只填英文原句，禁止包含中文
4. 仅为B${n}-${s}至B${n}-${e}生成完整layout（严格按规则阶段二）
   JSON要求：字符串内的双引号必须写成 \\"，禁止裸露未转义的双引号
5. Write到 ${projectDir}/draft/draft_B${n}_${tag}.json
   格式：{"storyboard_draft":[...]}，id格式B${n}-N，idx=${idx}`
```

**Workflow 结构**（最多 2 章并发，章内批次串行）：

```javascript
export const meta = {
  name: 'storyboard-5a',
  description: '5.3a layout 生成，6条/批，最多2章并发',
  phases: [{ title: '5.3a', detail: 'layout 生成' }],
}

// 示例：按章分轮，每轮最多 2 章并发，章内批次严格串行
const chapterBatches = {
  // 每章的批次列表，每批 ≤6 条
  // 例：总数16条的章 → [[1,6,'1_6'],[7,12,'7_12'],[13,16,'13_16']]
}
const rounds = [[1,2],[3,4],[5,6],[7,8],[9]]  // 按需调整

for (const round of rounds) {
  await parallel(round.map(n => () =>
    (async () => {
      for (const [s, e, tag] of chapterBatches[n]) {
        await agent(layout5a(n, chapterIdxMap[n], s, e, tag), {label:`5.3a-B${n}-${tag}`, phase:'5.3a'})
      }
    })()
  ))
}
```

**完成后在主对话合并并拆成 3 条/批供 5.3b 使用**：

```python
import json, os, re

project_dir = 'YOUR_PROJECT_DIR'

# 收集某章所有批次文件（按首条 id 数字排序）
def get_chapter_batch_files(n, batch_tags):
    files = []
    for tag in batch_tags:
        p = f'{project_dir}/draft/draft_B{n}_{tag}.json'
        if os.path.exists(p):
            files.append(p)
    return files

for n in chapters_to_merge:
    files = get_chapter_batch_files(n, batch_tags_for[n])
    merged = []
    for f in files:
        merged.extend(json.load(open(f, encoding='utf-8'))['storyboard_draft'])
    merged.sort(key=lambda x: int(re.search(r'-(\d+)$', x['id']).group(1)))
    seen = set(); out = []
    for e in merged:
        if e['id'] not in seen: seen.add(e['id']); out.append(e)
    with open(f'{project_dir}/draft/draft_B{n}.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'storyboard_draft': out}, f, ensure_ascii=False, indent=2); f.write('\n')
    print(f'B{n} draft: {len(out)}条')
    # 拆成 3 条一批供 5.3b
    for i in range(0, len(out), 3):
        batch = out[i:i+3]
        s = re.search(r'-(\d+)$', batch[0]['id']).group(1)
        e = re.search(r'-(\d+)$', batch[-1]['id']).group(1)
        with open(f'{project_dir}/draft/draft_B{n}_{s}_{e}.json', 'w', encoding='utf-8', newline='\n') as f:
            json.dump({'storyboard_draft': batch}, f, ensure_ascii=False, indent=2); f.write('\n')
    print(f'B{n} 拆为 {(len(out)+2)//3} 个3条批次')
```

## 第六步 — 5.3b prompt 生成（Workflow，严格串行，每批 3 条）

> ⚠️ **运行期间请勿在 IDE 切换或打开任何文件，这是 stall 的最主要原因。**

**最多 2 章并发，章内批次串行**。

**存在性检查（同时验证 JSON 合法）**：

```javascript
const skip5b = (path) =>
`存在性检查：Bash工具运行：
python3 -c "import json,os; p='${path}'; ok=os.path.exists(p) and os.path.getsize(p)>10; v=False; exec('try:\\n  json.load(open(p,encoding=\\"utf-8\\"))\\n  v=True\\nexcept: pass') if ok else None; print('EXISTS' if (ok and v) else 'MISSING')"
含EXISTS→输出"已存在跳过"立即结束。含MISSING→继续。`
```

**每批 agent prompt 模板**：

```javascript
const prompt5b = (n, draftFile, outFile) =>
`${skip5b(`${projectDir}/draft/${outFile}`)}
你是5.3b prompt生成节点，将 ${draftFile} 中的所有条目扩写为prompt。
1. Read ${projectDir}/workflow/5.3b_prompt_generation.md → 提取完整规则
2. Read ${projectDir}/draft/tmp_B${n}_full_cs.json → 角色/场景/风格数据（预提取子集）
3. Read ${projectDir}/draft/${draftFile} → storyboard_draft数组（最多3条）
4. 逐条扩写为storyboard_assets（新增prompt字段，其余字段原样保留）
   JSON要求：字符串内的双引号必须写成 \\"，禁止裸露未转义的双引号
5. Write到 ${projectDir}/draft/${outFile}，格式：{"storyboard_assets":[...]}`
```

**Workflow 结构**（2 章并发，章内串行）：

```javascript
export const meta = {
  name: 'storyboard-5b',
  description: '5.3b prompt 生成，3条/批，2章并发章内串行',
  phases: [{ title: '5.3b', detail: 'prompt 生成' }],
}

const chapterPairs = [[1,2],[3,4],[5,6],[7,8],[9]]  // 按需调整

for (const pair of chapterPairs) {
  await parallel(pair.map(n => () =>
    (async () => {
      for (const draftFile of allBatches[n]) {
        const outFile = draftFile.replace('draft_', 'assets_')
        await agent(prompt5b(n, draftFile, outFile), {label:`5.3b-B${n}-${draftFile}`, phase:'5.3b'})
      }
    })()
  ))
}
```

**重要**：如果中途失败，直接用 `resumeFromRunId` 断点续跑——已完成的批次会因为存在性检查而秒级跳过。

**兜底方案（agent 持续 stall 时）**：当某批次经过 2 次 retry 仍然 stall，直接在**主对话**生成 prompt 并用 Python Write 文件——主对话没有 180 秒超时限制：

```python
# 示例：直接生成 prompt 写入文件，绕开 agent 超时
import json

project_dir = 'YOUR_PROJECT_DIR'
draft = json.load(open(f'{project_dir}/draft/draft_BN_s_e.json', encoding='utf-8'))
items = draft['storyboard_draft']

# 根据 layout 内容逐条写 prompt（7段格式：①构图与镜头 ②动作与关系 ③场景 ④光影 ⑤主体与角色 ⑥风格与媒介 ⑦约束条件）
prompts = {
    'BN-X': "构图与镜头：...\n\n动作与关系：...\n\n场景：...\n\n光影与色彩：...\n\n主体与角色：...\n\n风格与媒介：...\n\n约束条件：...",
}

output = {'storyboard_assets': []}
for item in items:
    entry = dict(item)
    entry['prompt'] = prompts[item['id']]
    output['storyboard_assets'].append(entry)

with open(f'{project_dir}/draft/assets_BN_s_e.json', 'w', encoding='utf-8', newline='\n') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(f'写入成功: {len(output["storyboard_assets"])} 条')
```

## 第七步 — 合并 assets 并 QC（主对话 + Workflow 串行）

**合并**（主对话 Python 完成）：

```python
import json, os, re

project_dir = 'YOUR_PROJECT_DIR'

# 先检测并清理破损 JSON 文件
def is_valid_json(path):
    if not os.path.exists(path) or os.path.getsize(path) < 10:
        return False
    try:
        json.load(open(path, encoding='utf-8'))
        return True
    except:
        return False

for n in chapters_to_merge:
    # 汇总该章所有批次 assets 文件
    merged = []
    for df in batch_draft_files_for[n]:
        af = df.replace('draft_', 'assets_')
        path = f'{project_dir}/draft/{af}'
        if is_valid_json(path):
            merged.extend(json.load(open(path, encoding='utf-8'))['storyboard_assets'])
        else:
            print(f'⚠️ {af} 缺失或破损，跳过')
    merged.sort(key=lambda x: int(re.search(r'-(\d+)$', x['id']).group(1)))
    seen = set(); out = []
    for e in merged:
        if e['id'] not in seen: seen.add(e['id']); out.append(e)
    with open(f'{project_dir}/draft/assets_B{n}.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'storyboard_assets': out}, f, ensure_ascii=False, indent=2); f.write('\n')
    print(f'B{n} assets: {len(out)}条')
```

**QC**（Workflow 串行，每章一个 agent，读取 tmp_B{N}_full_cs.json 而非完整 char_scene_info.json）：

必检清单：
- L1-L4：layout 5段标签 + 镜头4要素 + 逐格预算 + 比例锚点
- P1-P5：prompt 7段标签 + 场景指纹 + 无内部ID + 角色外观 + 文字声明
- C1：covered_sentences ≤ 6句
- C2：每条有且仅有 6 个字段

发现问题立即修复写回，修复后重检确认。

## 第八步 — 合并到 output.json

```python
import json, glob, re

out_path = f'{projectDir}/output.json'
output = json.load(open(out_path, encoding='utf-8'))
existing_ids = {a['id'] for a in output['storyboard_assets']}
added = 0
for n in sorted_chapters:
    data = json.load(open(f'{projectDir}/draft/assets_B{n}.json', encoding='utf-8'))
    for entry in data['storyboard_assets']:
        if entry['id'] not in existing_ids:
            output['storyboard_assets'].append(entry)
            existing_ids.add(entry['id'])
            added += 1
output['storyboard_assets'].sort(key=lambda x: (int(x['id'].split('-')[0][1:]), int(x['id'].split('-')[1])))
with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(output, f, ensure_ascii=False, indent=2); f.write('\n')
print(f'已合并 {added} 条，当前共 {len(output["storyboard_assets"])} 条')

# 编码体检
with open(out_path, 'rb') as f: raw = f.read()
print('U+FFFD残留:', raw.count(b'\xef\xbf\xbd'))
raw.decode('utf-8', errors='strict'); print('严格UTF-8：通过')
print('BOM：', '存在' if raw.startswith(b'\xef\xbb\xbf') else '无')
crlf = raw.count(b'\r\n'); lf = raw.count(b'\n') - crlf
print(f'CRLF={crlf} LF-only={lf}')
```

## 故障排查

| 症状 | 原因 | 解法 |
|------|------|------|
| agent stalled（3分钟无输出） | **IDE 切换/打开文件**（最常见原因） | Workflow 运行期间不要操作 IDE |
| agent stalled | 5.3a 批次超过 6 条，输出量过大 | 减少到 ≤6 条/批 |
| agent stalled | 5.3b 批次超过 3 条，输出量过大 | 减少到 3 条/批 |
| `[Request interrupted by user]` | IDE 切换文件触发中断 | Workflow 运行时不动 IDE |
| `[Request interrupted by user]` | 并发超过 2 个 | 减少到最多 2 个并发 |
| JSON broken（`Expecting ',' delimiter`） | prompt 字符串内有未转义双引号 | 删除该批次文件；agent prompt 里加提醒"字符串内双引号必须写成 \\""；或改用主对话兜底方案 |
| 存在性检查误判为已存在 | 只检查了文件大小，未验证 JSON 合法性 | 存在性检查必须用 `try: json.load()` 验证，破损文件应视为 MISSING |
| 某批次经 2 次 retry 仍 stall | 输出量超限或持续 IDE 干扰 | 用主对话兜底方案直接生成 prompt 写文件（见第六步） |
