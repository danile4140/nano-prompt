---
name: storyboard-generator
description: 使用 Nano Banana 2 工作流（5.3a 分镜规划 + prompt 生成合并节点）从英文原著生成分镜。当用户要求生成分镜、跑流程、处理章节、或从 input.txt 生成 output.json 时使用本 skill。即使用户只说"生成分镜"、"跑一下"、"run"也应触发。
---

# 分镜生成器

将英文章节依次经过 5.3a（分镜规划 + prompt 直接生成）→ 质量检查两个阶段。

## 关键约束（必读，违反必失败）

1. **5.3a 每批最多 4 条**（合并了规划和 prompt 生成，输出量更大，4 条是实测上限）
2. **Workflow 并发上限：2 个**（更多并发会互相触发中断，哪怕你不动 IDE）
3. **char_scene_info.json 不能直接传给 agent**（51KB 太大）——必须在主对话预提取相关章节的角色/场景子集，写入 `draft/tmp_B{N}_full_cs.json`，让 agent 只读小文件
4. **每个 agent 只读 3 个文件**：规则文件 + 预提取 cs 文件 + draft 批次文件
5. **每个批次文件写入前必须做存在性检查**，已存在且 JSON 合法则跳过（必须同时验证 JSON 可解析，不能只检查文件大小）
6. **不要换模型**：必须用 sonnet，不要改为 haiku（质量不达标）
7. **运行 Workflow 期间禁止在 IDE 切换/打开文件**：IDE 文件操作会触发 `[Request interrupted by user]` 中断 agent，这是最主要的 stall 原因
8. **兜底方案禁止用 Python 超长字符串字面量写 prompt**：Write 工具写入超长单行字符串时会引入字符损坏（如 `——` 变成 `\xef\xbf\xbd`），且 prompt 中含英文引号（如 `"I can jump"` `"No one must see me"`）会破坏 Python 语法。**必须用 `"\n".join([...])` 列表方式逐段组合 prompt**，每段一个列表元素（见第五步兜底方案）

## 文件约定

| 文件 | 作用 |
|------|------|
| `input.txt` | 原文，章节以 `从 B{N}-1 开始编号` 标记分隔 |
| `char_scene_info.json` | 完整角色/场景/风格数据（不直接传给 agent） |
| `draft/plan_B{N}.md` | 阶段一输出：句子分配表（含中文译文） |
| `draft/assets_B{N}_{s}_{e}.json` | 5.3a 批次输出：B{N}-{s} 至 B{N}-{e} 的 storyboard_assets |
| `draft/assets_B{N}.json` | 合并后的完整 assets |
| `draft/tmp_B{N}_cs_{tag}.json` | 预提取的批次角色/场景子集（5.3a 用） |
| `draft/tmp_B{N}_plan_{tag}.txt` | 预提取的批次分配表条目（5.3a 用） |
| `draft/tmp_B{N}_full_cs.json` | 预提取的章节全量角色/场景子集（QC 用） |
| `output.json` | 最终合并结果（`storyboard_assets` 数组） |
| `workflow/5.3a_storyboard_planning.md` | 5.3a 规则（agent 直接 Read） |

## 第一步 — 准备工作（主对话完成，不启动 agent）

1. **读取 `input.txt`**，按 `从 B(\d+)-1 开始编号` 标记切分章节。
2. **读取 `char_scene_info.json`**，确认存在三个字段。
3. **检查 `output.json`**，不存在则创建 `{ "storyboard_assets": [] }`。
4. **创建 `draft/`** 目录（若不存在）。
5. **过滤章节**：跳过 `output.json` 中已有对应首条 ID（如 `B8-1`）的章节。
6. **预提取 char_scene 子集**（Python 内联完成）：
   - 分析每章涉及的角色和场景 ID，从 `char_scene_info.json` 提取子集
   - 写入 `draft/tmp_B{N}_full_cs.json`（供 QC 使用）
   - 每个 5.3a 批次也写对应的 `draft/tmp_B{N}_cs_{tag}.json` 和 `draft/tmp_B{N}_plan_{tag}.txt`

## 第二步 — 生成分拆计划（Workflow，各章并发）

每章 1 个 agent，最多 2 章并发。agent 只读：规则文件 + char_scene_info.json（此步骤可读完整文件，因为不生成大量输出）。

```javascript
export const meta = {
  name: 'storyboard-plan',
  description: '生成分镜分拆计划，仅执行句子分配，不生成 prompt',
  phases: [{ title: '分拆计划', detail: '逐章节句子分配并输出计划文件' }],
}

const { chapters, projectDir } = args

await parallel(chapters.map(chapter => async () => {
  await agent(
    `你的任务是执行 5.3a 分镜规划的【阶段一：句子分配】，不生成任何 prompt 内容。

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

