#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# ── constants ──────────────────────────────────────────────────────────────────

style_setting = (
    "经典欧式古典儿童插画风格，轻复古英伦乡村质感，暖调柔和配色，细腻淡彩手绘笔触，"
    "房屋建筑简约欧式造型，人物神态细腻自然，神态贴合故事委屈压抑情绪，场景写实简约不复杂，"
    "层次清淡素雅，氛围感怀旧静谧，画面柔和温润，整体色调偏暖杏色，线条流畅舒缓，纯绘本插画质感"
)

standard_17_5 = (
    "角色外观、服装细节、场景家具布局严格遵循参考图，不自行添加或修改任何细节，"
    "人物外观与比例保持前后一致。画面内不得渲染中文文字，无水印，无多余人物，"
    "人物比例自然，道具大小合理，空间关系清楚。"
)

no_text_declaration = "画面内无任何浮动文字、旁白说明文字、标题文字、标签文字。"

# ── character appearance descriptions (no IDs) ────────────────────────────────

jane_desc = (
    "18岁年轻女性，浅棕中长发盘在脑后，灰蓝色杏仁眼，"
    "藏青色粗布连衣裙，领口配白色棉质翻领，黑色粗跟皮鞋"
)
jane_neg = "禁止夸张妆容，禁止华丽服饰"

rochester_desc = (
    "38岁中年男性，深黑色卷发夹杂白发，双眼失明无神，左手手臂残缺，"
    "深黑色宽松家居服，深色软底鞋"
)
rochester_neg = "禁止明亮眼神，禁止完整左手，禁止正式服饰"

rochester_b929_desc = (
    "38岁中年男性，深黑色卷发夹杂白发，单眼部分恢复视力、目光有所聚焦（非完全空洞），"
    "左手手臂残缺，深黑色宽松家居服，深色软底鞋"
)
rochester_b929_neg = "禁止双眼完全明亮，禁止完整左手，禁止正式服饰，禁止夸张聚焦眼神"

adele_desc = (
    "成长后的法国少女，浅金色卷发，深蓝色眼睛，气质较幼年时更成熟稳重，"
    "保留少女灵动感，服饰整洁"
)
adele_neg = "禁止幼童体型，禁止沉闷表情"

# ── scene fingerprint for S22 ─────────────────────────────────────────────────

s22_fp_night = "石砌壁炉+布艺沙发+棉布窗帘小窗"
s22_fp_day   = "起居室窗边日光+布艺沙发+石砌壁炉"

# ── helper ────────────────────────────────────────────────────────────────────

def build_prompt(
    composition,        # ① 构图与镜头
    action_relation,    # ② 动作与关系
    scene,              # ③ 场景
    light_color,        # ④ 光影与色彩
    subject_char,       # ⑤ 主体与角色
    constraint,         # ⑦ 约束条件 (ratio + fingerprint + 17.5 + no-text appended inside)
):
    sections = [
        f"①构图与镜头：{composition}",
        f"②动作与关系：{action_relation}",
        f"③场景：{scene}",
        f"④光影与色彩：{light_color}",
        f"⑤主体与角色：{subject_char}",
        f"⑥风格与媒介：{style_setting}",
        f"⑦约束条件：{constraint}",
    ]
    return "\n\n".join(sections)


# ── prompt definitions ────────────────────────────────────────────────────────

def prompt_B9_21():
    constraint = (
        f"画面比例锚点：两人各约占画幅1/2。"
        f"场景指纹：{s22_fp_night}。"
        f"{standard_17_5}"
        f"角色外观约束——{jane_desc.split('，')[0]}女性：{jane_neg}；"
        f"中年男性角色：{rochester_neg}。"
        f"{no_text_declaration}"
    )
    return build_prompt(
        composition=(
            "中近景双人同框，年轻女性居左身体微前倾表达坚定，中年男性居右身体略内收，"
            "两人情绪对比鲜明，镜头平视"
        ),
        action_relation=(
            "年轻女性语气坚定，身体微前倾强调确定感；中年男性摆手或低头，"
            "肢体语言传达自我否定与退缩；摆手动作须带手绘线条图示质感，"
            "起居室壁炉火光在背景中轻微跳动作为环境效果；"
            "动作对比呈现她的坚定对抗他的自我贬低"
        ),
        scene=(
            "偏远林地小农庄起居室，夜晚，石砌壁炉、布艺沙发、棉布窗帘小窗，"
            "烛台是主要光源，氛围由温暖转向男性角色的自我质疑"
        ),
        light_color=(
            "暖烛光为主，男性角色一侧阴影加深强调内敛自我遮蔽感，"
            "女性角色一侧较亮传达情感主动性，冷暖对比烘托两人情绪差异"
        ),
        subject_char=(
            f"左侧较亮：{jane_desc}；"
            f"右侧较暗：{rochester_desc}；"
            "两人各占画幅约1/2"
        ),
        constraint=constraint,
    )


