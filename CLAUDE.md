# 规则

1. 不确定时必须停下来问，不能猜。
2. 存在多种理解时列出选项让用户选，而不是替你做决定。
3. 发现不合理的需求或者更优秀的方案时, 主动提出来, 不能盲目执行。

---

# 任意改动的修正原则(硬性)

修改 `coze_storyboard_workflow.optimized.md` 中的规则时：

1. **找充要条件，不打补丁**：规则应描述"什么情况下触发/不触发"的本质判断标准，而不是在已有规则上逐个追加"禁止 X / 禁止 Y"的例外列表——例外列表越补越长，永远堵不完。
2. **不穷举场景，给判断标准**：规则应让模型能自行推导新情况，而不是依赖已列出的案例。
3. **发现规则冲突时主动指出**：修改前先检查相关规则是否互相矛盾，若有冲突先列出让用户决策，再动文件。

---

# 文件编辑规范（硬性）

## 编码与换行符

1. **所有文本文件（`.md` / `.txt` / `.json` / `.yml`）必须使用 UTF-8 无 BOM 编码 + LF 换行符**。
   - 禁止使用 UTF-8 with BOM（开头 `EF BB BF`）。
   - 禁止使用 UTF-16 / GBK / GB18030 / Windows-1252 等其他编码保存。
   - 禁止 CRLF（`\r\n`）和 LF（`\n`）混用。
2. 项目根目录已配置 `.gitattributes`，统一强制 LF + UTF-8，编辑器请勿覆盖此设置。
3. Windows 上禁止使用旧版"记事本"编辑这些文件（旧版记事本会自动加 BOM 或转 GBK）。推荐用 VS Code / Sublime / Notepad++，并显式设置默认编码为 `UTF-8 without BOM`。

## 防"中文乱码"自检

4. **每次对 `.md` 文件做大批量 LLM 编辑后**（尤其是包含大段中文 + emoji + 引号的多次 Edit），必须立刻跑一次乱码体检：
   ```bash
   grep -n "�" <文件路径>
   ```
   如有输出，必须当场修复（结合上下文还原原字符），不得积累。
5. 体检脚本（更严格，包含 UTF-8 合法性 + 残留 U+FFFD 数量 + 换行符一致性）：
   ```bash
   python -c "
   path = '<文件路径>'
   with open(path, 'rb') as f: data = f.read()
   print('U+FFFD 残留:', data.count(b'\xef\xbf\xbd'))
   try:
       data.decode('utf-8', errors='strict')
       print('严格 UTF-8 解码: 通过')
   except UnicodeDecodeError as e:
       print('严格 UTF-8 解码: 失败 -', e)
   print('BOM 头:', '存在' if data.startswith(b'\xef\xbb\xbf') else '无')
   crlf = data.count(b'\r\n')
   lf = data.count(b'\n') - crlf
   print(f'换行符: CRLF={crlf}, LF-only={lf}')
   "
   ```
6. 修复 `�` 时，必须**结合上下文还原原意**（如 `继续��叠` → `继续叠加`、`参考图工��流` → `参考图工作流`），不得用空格、句号或随机字符替代；上下文模糊的项必须先列对照表向用户确认再改。

## 粘贴与跨平台传输

7. 从聊天界面 / 网页 / 富文本编辑器粘贴大段中文时，先用 `Ctrl+Shift+V` 粘为无格式纯文本，避免 RTF / HTML 的隐藏字符污染。
8. 跨平台（Windows ↔ Mac ↔ Linux）传输文档时，避免经过会自动转码的中转工具（如某些 IM 软件、邮件客户端预览）；推荐用 git / scp / 网盘原文件传输。
