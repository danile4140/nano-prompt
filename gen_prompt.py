import json, os, re

project_dir = 'E:/coze-ai-nanobanana/docs/南海奇幻故事'

char_desc = {
    'C1': {
        'full': '年迈男性老人，皮肤异常苍白近乎白色，头发枯草黄色稀疏蓬乱，双目浑浊泛白失明无神，身着深色宽松长袍，脖颈挂多串叶片编成的项链，赤脚',
        'ban': '不要更换发色为深色或黑色，不要改为健康有神的眼睛，不要更换服装主色为浅色，不要去掉项链，不要添加鞋子，不要改变苍白肤色，不要改变体型为壮实，无胡须，无络腮胡'
    },
    'C1b': {
        'full': '年迈男性老人，皮肤异常苍白近乎白色，枯草黄发，失明白眼，深色宽松长袍（等比例放大），叶片项链，赤脚；体型急剧放大至巨人尺度，头肩宽如小岛；左手托举铁皮提灯',
        'ban': '不要更换发色为深色或黑色，不要改为健康有神的眼睛，不要更换服装主色为浅色，不要去掉项链，不要添加鞋子，不要改变苍白肤色，不要缩小至正常人体型，不要去掉提灯，无胡须，无络腮胡'
    },
    'C2': {
        'full': '成年夏威夷男性，约二十多岁，深棕色皮肤，黑色直发中等长度略蓬松，五官端正，眼睛深棕色，体型匀称偏瘦，身着宽松白色短袖衬衫，深色宽松长裤，腰间系布带，赤脚',
        'ban': '不要更换发色为浅色，不要改为卷发，不要更换服装主色，不要改为长袖，不要添加鞋子，不要改变体型为肥胖或魁梧，无胡须，无络腮胡'
    },
    'C3': {
        'full': '成年夏威夷女性，约二十岁出头，深棕色皮肤，黑色直发长至肩膀，发丝顺直，五官柔和，眼睛深棕色，体型纤细匀称，身着浅黄色宽松长裙，无袖，裙摆及踝',
        'ban': '不要更换发色为浅色或棕红色，不要改为卷发，不要更换服装主色为深色，不要改为有袖款式，不要改变体型'
    },
    'C4': {
        'full': '成年波利尼西亚女性，约十八至二十岁，深棕色皮肤，黑色卷发蓬松至肩，眼睛深色，表情略显警觉，体型纤细，身着宽大植物叶片裙，叶片绿色，叶裙覆盖腰部至膝盖，上身无遮蔽，赤脚',
        'ban': '不要更换发色为直发或浅色，不要更换裙子为布料款式，不要去掉植物叶裙，不要添加上衣遮蔽，不要添加鞋子'
    },
    'C5': {
        'full': '中年白人男性，约四五十岁，浅肤色，浅棕色短发略带灰白，留有整齐的短胡须，体型中等略显魁梧，身着深蓝色船长制服外套，双排铜扣，深色长裤，黑色皮靴至小腿，头戴深蓝色船长圆顶帽',
        'ban': '不要更换服装主色为浅色，不要改为无扣单排扣，不要更换帽子，不要去掉短胡须，不要更换发色为深黑色，不要改变体型为消瘦'
    },
    'C6': {
        'full': '成年白人男性，约三十多岁，浅肤色，深棕色短发，面部无胡须，表情严厉，体型高大魁梧，肌肉明显，身着深灰色粗布工作上衣，短袖，前胸无扣，深色粗布长裤，黑色厚底靴，无帽',
        'ban': '不要更换服装主色为浅色，不要改为长袖，不要改变体型为瘦小，不要添加胡须，不要添加帽子，不要更换发色为浅色，无胡须，无络腮胡'
    },
    'C7': {
        'full': '成年夏威夷男性，约三十岁，深棕色皮肤，黑色短直发，五官普通，体型中等健壮，身着棕色宽松短袖衬衫，深色短裤，赤脚',
        'ban': '不要更换发色为浅色，不要改为卷发，不要更换服装主色，不要改为长袖，不要添加鞋子，无胡须，无络腮胡'
    },
    'C8': {
        'full': '中年波利尼西亚男性，约四五十岁，深棕色皮肤，黑色短发略带鬈曲，面部有传统纹身图案，深蓝色几何线条覆盖面颊和下颌，体型高大健壮，身着传统棕黄色草裙，及膝，颈部挂有鲨鱼牙齿串成的项链，赤脚，无上衣',
        'ban': '不要去掉面部纹身，不要更换纹身颜色，不要更换草裙主色，不要去掉鲨鱼牙齿项链，不要添加上衣，不要改变体型为消瘦，无胡须，无络腮胡'
    },
    'C9': {
        'full': '中年白人男性，约四五十岁，浅肤色，灰白色短发梳理整齐，面部留有整洁的浅色短络腮胡，体型中等略显清瘦，身着黑色立领长袍，袖子长至手腕，白色内衬领口微露，黑色皮鞋',
        'ban': '不要更换服装主色为非黑色，不要去掉白色内衬领口，不要去掉络腮胡，不要更换发色为深黑色，不要改变体型为肥胖'
    },
}