def prompt_B9_22():
    constraint = (
        f"画面比例锚点：两人各约占画幅1/2。"
        f"场景指纹：{s22_fp_night}。"
        f"{standard_17_5}"
        f"角色外观约束——{jane_desc.split('，')[0]}女性：{jane_neg}；"
        f"中年男性角色：{rochester_neg}。"
        "禁止出现任何第三人物形象。"
        f"{no_text_declaration}"
    )
    return build_prompt(
        composition=(
            "中景双人，中年男性居左头微侧向女性方向询问，"
            "年轻女性居右面朝男性坦然回答，镜头平视，两人之间对话轴清晰"
        ),
        action_relation=(
            "中年男性问话时手指轻轻叩击椅把扶手，传达极度克制的微妙嫉妒情绪，"
            "叩击动作以手绘细节方式表现；"
            "年轻女性回答时表情平静自然，无刻意修饰；"
            "壁炉烛光在男性背后轻微跳动作为环境效果；"
            "两人情绪温差通过细微肢体语言传达，非面部夸张表情"
        ),
        scene=(
            "偏远林地小农庄起居室，夜晚，石砌壁炉、布艺沙发、棉布窗帘小窗，"
            "暖烛光氛围，与前序连贯"
        ),
        light_color=(
            "暖烛光均匀稳定，画面平和，无高对比度阴影，"
            "情绪微妙而非激烈，色调温和"
        ),
        subject_char=(
            f"左侧（发问者）：{rochester_desc}；"
            f"右侧（回答者）：{jane_desc}；"
            "两人面部均清晰可见，各占画幅约1/2"
        ),
        constraint=constraint,
    )


def prompt_B9_23():
    constraint = (
        f"画面比例锚点：两格各占画幅约1/2，人物面部约占各格画高2/3。"
        f"场景指纹：{s22_fp_night}。"
        f"{standard_17_5}"
        f"角色外观约束——{jane_desc.split('，')[0]}女性：{jane_neg}；"
        f"中年男性角色：{rochester_neg}。"
        "禁止标注对话人名。"
        f"{no_text_declaration}"
    )
    return build_prompt(
        composition=(
            "双格对切近景：第一格为中年男性面部特写（头微微前倾，眉间轻微紧张）；"
            "第二格为年轻女性面部特写（表情平静直接，眼神朝向男性方向）；"
            "两格并排，切换节奏加快暗示对话临近关键转折"
        ),
        action_relation=(
            "中年男性头部轻微前倾传达追问情绪强度，前倾角度须微小不夸张；"
            "年轻女性面部平静如水，眼神不回避，回答直接干脆；"
            "两格对切加速感以构图静止+视线张力传达，无夸张肢体动作；"
            "背景烛光虚化光晕作为环境效果"
        ),
        scene=(
            "偏远林地小农庄起居室，夜晚，烛光近景，背景极度虚化为暖橙光晕，"
            "与前序连贯"
        ),
        light_color=(
            "暖烛光近景，两人面部细节清晰，光影稳定沉着，"
            "无强烈色温变化，烘托压抑嫉妒情绪的积累"
        ),
        subject_char=(
            f"第一格：{rochester_desc}，面部特写；"
            f"第二格：{jane_desc}，面部特写"
        ),
        constraint=constraint,
    )


