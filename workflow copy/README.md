# Coze AI Nano Banana 工作流

## 节点运行顺序

5.1 + 5.2（并行）→ 5.3a → 5.3b

## 文件索引

| 文件 | 节点 | 用途 | 备注 |
|------|------|------|------|
| [principles.md](principles.md) | — | 设计原则、构图配方表 | 理解背景时阅读 |
| [5.1_characters.md](5.1_characters.md) | 5.1 | 从原著提取角色，输出 character_assets | 与 5.2 并行 |
| [5.2_scenes.md](5.2_scenes.md) | 5.2 | 从原著提取场景，输出 scene_assets | 与 5.1 并行 |
| [5.3a_storyboard_planning.md](5.3a_storyboard_planning.md) | **5.3a** | **按章节规划分镜结构，输出 storyboard_draft** | **核心文件** |
| [5.3b_prompt_generation.md](5.3b_prompt_generation.md) | **5.3b** | **将分镜规划扩写为最终 prompt，输出 storyboard_assets** | **核心文件** |

## 输入输出关系

```
原著全文 ──→ 5.1 ──→ character_assets ─┐
         └──→ 5.2 ──→ scene_assets ────┤
                                        ├──→ 5.3a (按章节循环) ──→ storyboard_draft
                                        |                              │
                                        └──────────────────────────── ↓
                                                                  5.3b (按章节循环)
                                                                       │
                                                                       ↓
                                                              storyboard_assets
```
