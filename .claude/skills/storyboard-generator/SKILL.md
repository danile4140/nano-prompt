---
name: storyboard-generator
description: 使用 Nano Banana 2 工作流（5.3a 分镜规划 + 5.3b prompt 生成）从英文原著生成分镜。当用户要求生成分镜、跑流程、处理章节、或从 input.txt 生成 output.json 时使用本 skill。即使用户只说"生成分镜"、"跑一下"、"run"也应触发。
---

# 分镜生成器

将英文章节依次经过 5.3a（分镜规划）→ 5.3b（prompt 生成）→ 质量检查三个阶段，通过 Workflow 并发处理所有章节。

## 文件约定

| 文件 | 作用 |
|------|------|
| `input.txt` | 原文，章节以 `从 B{N}-1 开始编号` 标记分隔 |
| `char_scene_info.json` | 必须包含 `character_assets`、`scene_assets`、`style_setting` |
| `draft/draft_B{N}.json` | 5.3a 每章输出（中间文件） |
| `draft/assets_B{N}.json` | 5.3b 每章输出（中间文件） |
| `output.json` | 最终合并结果（`storyboard_assets` 数组） |
| `workflow/5.3a_storyboard_planning.md` | 5.3a 规则（运行时原文读取） |
| `workflow/5.3b_prompt_generation.md` | 5.3b 规则（运行时原文读取） |

## 第一步 — 准备工作（在启动 Workflow 前自行完成）

在启动任何 agent 之前，先完成以下所有操作：

1. **读取 `input.txt`**，按 `从 B(\d+)-1 开始编号` 标记切分章节。
   - 每章结构：`{ n: <章节编号>, idx: <n-1>, text: <两标记之间的内容，去首尾空白> }`
   - 如无标记，整个文件视为第 B1 章（n=1，idx=0）。

2. **读取 `char_scene_info.json`**，确认存在 `character_assets`、`scene_assets`、`style_setting` 三个字段。

3. **检查 `output.json`**，不存在则创建 `{ "storyboard_assets": [] }`；收集已有 ID，支持断点续跑。

4. **创建 `draft/`** 目录（若不存在）。

5. **过滤章节**，跳过 `output.json` 中已完整存在对应 ID（如 `B8-1`）的章节。

6. **确定 `projectDir`**，即当前工作目录的绝对路径（如 `E:\coze-ai-nanobanana`），作为 `args` 的一部分传给 Workflow。

## 第二步 — 生成分拆计划（Workflow 1，轻量级）

启动一个只执行**阶段一**（句子分配）的轻量 Workflow，所有章节并发运行。

```javascript
export const meta = {
  name: 'storyboard-plan',
  description: '生成分镜分拆计划，仅执行句子分配，不生成 layout',
  phases: [{ title: '分拆计划', detail: '逐章节句子分配并输出计划文件' }],
}

const { chapters, projectDir } = args
log(`共 ${chapters.length} 章，开始生成分拆计划...`)

await parallel(chapters.map(chapter => async () => {
  await agent(
    `你的任务是执行 5.3a 分镜规划的【阶段一：句子分配】，不生成任何 layout 内容。

## 执行步骤

