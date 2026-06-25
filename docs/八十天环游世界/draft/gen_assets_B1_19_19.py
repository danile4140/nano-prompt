import json

proj = "E:/coze-ai-nanobanana/docs/八十天环游世界/draft"
items = json.load(open(f"{proj}/draft_B1_19_19.json", encoding="utf-8"))["storyboard_draft"]

prompt_19 = "\n".join([
    "构图与镜头：主画面+云状气泡内场景构图，主画面约60%（右侧），左上角云状气泡约40%；主画面镜头位于青年男性正前方偏右约0.5米，平视，看向其面部，正面偏左20°；前景为壁炉架上电钟纸张下缘局部，背景仅见卧室壁炉架右侧片段；云状外框气泡（白色棉絮形轮廓）置于左上角，AURA-DREAM：柔白棉絮云边缘，淡金色光斑零星点缀，画面边缘羽化柔和。",
    "",
    "动作与关系：青年男性面带满意微笑，嘴角上扬，眼眸放松，头部轻轻点头，手叉腰，表情由惊叹转为满足；心理独白气泡（椭圆形独白外框，尾巴指向青年男性）内画：绿色对勾简笔画+宁静波纹圆圈简笔画（满意确认语义）；云状大气泡承载内心满足意象：左区画时钟齿轮简笔画（规律有序）+右区画小人按时执行任务序列简笔画（clockwork规律感），两区之间为橙红色简笔右向箭头，整体传达像钟表一样规律的内心满足；无文字气泡，纯图示。",
    "",
    "场景：仆人卧室，正午前后，自然光；青年男性站于壁炉前，壁炉架约在其头部高度，电钟在其视线上方。",
    "",
    "光影与色彩：暖白光，柔和满足氛围；云气泡内色调偏淡蓝梦想感，主画面人物清晰；AURA-DREAM效果在云气泡外框区域可见。",
    "",
    "主体与角色：青年男性，约三十岁，棕色蓬松卷发，蓝色眼睛，面容亲切，满意微笑；朴素深色仆从背心，长裤；中近景，面部约占主画面高度3/4，左侧见肩膀局部；可辨识1人；云气泡内为图示，无角色。",
    "",
    "风格与媒介：STYLE_PLACEHOLDER。",
    "",
    "约束条件：角色外观、服装细节、场景家具布局严格遵循参考图；不要更换发色为黑色或金色，不要改为直发，不要改为灰色眼睛，不要更换服装主色，不要改变体型；人物外观与比例保持前后一致，画面内不得渲染中文文字，无水印，无多余人物，人物比例自然；画面内无任何浮动文字、旁白说明文字、标题文字、标签文字；比例锚点：青年男性中近景，面部约占主画面高度3/4；云气泡约占画面左上角40%。场景指纹：仆人卧室壁炉架+壁炉上方电钟+钟下纸张，位置形态不变。",
])

assets = []
for item in items:
    entry = dict(item)
    entry["prompt"] = prompt_19
    assets.append(entry)

output = {"storyboard_assets": assets}
with open(f"{proj}/assets_B1_19_19.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
    f.write("\n")

d2 = json.load(open(f"{proj}/assets_B1_19_19.json", encoding="utf-8"))
for it in d2["storyboard_assets"]:
    print(f"  {it['id']}: OK, prompt={len(it['prompt'])}字符")