def prompt_B9_24():
    constraint = (
        f"画面比例锚点：双人格两人各约1/2；单人格男性面部约占画高2/3。"
        f"场景指纹：{s22_fp_night}。"
        f"{standard_17_5}"
        f"角色外观约束——{jane_desc.split('，')[0]}女性：{jane_neg}；"
        f"中年男性角色：{rochester_neg}。"
        "男性微笑须克制，久违感而非大喜，嘴角轻扬即可。"
        f"{no_text_declaration}"
    )
    return build_prompt(
        composition=(
            "先为中近景双人同框（男性居左问话，女性居右轻摇头回答），"
            "随即切至男性面部单格特写（嘴角浮现久违的微笑，眼眶处有情绪波动）；"
            "双格+单格组合，镜头平视"
        ),
        action_relation=(
            "年轻女性轻摇头+平静表情作为斩钉截铁回答，头部摇动须以手绘图示质感表现；"
            "男性微笑格：嘴角轻扬，久违的微小表情变化是叙事高点；"
            "背景壁炉暖光在微笑格中明显增强，象征情绪破冰；"
            "环境效果：烛光光晕在情绪转折处柔和扩散"
        ),
        scene=(
            "偏远林地小农庄起居室，夜晚，石砌壁炉、布艺沙发、棉布窗帘小窗，"
            "烛光，微笑格背景虚化为纯暖色光晕"
        ),
        light_color=(
            "男性微笑格暖光明显增强，面部阴影减少，象征情绪破冰；"
            "双人格暖烛光平稳；整体色温在微笑格达到该序列局部高点"
        ),
        subject_char=(
            f"双人格左侧：{rochester_desc}；右侧：{jane_desc}；"
            f"单人格：{rochester_desc}，面部特写"
        ),
        constraint=constraint,
    )


def prompt_B9_25():
    constraint = (
        "画面比例锚点：手部特写居画面中心，两人面部在画面上方模糊可见。"
        "场景指纹：暖烛光下的手握特写+布艺沙发扶手+石砌壁炉背景光晕。"
        f"{standard_17_5}"
        f"角色外观约束——{jane_desc.split('，')[0]}女性：{jane_neg}；"
        f"中年男性角色：{rochester_neg}。"
        "男性握手动作须有摸索感，非精准方向。"
        f"{no_text_declaration}"
    )
    return build_prompt(
        composition=(
            "近景俯视略偏，镜头聚焦两人相握的手部细节居画面中心，"
            "两人面部在上方模糊可见；手握手是画面唯一核心主体，"
            "构图静止传达深沉沉默感"
        ),
        action_relation=(
            "中年男性一手摸索伸向女性之手，握住时带有寻觅感，非精准动作；"
            "手部握合动作以手绘细腻线条质感呈现，象征重建连结；"
            "男性低头，嘴唇微动传达轻声询问；"
            "壁炉暖光在手部周围形成柔和光晕作为环境效果；"
            "构图整体静止，沉默感由静止传达"
        ),
        scene=(
            "偏远林地小农庄起居室，夜晚，烛台光源，背景极度虚化为暖橙光晕，"
            "布艺沙发扶手在手部旁侧隐约可见，石砌壁炉背景光晕"
        ),
        light_color=(
            "暖烛光集中照亮手部区域，两人肤色在光晕中柔和融合，"
            "传达亲密深情氛围；面部区域光线柔和模糊"
        ),
        subject_char=(
            f"主体：两人相握手部特写；"
            f"次要辅助（模糊）：{rochester_desc}面部上方；{jane_desc}面部上方"
        ),
        constraint=constraint,
    )


def prompt_B9_26():
    constraint = (
        "画面比例锚点：两人同框近景，各约占画幅1/2，双手相握仍可见。"
        "场景指纹：暖烛光全幅笼罩+布艺沙发+石砌壁炉（本格为全章烛光最亮格）。"
        f"{standard_17_5}"
        f"角色外观约束——{jane_desc.split('，')[0]}女性：{jane_neg}；"
        f"中年男性角色：{rochester_neg}。"
        "本格为全章情感顶点，暖光须明显强于前序所有格；男性喜悦通过面部表情传达，不用夸张动作。"
        f"{no_text_declaration}"
    )
    return build_prompt(
        composition=(
            "中近景双人同框，年轻女性居左，中年男性居右，"
            "镜头平视，画面构图趋于对称，强调两人在同一空间终于和解的庄重感"
        ),
        action_relation=(
            "年轻女性眼含泪光但嘴角微笑，泪光以手绘细腻水光质感表现；"
            "中年男性面部绽放深沉喜悦（比前一微笑格更深层），头微微低下像放下重担；"
            "两人双手仍相握可见；"
            "壁炉暖光此格全幅扩散作为环境效果，暗示情感全面升温；"
            "身体自然靠近但动作克制不夸张"
        ),
        scene=(
            "偏远林地小农庄起居室，夜晚，烛台此格为全章最亮光源，"
            "暖光将整个画面笼罩，石砌壁炉、布艺沙发背景可见"
        ),
        light_color=(
            "暖黄烛光全幅照亮，阴影最少，画面最亮最暖，"
            "与前序所有压抑格形成全章最大色温转折，象征情感高潮"
        ),
        subject_char=(
            f"左侧：{jane_desc}，眼含泪光微笑；"
            f"右侧：{rochester_desc}，面露深沉喜悦；"
            "双手相握仍可见，两人面部均清晰"
        ),
        constraint=constraint,
    )