1. 用 Read 工具读取 ${projectDir}/workflow/5.3a_storyboard_planning.md
   - 提取 \`### 系统提示词\` 下方 \`\`\`text 代码块内的完整规则
   - 重点研读：§2 逐句覆盖、§3 节拍切分、§3b 句数上限、§4 必拆充要条件

2. 用 Read 工具读取 ${projectDir}/char_scene_info.json，获取 style_setting

3. 按规则对以下章节原文执行阶段一：
   - 将原文按句号/问号/感叹号切分，逐句标注"→ 归属哪条分镜"
   - 自检未覆盖句数 = 0

章节内容（第 ${chapter.n} 章，idx=${chapter.idx}）：
---
${chapter.text}
---

4. 将分配结果写入 ${projectDir}/draft/plan_B${chapter.n}.md，格式如下：

# 第 ${chapter.n} 章分镜规划

共 **N** 条分镜

## 分配表

**B${chapter.n}-1**（X 句）
- 分组依据：[节拍判断理由，如：同一场景同一时刻连续动作，无认知锚点切换，同节拍合并]
- 原文：
  1. "..."
  2. "..."

**B${chapter.n}-2**（X 句）
- 分组依据：[...]
- 原文：
  1. "..."

（每条分镜都按此格式输出，不得省略）

5. 计划文件写入完成后，重新读取 ${projectDir}/draft/plan_B${chapter.n}.md，为分配表中每条原文句子追加中文译文，更新写回文件。译文格式：在每条英文原句下方增加一行缩进的 "译：[中文译文]"，例如：
  1. "One evening, St John came to my house..."
     译：一天傍晚，圣约翰来到我家……
译文风格：忠实原文，通顺自然，不意译，不删减细节。`,
    { label: `计划-B${chapter.n}`, phase: '分拆计划' }
  )
  log(`✓ 第 ${chapter.n} 章分拆计划完成`)
}))
```

## 第三步 — 展示计划并等待确认

Workflow 1 完成后，读取所有 `draft/plan_B{N}.md` 文件，在对话中展示以下汇总信息：

- 每章分了多少条分镜（从文件首行 `共 **N** 条分镜` 提取）
- 对应计划文件的完整路径（供用户自行查看详细分配和译文）

示例输出格式：
```
分拆计划已生成：
- 第 8 章：32 条分镜 → draft/plan_B8.md
- 第 9 章：29 条分镜 → draft/plan_B9.md

请查看计划文件确认分组是否合理，回复「继续」后开始生成完整分镜内容。如需调整，说明哪章哪条需要修改。
```

**收到用户确认后**再执行第四步。若用户提出调整意见，根据其指令修改对应 `draft/plan_B{N}.md`，修改后再次展示汇总并询问确认。

## 第四步 — 生成完整分镜（Workflow 2，用户确认后执行）

按以下结构编写并运行主 Workflow。传入的 `args` 与第二步相同：`{ chapters: <第一步解析的章节数组>, projectDir: <项目绝对路径> }`——直接复用，无需重新解析 input.txt。

```javascript
export const meta = {
  name: 'storyboard-generator',
  description: '基于已确认的分拆计划，生成完整分镜 layout + prompt 并检查',
  phases: [
    { title: '规划 (5.3a)', detail: '基于计划文件生成完整 layout' },
    { title: '生成 (5.3b)', detail: '逐章节扩写最终 prompt' },
    { title: '检查', detail: '逐章节质量校验与自动修复' },
  ],
}

const { chapters, projectDir } = args

log(`共 ${chapters.length} 章待处理：${chapters.map(c => 'B' + c.n).join('、')}`)

