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

## 第二步 — 启动 Workflow

按以下结构编写并运行 Workflow，将章节数据和项目目录路径通过 `args` 传入。

```javascript
export const meta = {
  name: 'storyboard-generator',
  description: '通过 5.3a → 5.3b → 检查流水线并发处理所有章节，生成分镜',
  phases: [
    { title: '规划 (5.3a)', detail: '逐章节执行分镜规划' },
    { title: '生成 (5.3b)', detail: '逐章节扩写最终 prompt' },
    { title: '检查', detail: '逐章节质量校验' },
  ],
}

// args: { chapters: [{n, idx, text}], projectDir }
const { chapters, projectDir } = args

const results = await pipeline(
  chapters,

  // ── 阶段一：5.3a 分镜规划 ──────────────────────────────────────────────
  async (chapter) => {
    await agent(
      `你的任务是作为"5.3a 分镜规划节点"，严格遵守系统提示词的每一条规则，生成第 ${chapter.n} 章的 storyboard_draft。

## 执行步骤

1. 用 Read 工具读取 ${projectDir}/workflow/5.3a_storyboard_planning.md
   - 找到 \`### 系统提示词\` 下方的 \`\`\`text 代码块
   - 提取代码块内的完整内容作为你的系统规则——一字不改，不裁剪，不概括

2. 用 Read 工具读取 ${projectDir}/char_scene_info.json
   - 提取 character_assets、scene_assets、style_setting

3. 严格按照系统规则处理以下章节（idx=${chapter.idx}，id 格式 B${chapter.n}-{{seq}}）：

---
${chapter.text}
---

   **执行顺序硬性要求（来自规则的两阶段强制）**：
   - **先完成阶段一**：将原文按句号/问号/感叹号逐句切分，逐句标注"→ 归属哪条分镜"，形成完整分配表，自检"未覆盖句数 = 0"——等式不成立禁止进入下一步
   - **再进入阶段二**：按分配表设计每条分镜的 layout，covered_sentences 从分配表直接抄入，不得从 layout 反推
   - 禁止跳过阶段一直接写 layout

4. 用 Write 工具将结果写入 ${projectDir}/draft/draft_B${chapter.n}.json
   - 只输出合法 JSON，顶层字段只保留 storyboard_draft
   - 如果 layout 字段内有未转义的双引号导致 JSON 非法，写入前用以下 Python 脚本修复：
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
     json.loads(fixed)  # 验证合法性
     open(path,'w',encoding='utf-8',newline='\\n').write(fixed)
     \`\`\``,
      { label: `5.3a-B${chapter.n}`, phase: '规划 (5.3a)' }
    )
    return chapter
  },

  // ── 阶段二：5.3b prompt 生成 ───────────────────────────────────────────
  async (chapter) => {
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
   - 如有 JSON 非法（未转义双引号），同样用 fix 脚本修复后保存`,
      { label: `5.3b-B${chapter.n}`, phase: '生成 (5.3b)' }
    )
    return chapter
  },

  // ── 阶段三：质量检查 + 自动修复 ──────────────────────────────────────────
  async (chapter) => {
    await agent(
      `你是分镜质量检查员兼修复员。检查第 ${chapter.n} 章生成结果，**发现问题必须当场修复**，不需要等待确认。

## 第一轮：读取文件并检查

1. 用 Read 工具读取 ${projectDir}/workflow/5.3a_storyboard_planning.md（备用：修复 layout 时需要参考规则）
2. 用 Read 工具读取 ${projectDir}/workflow/5.3b_prompt_generation.md（备用：修复 prompt 时需要参考规则）
3. 用 Read 工具读取 ${projectDir}/char_scene_info.json（备用：修复时需要角色/场景数据）
4. 用 Read 工具读取 ${projectDir}/draft/draft_B${chapter.n}.json
5. 用 Read 工具读取 ${projectDir}/draft/assets_B${chapter.n}.json

## 必检清单（逐条检查，不得跳过）

**[layout 检查]**（检查 draft_B${chapter.n}.json 中每条 storyboard_draft）
□ L1. 每条 layout 使用 5 段中文标签：「构图与镜头：」「动作与关系：」「场景：」「光影与色彩：」「主体与角色：」（不得出现 ⑥⑦ 或"风格与媒介："/"约束条件："）
□ L2. 每条 layout 的「构图与镜头」段包含：镜头位于何处/看向何处、前中后景、主体朝向、背景锚点（4 问答）
□ L3. 每条 layout 的「主体与角色」段包含逐格角色预算（"左格可辨识 X 人…"）
□ L4. 每条 layout 的「构图与镜头」段末尾包含逐角色比例锚点

**[prompt 检查]**（检查 assets_B${chapter.n}.json 中每条 storyboard_assets）
□ P1. 每条 prompt 使用 7 段中文标签，段间用空行（\\n\\n）分隔：构图与镜头/动作与关系/场景/光影与色彩/主体与角色/风格与媒介/约束条件
□ P2. prompt 的「约束条件」段末尾有「场景指纹：[元素A]+[元素B]+[元素C]，位置形态不变」一行
□ P3. prompt 文本中不包含内部 ID（C1/C2/S1/B${chapter.n}-x/T1 等格式）
□ P4. 每条 prompt 的「主体与角色」段展开了角色外观（发色发型 + 服装主色 + 1 个高辨识度细节）
□ P5. 有气泡/英文内容的 prompt 结尾有"英文拼写正确，无气泡外浮动文字…手写体风格"；无英文的有"画面内无任何浮动文字…"

**[覆盖检查]**
□ C1. 每条 storyboard_assets 的 covered_sentences 句数 ≤ 6
□ C2. 每条 storyboard_assets 有且只有 6 个字段（id/character_refs/scene_refs/covered_sentences/layout/prompt）

## 第二轮：修复（发现任何问题立即执行，无需确认）

**修复依据**：
- layout 问题（L1-L4）→ 以 5.3a_storyboard_planning.md 中 `### 系统提示词` 代码块的原文为唯一规则依据，修改 draft_B${chapter.n}.json 中对应条目的 layout 字段
- prompt 问题（P1-P5）→ 以 5.3b_prompt_generation.md 中 `### 系统提示词` 代码块的原文为唯一规则依据，结合 char_scene_info.json，修改 assets_B${chapter.n}.json 中对应条目的 prompt 字段
- C2 字段数量错误 → 保留且只保留 6 个规定字段（id/character_refs/scene_refs/covered_sentences/layout/prompt）
- C1 句数超限（≥7 句） → 需要人工判断叙事拆分，标记为"需人工复查"

修复时严格按照规则文件原文执行，禁止自行概括或简化规则。修复后用 Write 工具覆盖写回原文件，写入前确保 JSON 合法（如含未转义引号先用 fix() 函数处理）。

## 第三轮：验证修复结果

修复写入后，重新读取文件，再跑一遍必检清单，确认所有问题已消除。

## 最终输出

- 全部通过（含修复后通过）：输出"✓ 第 ${chapter.n} 章检查通过，共 X 条分镜"
- 仍有无法自动修复的问题（如 C1 句数超限导致叙事逻辑需要人工判断）：输出"⚠ 第 ${chapter.n} 章：自动修复完成，以下问题需人工复查：[具体问题列表]"`,
      { label: `检查修复-B${chapter.n}`, phase: '检查' }
    )
    return chapter
  }
)

return results.filter(Boolean)
```

## 第三步 — 合并到 output.json

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