scene_fingerprint = {
    'S1': '满排木制书架+皮面圣经桌面+砖砌壁炉，位置形态不变',
    'S2': '低矮木质房屋正门+碎石泥土小路+远处海湾，位置形态不变',
    'S3': '细白沙滩+五彩贝壳+茂密低矮热带树林边缘，位置形态不变',
    'S3b': '细白沙滩+树林边缘被砍倒树干横陈+翻动踩踏沙地，位置形态不变',
    'S4': '传统夏威夷双体独木舟+前桅悬挂铁皮提灯+船尾舵把，位置形态不变',
    'S5': '宽阔木质甲板+大型多辐圆形木制舵轮+主桅及索具，位置形态不变',
    'S6': '低矮草顶木框旧茅屋+正门朝向礁湖侧开放+清澈蓝绿色礁湖水面，位置形态不变',
    'S7': '结构完整新鲜棕榈叶屋顶茅屋+竹木编织整齐墙面+礁湖水面，位置形态不变',
    'S8': '排列有序草顶茅屋群+石板泥土小路+中央开阔空地，位置形态不变',
    'S9': '高大宽叶乔木群+树干与根茎交错地面+树林边缘兽径，位置形态不变',
    'S10': '满排木制书架+桌面摊开旧地图+砖砌壁炉，位置形态不变',
}

def get_fp(scene_refs):
    fps = [scene_fingerprint.get(s, '') for s in scene_refs if s in scene_fingerprint]
    if not fps:
        return '场景固定元素位置形态不变'
    return '；'.join(fps)

def get_ban(char_refs):
    parts = []
    for c in char_refs:
        if c in char_desc:
            parts.append(char_desc[c]['ban'])
    return '；'.join(parts)

def make_constraint(char_refs, scene_refs, layout_text):
    has_quotes = bool(re.search(r'"[A-Za-z]', layout_text))
    ban = get_ban(char_refs)
    fp = get_fp(scene_refs)
    parts = ['角色外观、服装细节、场景家具布局严格遵循参考图，不自行添加或修改任何细节，人物外观与比例保持前后一致，画面内不得渲染中文文字，无水印，无多余人物，人物比例自然，道具大小合理，空间关系清楚']
    if ban:
        parts.append(ban)
    if has_quotes:
        parts.append('英文拼写正确，无任何气泡外浮动文字、旁白说明文字、标题文字，气泡不遮主体，画面内所有英文字母统一使用手写体风格：随性手写字母，笔画粗犷有力，基线轻微起伏，字母间距自然')
    else:
        parts.append('画面内无任何浮动文字、旁白说明文字、标题文字、标签文字')
    parts.append('场景指纹：' + fp)
    return '；'.join(parts)