def prompt_B9_27():
    constraint = (
        "画面比例锚点：三格横向并排，细分隔线区分，各格等宽。"
        "场景指纹：羽毛笔+信纸桌面+石砌壁炉背景（中格和右格）。"
        f"{standard_17_5}"
        f"角色外观约束——婚礼格剪影仅轮廓，无细节；写信格{jane_desc.split('，')[0]}女性侧影：{jane_neg}。"
        "禁止在任何格中出现第三具名人物形象；婚礼格禁止清晰描绘仪式细节，仅剪影处理。"
        f"{no_text_declaration}"
    )
    return build_prompt(
        composition=(
            "横向叙事序列条，三格并排以细线分隔：\n"
            "左格（婚礼仪式）：祭坛前两个人物轮廓剪影，无细节，仅轮廓；\n"
            "中格（写信）：年轻女性侧影低头伏案，羽毛笔在信纸上书写；\n"
            "右格（未回复）：桌面单封信纸特写，背景空旷，暗示沉默无回音；\n"
            "三格构成时间跨越叙事"
        ),
        action_relation=(
            "左格：两人剪影轮廓静止于祭坛前，动作极简，无面部细节；"
            "中格：女性侧影书写动作，羽毛笔笔尖在纸面上的手绘线条图示表现书写感；"
            "右格：信纸静置桌上，无人物，背景空旷暗示无回应；"
            "三格共同以动作逐渐消失传达时间流逝"
        ),
        scene=(
            "左格：模糊小教堂或起居室内祭坛轮廓；"
            "中格：偏远林地小农庄起居室，暖烛光，桌面书写场景；"
            "右格：同一起居室桌面局部，石砌壁炉背景隐约可见"
        ),
        light_color=(
            "三格色调：左格+中格为暖黄调，右格略降温至稍冷调，"
            "轻微色温变化传达时间推移和情绪落差"
        ),
        subject_char=(
            f"左格：两个人物剪影（一高一矮，无具名特征）；"
            f"中格：{jane_desc}侧影（书写姿态）；"
            "右格：无人物，仅信纸道具"
        ),
        constraint=constraint,
    )


def prompt_B9_28():
    constraint = (
        "画面比例锚点：左格约1/3画幅（无具名人物），右格约2/3画幅，"
        "右格中两人各约占1/3，窗框作为场景锚点。"
        f"场景指纹：{s22_fp_day}。"
        f"{standard_17_5}"
        f"角色外观约束——{jane_desc.split('，')[0]}女性：{jane_neg}；"
        f"成长后少女：{adele_neg}。"
        "左格禁止出现任何具名人物；右格少女须呈现较幼年更成熟的年龄感。"
        f"{no_text_declaration}"
    )
    return build_prompt(
        composition=(
            "双格构图：\n"
            "左格（象征性地图/地球仪）：远景地球仪或地图轮廓线条图，暗示遥远旅程，无具名人物；\n"
            "右格（窗边日常）：年轻女性与成长后少女并肩坐于起居室窗边，"
            "镜头平视略温柔，窗框作为场景锚点，日间自然光从窗口射入"
        ),
        action_relation=(
            "左格：地球仪/地图轮廓以手绘线条图示质感呈现远方感，纯环境叙事；"
            "右格：年轻女性侧脸微笑看着身旁少女；"
            "少女举手比划说话，手部姿态生动以手绘细节表现；"
            "两人肢体语言传达亲密友谊，窗外阳光在室内地板上形成暖光效果"
        ),
        scene=(
            "左格：象征性地图视觉（无室内背景）；"
            "右格：偏远林地小农庄起居室，日间，柔和自然光从窗口射入，"
            "室内温暖整洁，石砌壁炉、布艺沙发背景可见"
        ),
        light_color=(
            "右格日光暖调，明亮舒展，与前序夜间烛光格形成鲜明时间感对比，"
            "传达平静日常生活的温馨；左格色调相对中性"
        ),
        subject_char=(
            f"左格：无具名人物，地球仪/地图轮廓图示；"
            f"右格左侧：{jane_desc}；"
            f"右格右侧：{adele_desc}；两人并肩，窗框在背景"
        ),
        constraint=constraint,
    )


