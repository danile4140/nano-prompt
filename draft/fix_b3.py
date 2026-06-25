import json, re

with open('E:/coze-ai-nanobanana/draft/assets_B3.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
assets = data['storyboard_assets']

def add_segment_tags(prompt):
    tag_map = {
        '构图与镜头': '①',
        '动作与关系': '②',
        '场景': '③',
        '光影与色彩': '④',
        '主体与角色': '⑤',
        '风格与媒介': '⑥',
        '约束条件': '⑦',
    }
    for keyword, tag in tag_map.items():
        if tag not in prompt:
            pattern = re.compile(r'(?<!\w)(' + re.escape(keyword) + r'[：:])', re.UNICODE)
            new_prompt = pattern.sub(tag + r'\1', prompt, count=1)
            prompt = new_prompt
    return prompt

def fix_s7_id(prompt):
    prompt = re.sub(r'[(（]S7\s+森林中铁皮人所在树旁空地[)）]', '（奥兹国茂密森林中铁皮人所在树旁空地）', prompt)
    prompt = re.sub(r'\bS7\b', '奥兹国茂密森林空地', prompt)
    return prompt

def add_dorothy_no_loose_hair(prompt):
    if '散发' in prompt:
        return prompt
    patterns = [
        (r'(禁止改变多萝西浅棕色辫子发色[^；。\n]*)', r'\1；禁止改为散发'),
        (r'(禁止更改Dorothy发色和双辫发型)', r'\1，禁止改为散发'),
        (r'(Dorothy发色禁止篡改[^；。\n]*)', r'\1，禁止改为散发'),
        (r'(禁止更换多萝西发色及蓝白格子裙主色)', r'\1，禁止改为散发'),
    ]
    for pat, rep in patterns:
        new_prompt = re.sub(pat, rep, prompt, count=1)
        if new_prompt != prompt:
            return new_prompt
    const_idx = prompt.rfind('约束条件')
    if const_idx > -1:
        sub = prompt[const_idx:]
        m = re.search(r'(发色[^；\n]{0,30})', sub)
        if m:
            insert_at = const_idx + m.end()
            return prompt[:insert_at] + '；禁止改为散发' + prompt[insert_at:]
    return prompt

def add_tin_man_no_beard(prompt):
    if '胡须' in prompt:
        return prompt
    patterns = [
        (r'(禁止改变铁皮人银灰色金属主色、方形铁皮盔、铆钉接缝细节[^；。\n]*)', r'\1；铁皮人无胡须无络腮胡'),
        (r'(禁止将铁皮人改为皮肤人类，禁止更换为金色或铜色金属，禁止去掉方形铁皮盔，禁止添加柔性服装，禁止改变为圆润体型[^；。\n]*)', r'\1；无胡须无络腮胡'),
        (r'(禁止去掉方形铁皮盔，禁止添加柔性服装，禁止改变为圆润体型[^；。\n]*)', r'\1；无胡须无络腮胡'),
        (r'(禁止去掉铆钉接缝，禁止给铁皮人添加柔性服装，禁止改变为圆润体型[^；。\n]*)', r'\1，无胡须无络腮胡'),
        (r'(禁止去掉方形铁皮盔，禁止去掉铆钉接缝[^；。\n]*)', r'\1，无胡须无络腮胡'),
        (r'(禁止将铁皮人改为非银灰色金属，禁止去掉方形铁皮盔[^；。\n]*)', r'\1，无胡须无络腮胡'),
    ]
    for pat, rep in patterns:
        new_prompt = re.sub(pat, rep, prompt, count=1)
        if new_prompt != prompt:
            return new_prompt
    const_idx = prompt.rfind('约束条件')
    if const_idx > -1:
        sub = prompt[const_idx:]
        m = re.search(r'(铁皮盔[^；。\n]{0,50})', sub)
        if m:
            insert_at = const_idx + m.end()
            return prompt[:insert_at] + '，无胡须无络腮胡' + prompt[insert_at:]
    return prompt

def fix_b3_6_long_bubble(prompt):
    old = '示意铁皮人发问 "Who are you and where are you going?"'
    new = '示意铁皮人发问「你们是谁/去哪里」（不使用文字气泡，仅用问号图标+双角色头像图示承载）'
    return prompt.replace(old, new)

def fix_b3_7_long_bubble(prompt):
    # 7词长句，压缩为 "I'm Dorothy!" (3词，从原文直接圈取)
    old = '"I\'m Dorothy and this is the Scarecrow."'
    new = '"I\'m Dorothy!"'
    return prompt.replace(old, new)

def add_ratio_anchors_to_constraints(item):
    prompt = item['prompt']
    bid = item['id']
    if bid == 'B3-16':
        anchor_text = '比例锚点：左格多萝西行进头顶约到稻草人腰部高度，稻草人与铁皮樵夫身高相当，狮子背部约与多萝西肩部等高；右格多萝西近景头部填满格高约2/3，河面水平线在人物头顶上方约1/4格。'
    elif bid == 'B3-17':
        anchor_text = '比例锚点：左上格多萝西头顶约至格高3/4；右上格狮子头部约占格高3/5；左下格稻草人头顶约至格高4/5；右下格狮子头部占格高约2/3。'
    elif bid == 'B3-18':
        anchor_text = '比例锚点：左上格狮子腾空河面约占格高1/4，狮子背部高于河面约格高1/3；右上格狮子背部约与稻草人坐姿腰部等高；左下格多萝西头顶约高于狮子头部1/4格；右下格铁皮樵夫铁皮盔约与狮子头顶持平。'
    else:
        return prompt
    fp_idx = prompt.rfind('场景指纹')
    if fp_idx > -1:
        return prompt[:fp_idx] + anchor_text + '\n' + prompt[fp_idx:]
    return prompt

fix_log = []

for i, item in enumerate(assets):
    bid = item['id']
    prompt = item['prompt']
    original = prompt

    if bid not in ['B3-16', 'B3-17', 'B3-18']:
        prompt = add_segment_tags(prompt)
        if prompt != original:
            fix_log.append(bid + ': L1-添加段落标签')

    if 'S7' in prompt:
        p2 = fix_s7_id(prompt)
        if p2 != prompt:
            fix_log.append(bid + ': P3-移除S7 ID')
            prompt = p2

    if 'C1' in item['character_refs'] and '散发' not in prompt:
        p2 = add_dorothy_no_loose_hair(prompt)
        if '散发' in p2:
            fix_log.append(bid + ': P4-补多萝西散发禁止项')
            prompt = p2

    if 'C9' in item['character_refs'] and '胡须' not in prompt:
        p2 = add_tin_man_no_beard(prompt)
        if '胡须' in p2:
            fix_log.append(bid + ': P4-补铁皮人无胡须禁止项')
            prompt = p2

    if bid == 'B3-6':
        p2 = fix_b3_6_long_bubble(prompt)
        if p2 != prompt:
            fix_log.append('B3-6: P5-压缩长气泡')
            prompt = p2

    if bid == 'B3-7':
        p2 = fix_b3_7_long_bubble(prompt)
        if p2 != prompt:
            fix_log.append("B3-7: P5-压缩长气泡")
            prompt = p2

    if bid in ['B3-16', 'B3-17', 'B3-18']:
        item_tmp = dict(item)
        item_tmp['prompt'] = prompt
        p2 = add_ratio_anchors_to_constraints(item_tmp)
        if p2 != prompt:
            fix_log.append(bid + ': L4-约束条件补比例锚点')
            prompt = p2

    assets[i]['prompt'] = prompt

print('修复日志:')
for log in fix_log:
    print('  ' + log)
print('共修复: ' + str(len(fix_log)) + ' 项')

with open('E:/coze-ai-nanobanana/draft/assets_B3.json', 'w', encoding='utf-8', newline='\n') as f:
    json.dump({'storyboard_assets': assets}, f, ensure_ascii=False, indent=2)
print('已保存')