def extract_section(layout, label, next_label):
    start = layout.find(label)
    if start < 0:
        return ''
    start_content = start + len(label)
    if start_content < len(layout) and layout[start_content] == '：':
        start_content += 1
    if next_label:
        end = layout.find(next_label, start_content)
        if end < 0:
            end = len(layout)
    else:
        end = len(layout)
    return layout[start_content:end].strip()


def expand_char(text, char_refs):
    for c_id in char_refs:
        if c_id in char_desc:
            text = text.replace('（引用' + c_id + '）', '（' + char_desc[c_id]['full'] + '）')
    text = re.sub(r'（引用C\w+b?）', '', text)
    return text


def generate_prompt(item):
    layout = item['layout']
    char_refs = item['character_refs']
    scene_refs = item['scene_refs']

    section_labels = ['①构图与镜头', '②动作与关系', '③场景', '④光影与色彩', '⑤主体与角色']

    sections = {}
    for i, label in enumerate(section_labels):
        next_label = section_labels[i+1] if i+1 < len(section_labels) else None
        sections[label] = extract_section(layout, label, next_label)

    parts = []

    s1 = re.sub(r'（引用C\w+b?）', '', sections['①构图与镜头'])
    parts.append('①构图与镜头：' + s1)
    parts.append('')

    s2 = expand_char(sections['②动作与关系'], char_refs)
    parts.append('②动作与关系：' + s2)
    parts.append('')

    s3 = re.sub(r'（引用C\w+b?）', '', sections['③场景'])
    parts.append('③场景：' + s3)
    parts.append('')

    s4 = re.sub(r'（引用C\w+b?）', '', sections['④光影与色彩'])
    parts.append('④光影与色彩：' + s4)
    parts.append('')

    s5 = expand_char(sections['⑤主体与角色'], char_refs)
    parts.append('⑤主体与角色：' + s5)
    parts.append('')

    parts.append('⑥风格与媒介：STYLE_PLACEHOLDER')
    parts.append('')

    constraint = make_constraint(char_refs, scene_refs, layout)
    parts.append('⑦约束条件：' + constraint)

    return '\n'.join(parts)


def process_batch(draft_file, assets_file):
    if not os.path.exists(draft_file):
        print('SKIP missing: ' + draft_file)
        return False

    if os.path.exists(assets_file) and os.path.getsize(assets_file) > 10:
        try:
            json.load(open(assets_file, encoding='utf-8'))
            print('SKIP exists: ' + assets_file)
            return True
        except Exception:
            pass

    draft = json.load(open(draft_file, encoding='utf-8'))
    items = draft['storyboard_draft']

    output = {'storyboard_assets': []}
    for item in items:
        entry = dict(item)
        entry['prompt'] = generate_prompt(item)
        output['storyboard_assets'].append(entry)

    with open(assets_file, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        f.write('\n')

    try:
        json.load(open(assets_file, encoding='utf-8'))
        print('OK: ' + assets_file + ' (' + str(len(items)) + ' 条)')
        return True
    except Exception as e:
        print('ERROR: ' + assets_file + ': ' + str(e))
        return False


chapters = {
    1: ['1_3','4_6','7_9','10_12','13_15','16_18','19_21'],
    2: ['1_3','4_6','7_9','10_12','13_15','16_17'],
    3: ['1_3','4_6','7_9','10_12','13_15','16_17'],
    4: ['1_3','4_6','7_9','10_12','13_15','16_16'],
    5: ['1_3','4_6','7_9','10_12','13_15'],
    6: ['1_3','4_6','7_9','10_12','13_13'],
}

success = 0
fail = 0
for n, tags in chapters.items():
    for tag in tags:
        draft_file = project_dir + '/draft/draft_B' + str(n) + '_' + tag + '.json'
        assets_file = project_dir + '/draft/assets_B' + str(n) + '_' + tag + '.json'
        if process_batch(draft_file, assets_file):
            success += 1
        else:
            fail += 1

print('\n完成：成功' + str(success) + '，失败' + str(fail))