## 第三步 — 汇总计划（自动继续）

读取所有 `draft/plan_B{N}.md`，在主对话输出每章分镜数量汇总表，然后**直接继续**进入第四步，不等待用户确认。

## 第四步 — 预提取小文件（主对话完成）

用 Python 内联完成，不启动 agent：

```python
import json, re

d = json.load(open(f'{projectDir}/char_scene_info.json', encoding='utf-8'))

# 分析每章涉及的角色/场景（根据 plan 文件中出现的 ID 或手动指定）
# 为每章写 tmp_B{N}_full_cs.json（全量供 QC 使用）
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

## 第五步 — 5.3a 生成（Workflow，每批最多 4 条，最多 2 章并发）

> ⚠️ **运行期间请勿在 IDE 切换或打开任何文件，否则会中断 agent。**

**预提取要求**：每批 4 条对应的 `tmp_B{N}_cs_{tag}.json` 和 `tmp_B{N}_plan_{tag}.txt` 必须在第四步提前写好。

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
const assets5a = (n, idx, s, e, tag) =>
`${skip5a(`${projectDir}/draft/assets_B${n}_${tag}.json`)}
你是5.3a分镜规划节点，为第${n}章B${n}-${s}至B${n}-${e}（共${e-s+1}条）生成完整 storyboard_assets（含 prompt，layout 为空字符串）。
1. Read ${projectDir}/workflow/5.3a_storyboard_planning.md → 提取完整规则
2. Read ${projectDir}/draft/tmp_B${n}_cs_${tag}.json → 角色/场景/风格数据（预提取子集）
3. Read ${projectDir}/draft/tmp_B${n}_plan_${tag}.txt → 分配表（B${n}-${s}至B${n}-${e}）
   covered_sentences 只填英文原句，禁止包含中文
4. 为B${n}-${s}至B${n}-${e}生成完整 storyboard_assets，每条包含 id/character_refs/scene_refs/covered_sentences/layout(空字符串)/prompt
   JSON要求：字符串内的双引号必须写成 \\"，禁止裸露未转义的双引号
5. Write到 ${projectDir}/draft/assets_B${n}_${tag}.json
   格式：{"storyboard_assets":[...]}，id格式B${n}-N，idx=${idx}`
```

**Workflow 结构**（最多 2 章并发，章内批次串行）：

```javascript
export const meta = {
  name: 'storyboard-5a',
  description: '5.3a 分镜规划+prompt 生成，4条/批，最多2章并发',
  phases: [{ title: '5.3a', detail: '分镜规划+prompt 生成' }],
}

// 示例：按章分轮，每轮最多 2 章并发，章内批次严格串行
const chapterBatches = {
  // 每章的批次列表，每批 ≤4 条
  // 例：总数12条的章 → [[1,4,'1_4'],[5,8,'5_8'],[9,12,'9_12']]
}
const rounds = [[1,2],[3,4],[5,6],[7,8],[9]]  // 按需调整

for (const round of rounds) {
  await parallel(round.map(n => () =>
    (async () => {
      for (const [s, e, tag] of chapterBatches[n]) {
        await agent(assets5a(n, chapterIdxMap[n], s, e, tag), {label:`5.3a-B${n}-${tag}`, phase:'5.3a'})
      }
    })()
  ))
}
```

**完成后在主对话合并 assets**：

```python
import json, os, re

project_dir = 'YOUR_PROJECT_DIR'

def get_chapter_batch_files(n, batch_tags):
    files = []
    for tag in batch_tags:
        p = f'{project_dir}/draft/assets_B{n}_{tag}.json'
        if os.path.exists(p):
            files.append(p)
    return files

for n in chapters_to_merge:
    files = get_chapter_batch_files(n, batch_tags_for[n])
    merged = []
    for f in files:
        merged.extend(json.load(open(f, encoding='utf-8'))['storyboard_assets'])
    merged.sort(key=lambda x: int(re.search(r'-(\d+)$', x['id']).group(1)))
    seen = set(); out = []
    for e in merged:
        if e['id'] not in seen: seen.add(e['id']); out.append(e)
    with open(f'{project_dir}/draft/assets_B{n}.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'storyboard_assets': out}, f, ensure_ascii=False, indent=2); f.write('\n')
    print(f'B{n} assets: {len(out)}条')
```

**兜底方案（agent 持续 stall 时）**：当某批次经过 2 次 retry 仍然 stall，直接在**主对话**生成 prompt 并用 Python Write 文件——主对话没有 180 秒超时限制。

**⚠️ 必须用 `"\n".join([...])` 列表方式写 prompt**，禁止写超长字符串字面量：