const results = await pipeline(
  chapters,

  // ── 阶段一：5.3a 阶段二（基于已确认计划生成 layout） ─────────────────────
  async (chapter) => {
    log(`第 ${chapter.n} 章 → 开始生成 layout...`)
    const output = await agent(
      `你的任务是作为"5.3a 分镜规划节点"的【阶段二：layout 生成】，基于已确认的句子分配计划，为每条分镜生成完整 layout。

## 执行步骤

1. 用 Read 工具读取 ${projectDir}/workflow/5.3a_storyboard_planning.md
   - 提取完整系统规则——一字不改，不裁剪，不概括
   - 本次只执行阶段二（layout 设计），句子分配已在计划文件中确定，直接使用

2. 用 Read 工具读取 ${projectDir}/char_scene_info.json
   - 提取 character_assets、scene_assets、style_setting

3. 用 Read 工具读取 ${projectDir}/draft/plan_B${chapter.n}.md
   - 这是已经过用户确认的分配表，covered_sentences 必须严格按此文件的英文原句填入
   - 禁止重新判断句子分配，只基于此计划生成 layout
   - 计划文件中每句英文下方有"译：..."中文译文，**仅供理解原文语义参考，禁止写入 covered_sentences 或 layout**
   - covered_sentences 只能填英文原句（即计划文件中带编号的引号内容），不得包含任何中文

4. 为每条分镜生成完整 layout（严格按照系统规则的阶段二要求）

5. 用 Write 工具将结果写入 ${projectDir}/draft/draft_B${chapter.n}.json
   - 只输出合法 JSON，顶层字段只保留 storyboard_draft
   - id 格式：B${chapter.n}-{{seq}}，idx=${chapter.idx}
   - 如 layout 字段含未转义双引号导致 JSON 非法，写入前用以下 Python 脚本修复：
     \`\`\`python
     import json
     def fix(text):
         r=[]; i=0; ins=False; esc=False
         while i<len(text):
             c=text[i]
             if esc: r.append(c); esc=False
             elif c==chr(92): r.append(c); esc=True
             elif c==chr(34):
                 if not ins: ins=True; r.append(c)
                 else:
                     j=i+1
                     while j<len(text) and text[j] in ' \\t\\r\\n': j+=1
                     if j<len(text) and text[j] in ',}]:\\n\\r': ins=False; r.append(c)
                     else: r.append(chr(92)); r.append(chr(34))
             else: r.append(c)
             i+=1
         return ''.join(r)
     path='${projectDir}/draft/draft_B${chapter.n}.json'
     data=open(path,encoding='utf-8').read()
     fixed=fix(data)
     json.loads(fixed)
     open(path,'w',encoding='utf-8',newline='\\n').write(fixed)
     \`\`\`

6. 文件写入成功后，在回复的**最后一行**单独输出：
   DRAFT_COUNT: N（N 为 storyboard_draft 数组的实际条数）`,
      { label: `5.3a-B${chapter.n}`, phase: '规划 (5.3a)' }
    )
    const match = output && output.match(/DRAFT_COUNT:\s*(\d+)/)
    const count = match ? parseInt(match[1]) : '?'
    log(`✓ 第 ${chapter.n} 章 layout 生成完成：共 ${count} 条分镜`)
    return { chapter, count }
  },

  // ── 阶段二：5.3b prompt 生成 ───────────────────────────────────────────
  async ({ chapter, count }) => {
    log(`第 ${chapter.n} 章 → 开始生成 prompt（共 ${count} 条分镜）...`)
    await agent(
      `你的任务是作为"5.3b prompt 生成节点"，严格遵守系统提示词的每一条规则，将第 ${chapter.n} 章的分镜规划扩写为最终 prompt。

## 执行步骤

1. 用 Read 工具读取 ${projectDir}/workflow/5.3b_prompt_generation.md
   - 找到 \`### 系统提示词\` 下方的 \`\`\`text 代码块
   - 提取完整内容作为你的系统规则——一字不改，不裁剪，不概括

2. 用 Read 工具读取 ${projectDir}/char_scene_info.json
   - 提取 character_assets、scene_assets、style_setting

3. 用 Read 工具读取 ${projectDir}/draft/draft_B${chapter.n}.json
   - 提取 storyboard_draft 数组

4. 严格按照系统规则，逐条将 storyboard_draft 扩写为 storyboard_assets（新增 prompt 字段，其余字段原样保留）

5. 用 Write 工具将结果写入 ${projectDir}/draft/assets_B${chapter.n}.json
   - 只输出合法 JSON，顶层字段只保留 storyboard_assets
   - 如有 JSON 非法（prompt/layout 字段含未转义双引号），写入前用以下脚本修复：
     \`\`\`python
     import json
     def fix(text):
         r=[]; i=0; ins=False; esc=False
         while i<len(text):
             c=text[i]
             if esc: r.append(c); esc=False
             elif c==chr(92): r.append(c); esc=True
             elif c==chr(34):
                 if not ins: ins=True; r.append(c)
                 else:
                     j=i+1
                     while j<len(text) and text[j] in ' \\t\\r\\n': j+=1
                     if j<len(text) and text[j] in ',}]:\\n\\r': ins=False; r.append(c)
                     else: r.append(chr(92)); r.append(chr(34))
             else: r.append(c)
             i+=1
         return ''.join(r)
     path='${projectDir}/draft/assets_B${chapter.n}.json'
     data=open(path,encoding='utf-8').read()
     fixed=fix(data)
     json.loads(fixed)
     open(path,'w',encoding='utf-8',newline='\\n').write(fixed)
     \`\`\``,
      { label: `5.3b-B${chapter.n}`, phase: '生成 (5.3b)' }
    )
    log(`✓ 第 ${chapter.n} 章 prompt 生成完成`)
    return chapter
  },

  // ── 阶段三：质量检查 + 自动修复 ──────────────────────────────────────────
  async (chapter) => {
    log(`第 ${chapter.n} 章 → 开始质量检查...`)
    await agent(
    `你是分镜质量检查员兼修复员。检查第 ${chapter.n} 章生成结果，**发现问题必须当场修复**，不需要等待确认。

## 第一轮：读取文件并检查

1. 用 Read 工具读取 ${projectDir}/workflow/5.3a_storyboard_planning.md（备用：修复 layout 时参考规则）
2. 用 Read 工具读取 ${projectDir}/workflow/5.3b_prompt_generation.md（备用：修复 prompt 时参考规则）
3. 用 Read 工具读取 ${projectDir}/char_scene_info.json（备用：修复时需要角色/场景数据）
4. 用 Read 工具读取 ${projectDir}/draft/draft_B${chapter.n}.json
5. 用 Read 工具读取 ${projectDir}/draft/assets_B${chapter.n}.json

## 必检清单（逐条检查，不得跳过）

**[layout 检查]**
□ L1. 每条 layout 使用 5 段中文标签：「构图与镜头：」「动作与关系：」「场景：」「光影与色彩：」「主体与角色：」
□ L2. 每条 layout 的「构图与镜头」段包含：镜头位于何处/看向何处、前中后景、主体朝向、背景锚点（4 问答）
□ L3. 每条 layout 的「主体与角色」段包含逐格角色预算（"左格可辨识 X 人…"）
□ L4. 每条 layout 的「构图与镜头」段末尾包含逐角色比例锚点

**[prompt 检查]**
□ P1. 每条 prompt 使用 7 段中文标签，段间用空行（\\n\\n）分隔
□ P2. prompt 的「约束条件」段末尾有「场景指纹：[元素A]+[元素B]+[元素C]，位置形态不变」一行
□ P3. prompt 文本中不包含内部 ID（C1/C2/S1/B${chapter.n}-x 等格式）
□ P4. 每条 prompt 的「主体与角色」段展开了角色外观（发色发型 + 服装主色 + 1 个高辨识度细节）
□ P5. 有气泡/英文内容的 prompt 结尾有"英文拼写正确，无气泡外浮动文字…手写体风格"；无英文的有"画面内无任何浮动文字…"

**[覆盖检查]**
□ C1. 每条 storyboard_assets 的 covered_sentences 句数 ≤ 6
□ C2. 每条 storyboard_assets 有且只有 6 个字段（id/character_refs/scene_refs/covered_sentences/layout/prompt）

## 第二轮：修复（发现任何问题立即执行，无需确认）

**修复依据**：
- layout 问题（L1-L4）→ 以 5.3a_storyboard_planning.md 中系统提示词原文为唯一规则依据，修改对应条目的 layout 字段
- prompt 问题（P1-P5）→ 以 5.3b_prompt_generation.md 中系统提示词原文为唯一规则依据，结合 char_scene_info.json，修改对应条目的 prompt 字段
- C2 字段数量错误 → 保留且只保留 6 个规定字段
- C1 句数超限（≥7 句） → 标记为"需人工复查"

修复后用 Write 工具覆盖写回原文件。写入前必须确保 JSON 合法——如含未转义双引号，用以下脚本修复后再写：
\`\`\`python
import json
def fix(text):
    r=[]; i=0; ins=False; esc=False
    while i<len(text):
        c=text[i]
        if esc: r.append(c); esc=False
        elif c==chr(92): r.append(c); esc=True
        elif c==chr(34):
            if not ins: ins=True; r.append(c)
            else:
                j=i+1
                while j<len(text) and text[j] in ' \t\r\n': j+=1
                if j<len(text) and text[j] in ',}]:\n\r': ins=False; r.append(c)
                else: r.append(chr(92)); r.append(chr(34))
        else: r.append(c)
        i+=1
    return ''.join(r)
path='<目标文件路径>'  # draft_B{N}.json 或 assets_B{N}.json
data=open(path,encoding='utf-8').read()
fixed=fix(data)
json.loads(fixed)  # 验证
open(path,'w',encoding='utf-8',newline='\n').write(fixed)
\`\`\`

## 第三轮：验证修复结果

修复写入后，重新读取文件，再跑一遍必检清单，确认所有问题已消除。

## 最终输出

- 全部通过（含修复后通过）：输出"✓ 第 ${chapter.n} 章检查通过，共 X 条分镜"
- 仍有无法自动修复的问题：输出"⚠ 第 ${chapter.n} 章：以下问题需人工复查：[具体问题列表]"`,
      { label: `检查修复-B${chapter.n}`, phase: '检查' }
    )
    log(`✓ 第 ${chapter.n} 章全部完成`)
    return chapter
  }
)

