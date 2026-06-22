---
name: char-scene-generator
description: 从英文原著（input.txt）按照 5.1/5.2 工作流规范生成角色与场景设定卡，输出到 char_scene_info.json。当用户要求"生成角色场景"、"生成 char_scene_info"、"分析原文生成角色和场景"、"跑 5.1 5.2"时触发。即使用户只说"生成角色"或"生成场景"也应触发。
---

# 角色与场景设定生成器

从 `input.txt` 读取英文原著，并行执行 5.1（角色）和 5.2（场景）节点，生成结果合并写入 `char_scene_info.json`。

完整规则见：
- `references/5.1_characters.md` — 角色生成规则（提取系统提示词 + 用户提示词模板）
- `references/5.2_scenes.md` — 场景生成规则（提取系统提示词 + 用户提示词模板）

---

## 第一步 — 准备（主对话完成）

1. 读取 `input.txt` 获取原著内容
2. 读取 `style_settings.txt` 获取风格设定（文件内容即为 `style_setting` 原文，整行读取，不做任何裁剪或改写）；若文件不存在则询问用户
3. 在 `draft/` 目录下创建临时文件存放位置（若不存在则创建）

---

## 第二步 — 并行生成（Workflow，2 个 agent 同时启动）

两个 agent 独立运行，互不依赖：

**Agent 1（角色）**：
- Read `references/5.1_characters.md`，提取 `### 系统提示词` 下方 ` ```text ` 块内完整规则
- 按规则分析原著，生成所有角色设定卡
- 将结果 Write 到 `draft/tmp_characters.json`，格式：`{"character_assets": [...]}`

**Agent 2（场景）**：
- Read `references/5.2_scenes.md`，提取 `### 系统提示词` 下方 ` ```text ` 块内完整规则
- 按规则分析原著，生成所有场景设定卡
- 将结果 Write 到 `draft/tmp_scenes.json`，格式：`{"scene_assets": [...]}`

两个 agent 的用户提示词均使用对应规则文件中的「用户提示词」模板，填入实际的 `style_setting` 和原著内容。

---

## 第三步 — 合并输出（主对话 Python）

```python
import json, os

project_dir = 'YOUR_PROJECT_DIR'

chars = json.load(open(f'{project_dir}/draft/tmp_characters.json', encoding='utf-8'))
scenes = json.load(open(f'{project_dir}/draft/tmp_scenes.json', encoding='utf-8'))

output = {
    'style_setting': STYLE_SETTING,
    'character_assets': chars['character_assets'],
    'scene_assets': scenes['scene_assets'],
}

out_path = f'{project_dir}/char_scene_info.json'
with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
    f.write('\n')

print(f'角色：{len(output["character_assets"])} 个')
print(f'场景：{len(output["scene_assets"])} 个')

# 编码体检
with open(out_path, 'rb') as f: raw = f.read()
fffd = b'\xef\xbf\xbd'
print('U+FFFD残留:', raw.count(fffd))
raw.decode('utf-8', errors='strict')
print('严格UTF-8：通过')
```

---

## 故障排查

| 症状 | 原因 | 解法 |
|------|------|------|
| agent stall | 原著太长，单次生成量过大 | 把原著拆成前后两半分批跑，再合并去重 |
| JSON 解析失败 | agent 输出含 Markdown 代码块 | 删除临时文件，prompt 末尾加强调"只输出 JSON，绝对不含 \`\`\`" |
| 角色/场景遗漏 | 未遵循全员盘点规则 | 对照原文人工核对，补充缺失条目后手动写入 |