```python
# 兜底方案：在主对话生成 prompt，写入 assets 文件
import json

project_dir = 'YOUR_PROJECT_DIR'
plan = open(f'{project_dir}/draft/tmp_BN_plan_tag.txt', encoding='utf-8').read()

# ⚠️ 必须用 "\n".join([...]) 逐段拼接，禁止超长单行字符串字面量
# 每个列表元素对应 prompt 的一段（七段：构图/动作/场景/光影/角色/风格/约束）
# 如果段落内含有英文引号（如 "Kansas"），改写为不含引号的形式或用中文括号
prompts = {
    'BN-X': "\n".join([
        "构图与镜头：...",
        "",
        "动作与关系：...",
        "",
        "场景：...",
        "",
        "光影与色彩：...",
        "",
        "主体与角色：...",
        "",
        "风格与媒介：...",
        "",
        "约束条件：...",
    ]),
}

cs = json.load(open(f'{project_dir}/draft/tmp_BN_full_cs.json', encoding='utf-8'))
# 从 plan 文件中找到对应条目，构造 storyboard_assets 条目
output = {'storyboard_assets': []}
# ... 按需填充 id/character_refs/scene_refs/covered_sentences/layout/prompt

with open(f'{project_dir}/draft/assets_BN_s_e.json', 'w', encoding='utf-8', newline='\n') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(f'写入成功: {len(output["storyboard_assets"])} 条')
```

## 第六步 — 合并 assets 并 QC（主对话 + Workflow 串行）

**合并**（主对话 Python 完成）：

```python
import json, os, re

project_dir = 'YOUR_PROJECT_DIR'

def is_valid_json(path):
    if not os.path.exists(path) or os.path.getsize(path) < 10:
        return False
    try:
        json.load(open(path, encoding='utf-8'))
        return True
    except:
        return False

for n in chapters_to_merge:
    merged = []
    for af in batch_assets_files_for[n]:
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
- P1-P5：prompt 7段标签 + 场景指纹 + 无内部ID + 角色外观 + 文字声明
- C1：covered_sentences ≤ 6句
- C2：每条有且仅有 6 个字段（id/character_refs/scene_refs/covered_sentences/layout/prompt）
- C3：layout 字段值为空字符串 `""`

发现问题立即修复写回，修复后重检确认。

## 第七步 — 合并到 output.json

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

**如果 U+FFFD 残留 > 0**，执行以下修复流程（必须根据上下文还原原字符，禁止用空格或句号替代）：

```python
# U+FFFD 修复：定位 → 分析上下文 → 还原原字符
with open(out_path, 'rb') as f: raw = f.read()
text = raw.decode('utf-8', errors='replace')

import re
for m in re.finditer('[�]+', text):
    ctx = text[max(0, m.start()-20):m.end()+20]
    print(f'pos={m.start()} len={m.end()-m.start()}: {repr(ctx)}')

replacements = [
    # ('损坏片段', '正确原文'),   # 根据实际上下文填写
]
for old, new in replacements:
    text = text.replace(old, new)

assert '�' not in text, "仍有残留乱码，继续修复"
with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)
print('乱码修复完成')
```

## 故障排查

| 症状 | 原因 | 解法 |
|------|------|------|
| agent stalled（3分钟无输出） | **IDE 切换/打开文件**（最常见原因） | Workflow 运行期间不要操作 IDE |
| agent stalled | 5.3a 批次超过 4 条，输出量过大 | 减少到 ≤4 条/批 |
| `[Request interrupted by user]` | IDE 切换文件触发中断 | Workflow 运行时不动 IDE |
| `[Request interrupted by user]` | 并发超过 2 个 | 减少到最多 2 个并发 |
| JSON broken（`Expecting ',' delimiter`） | prompt 字符串内有未转义双引号 | 删除该批次文件；agent prompt 里加提醒"字符串内双引号必须写成 \\""；或改用主对话兜底方案 |
| 存在性检查误判为已存在 | 只检查了文件大小，未验证 JSON 合法性 | 存在性检查必须用 `try: json.load()` 验证，破损文件应视为 MISSING |
| 某批次经 2 次 retry 仍 stall | 输出量超限或持续 IDE 干扰 | 用主对话兜底方案直接生成 prompt 写文件（见第五步） |
| 兜底方案 Python 脚本 `SyntaxError` | prompt 字符串内含英文引号（如 `"I can jump"`）破坏 Python 语法 | 改用 `"\n".join([...])` 列表方式；将英文引号改写为无引号形式 |
| 兜底方案写入后出现乱码（`—` 变 `���`） | Write 工具写入超长单行字符串时字符损坏 | 改用 `"\n".join([...])` 列表方式，每段不超过一行 |
| output.json 合并后 U+FFFD 残留 | QC agent 写回时引入字符损坏 | 执行第七步的 U+FFFD 修复流程，根据上下文还原原字符 |