return results.filter(Boolean)
```
## 第五步 — 合并到 output.json

Workflow 完成后，用 Python 内联执行合并：

```python
import json, re, glob

out_path = 'output.json'
output = json.load(open(out_path, encoding='utf-8'))
existing_ids = {a['id'] for a in output['storyboard_assets']}

# 按章节编号排序收集所有中间文件
asset_files = sorted(
    glob.glob('draft/assets_B*.json'),
    key=lambda f: int(re.search(r'B(\d+)', f).group(1))
)

added = 0
for path in asset_files:
    data = json.load(open(path, encoding='utf-8'))
    for entry in data.get('storyboard_assets', []):
        if entry['id'] not in existing_ids:
            output['storyboard_assets'].append(entry)
            existing_ids.add(entry['id'])
            added += 1

with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
    f.write('\n')

print(f'已合并 {added} 条新分镜，当前共 {len(output["storyboard_assets"])} 条')
```

然后跑编码体检：

```bash
python3 -c "
path='output.json'
with open(path,'rb') as f: data=f.read()
print('U+FFFD 残留:', data.count(b'\xef\xbf\xbd'))
data.decode('utf-8', errors='strict')
print('严格 UTF-8：通过')
print('BOM：', '存在' if data.startswith(b'\xef\xbb\xbf') else '无')
crlf=data.count(b'\r\n'); lf=data.count(b'\n')-crlf
print(f'CRLF={crlf} LF-only={lf}')
"
```

## 关键约束

- **严禁裁剪或改写** 5.3a / 5.3b 系统提示词——必须从文件原文读取，完整传入 agent
- **JSON 修复**：agent 输出 JSON 非法时（layout/prompt 字段含未转义双引号），用第一阶段的 `fix()` 函数修复后再继续
- **仅 LF 换行**：所有 JSON 输出文件必须使用 LF 换行（Python 写文件时传 `newline='\n'`）
- **禁止 ID 泄漏**：`prompt` 文本中不得出现 C1/S1/B8-1 等内部 ID，只允许出现在 `refs` 数组里
- **断点续跑**：若部分章节已在 `output.json` 中，跳过（通过检查 B{N}-1 是否存在判断）