def prompt_B9_29():
    constraint = (
        "画面比例锚点：两位主角并肩居画面中心，两名孩童剪影居前景（体型极小），"
        "整体宽幅全景构图。"
        f"场景指纹：日光窗口+温暖起居室布艺沙发+窗外绿色植被。"
        f"{standard_17_5}"
        f"角色外观约束——{jane_desc.split('，')[0]}女性：{jane_neg}；"
        f"中年男性角色（部分复明）：{rochester_b929_neg}。"
        "孩童形象仅小剪影轮廓，禁止具名；男性目光聚焦须微妙，不过分夸张。"
        "本格为全章最明亮最暖格，日光须大面积铺陈。"
        f"{no_text_declaration}"
    )
    return build_prompt(
        composition=(
            "全章终格，宽幅全景家庭构图：主角二人并肩坐于起居室中心，"
            "中年男性侧头望向年轻女性，女性回望；"
            "两名孩童剪影在画面前景玩耍（体型极小，仅轮廓）；"
            "镜头平视略退，构图温馨宽阔，窗外绿色植被可见"
        ),
        action_relation=(
            "中年男性侧头凝视女性，目光比前序格有明显聚焦感（部分视力恢复），"
            "凝视动作以手绘细腻线条传达专注感；"
            "年轻女性温柔回望；"
            "两名孩童前景小剪影玩耍动态以简约线条轮廓表现；"
            "窗外阳光和室内绿植倒影作为环境效果，传达生机与平静"
        ),
        scene=(
            "偏远林地小农庄起居室，日间，明亮暖和，"
            "大面积日光从窗口射入，窗外隐约可见绿色植被（与前序章节荒凉形成对比），"
            "室内石砌壁炉、布艺沙发、棉布窗帘陈设温馨整洁"
        ),
        light_color=(
            "全章最明亮最暖格，日光从窗口大面积射入，暖黄米白色调，"
            "无阴影压制，象征苦难结束后的彻底光明；"
            "与章节首格的冷灰调形成完整情绪弧度对比"
        ),
        subject_char=(
            f"中心左侧：{jane_desc}，温柔回望；"
            f"中心右侧：{rochester_b929_desc}，侧头凝视；"
            "前景：两名孩童极小剪影，仅轮廓，无具名特征"
        ),
        constraint=constraint,
    )


# ── load draft and filter B9-21 to B9-29 ─────────────────────────────────────

with open("E:/coze-ai-nanobanana/draft_B9.json", "r", encoding="utf-8") as f:
    draft = json.load(f)

target_ids = {f"B9-{i}" for i in range(21, 30)}
prompt_funcs = {
    "B9-21": prompt_B9_21,
    "B9-22": prompt_B9_22,
    "B9-23": prompt_B9_23,
    "B9-24": prompt_B9_24,
    "B9-25": prompt_B9_25,
    "B9-26": prompt_B9_26,
    "B9-27": prompt_B9_27,
    "B9-28": prompt_B9_28,
    "B9-29": prompt_B9_29,
}

assets = []
for item in draft["storyboard_draft"]:
    if item["id"] not in target_ids:
        continue
    panel = {
        "id": item["id"],
        "character_refs": item["character_refs"],
        "scene_refs": item["scene_refs"],
        "covered_sentences": item["covered_sentences"],
        "layout": item["layout"],
        "prompt": prompt_funcs[item["id"]](),
    }
    assets.append(panel)

output = {"storyboard_assets": assets}
out_path = "E:/coze-ai-nanobanana/assets_B9_part3.json"
with open(out_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(output, ensure_ascii=False, indent=2))

print(f"Written {len(assets)} panels to {out_path}")
for p in assets:
    print(f"  {p['id']}: {len(p['prompt'])} chars")
