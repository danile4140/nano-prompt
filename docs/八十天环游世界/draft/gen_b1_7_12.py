import json

data = {
  "storyboard_draft": [
    {
      "id": "B1-7",
      "character_refs": ["C1"],
      "scene_refs": ["S1"],
      "covered_sentences": [
        "Phileas Fogg was sitting in his armchair waiting for his new manservant at some time between eleven and half past eleven.",
        "At exactly half past eleven Mr Fogg goes to the Reform Club.",
        "He looked up at the hands of the large clock by the wall that counted every second with a loud tick."
      ],
      "layout": (
        "①构图与镜头：主画面+画中画特写构图。"
        "主画面承载起居室全景（S1），C1坐于扶手椅；镜头位于扶手椅正面偏左约1米，斜侧30°，平视，看向C1与墙上大钟，"
        "前景为扶手椅左侧扶手局部，中景为C1坐姿，后景为左侧壁炉与墙上大钟。"
        "右上角画中画圆形特写（约占画面1/6）：壁炉上方大钟钟面特写，时针指向11:00-11:30之间。"
        "比例锚点：主画面C1坐于扶手椅，头顶约与门框把手等高（门框把手约在成人腰部高度，C1坐姿头顶需高于此）；"
        "大钟钟面在后景中直径约为C1头部宽度的两倍；圆形画中画约占画面右上角1/6。"
        "②动作与关系：C1坐于扶手椅，身体略前倾，双手放于椅扶手上，视线朝左上方看向大钟，"
        "表情专注平静，表达等待新仆从的状态；圆形画中画内钟面特写强调时间意识，"
        "钟面下方有图示气泡标注出发时间节点（11:30+小向右箭头+俱乐部轮廓图标）。"
        "③场景：萨维尔街宅邸起居室（S1），上午，自然光从窗帘隙透入。"
        "C1坐于中央扶手椅，椅背约在其背部中段高度；左侧壁炉上方可见大钟。"
        "④光影与色彩：上午柔和暖白光，室内安静，规律感强烈。"
        "⑤主体与角色：逐格角色预算：主画面可辨识1人；画中画为道具特写无角色。"
        "C1（引用C1）为唯一可辨识角色，坐姿，视线上扬看向钟，金发小胡子深色礼服。"
      )
    },
    {
      "id": "B1-8",
      "character_refs": ["C1", "C2"],
      "scene_refs": ["S1"],
      "covered_sentences": [
        "There was a knock at the door and a young man of about thirty came in."
      ],
      "layout": (
        "①构图与镜头：单格构图，中心聚焦组织。镜头位于室内左侧偏后，斜侧45°，平视，"
        "看向右侧木门——C2正推门而入，C1在远景扶手椅上侧头看向门口。"
        "前景为室内扶手椅左侧边缘，中景为敞开的木门与C2入门姿态，"
        "远景为C1坐于扶手椅（仅见侧面方向，不可完全辨识）。"
        "比例锚点：C2站立时头顶约至门框顶部下约15厘米（门框高于C2头顶）；"
        "C1在远景坐姿，头顶约与扶手椅靠背上缘平齐，尺度明显小于前景C2。"
        "②动作与关系：C2一手推开木门，一手自然垂放，略带微笑；"
        "敲门声用门板上方振动波纹图示气泡表达（波浪线图标，无英文文字）；"
        "C1在远景转头看向门口，表情平静审视，两人视线方向交汇。"
        "③场景：萨维尔街宅邸起居室（S1），上午，自然光从右侧木门透入。"
        "C2站于右侧木门入口处，C1坐于中央扶手椅，椅背约在C1背部中段。"
        "④光影与色彩：上午自然光从门口透入，C2轮廓略亮，室内暖色调。"
        "⑤主体与角色：逐格角色预算：可辨识2人（C2前景，C1远景）。"
        "C2（引用C2）为主视觉焦点，站立推门入室，棕色卷发，朴素仆从装；"
        "C1（引用C1）为远景，坐姿，仅见侧面，深色礼服。"
      )
    },
    {
      "id": "B1-9",
      "character_refs": ["C1", "C2"],
      "scene_refs": ["S1"],
      "covered_sentences": [
        "'You say that you are French, but your name is John?' asked Phileas Fogg, looking at him carefully.",
        "'Jean, sir, not John,' said the young man.",
        "'Jean Passepartout. I am an honest man, sir, and I must tell you that I haven't been a manservant all my life.",
        "I was a physical education teacher and a music teacher; then I became a singer.",
        "I once rode a horse in a circus, and for a time I worked for the fire brigade in Paris.'"
      ],
      "layout": (
        "①构图与镜头：对话双格构图，左右二分 1:2（C1质问占小格，C2主导回答��开占主格）。"
        "左格（约1/3）：C1中近景，从C2右肩后方过肩视角斜侧30°拍向C1面部，"
        "C2右肩背占左格左前景约1/5，C1正面偏右15°，背景仅见壁炉右侧边缘一角。"
        "右格（约2/3）：C2中景，正面偏左15°，手势自然说话，配云状气泡内职业序列图示；"
        "镜头位于C2正前方偏右约0.5米平视，背景仅见木门局部。"
        "比例锚点：左格C1面部占左格高度约2/3；"
        "右格C2站立，头顶约至门框顶部下约15厘米，人物占右格高度约4/5。"
        "②动作与关系：左格C1审视C2，眉头略微上扬，表情冷静带轻微质疑；"
        "对白图示气泡内为姓名疑问语义（法国国旗图标+名字问号）。"
        "右格C2自信挺胸，手势辅助说话，云状气泡承载自我介绍职业序列——"
        "气泡内为职业图标列表：体育老师+音乐老师+歌手+马术+消防员，每图标以小箭头相连，无英文文字。"
        "已扫描4对相邻句，四维度均无切换，保留5句豁免。"
        "③场景：萨维尔街宅邸起居室（S1），上午，自然光。"
        "左格C1坐于扶手椅，椅背约在其腰部；右格C2站立于门旁。"
        "④光影与色彩：上午暖白光，左格C1沉稳，右格C2活力。"
        "⑤主体与角色：逐格角色预算：左格可辨识1人（C1），右格可辨识1人（C2）。"
        "C1（引用C1）在左格，坐姿，金发小胡子；C2（引用C2）在右格，站立，棕色卷发，蓝眼睛。"
      )
    },
    {
      "id": "B1-10",
      "character_refs": ["C2"],
      "scene_refs": ["S1"],
      "covered_sentences": [
        "'I found out that a certain Mr Fogg was looking for a manservant.",
        "'He is a very clever, careful man,' they told me.",
        "'You won't find a quieter man in all of England.'",
        "'He does the same thing every day.'",
        "And so I came here to ask about the job, in the hope of finally being able to live a quiet life.'"
      ],
      "layout": (
        "①构图与镜头：主画面+云状气泡内场景构图（C2独白+回忆他人评价）。"
        "主画面（约65%）：C2近景中心聚焦，面朝C1方向（画面右侧离画），视线略偏右，认真说话。"
        "镜头位于C2正前方偏左约0.5米，平视，看向C2面部与上半身，"
        "前景无遮挡，背景仅见起居室木门左侧边缘。"
        "左上角云状气泡（约35%）：承载C2回忆他人对Fogg评价的场景——"
        "气泡内为多人议论图标（三个轮廓头像+说话符号），箭头指向Fogg图标（C1小头像），"
        "旁标聪明/安静/规律图标（齿轮+时钟+重复箭头）。"
        "比例锚点：主画面C2面部占主画面高度约3/4，左侧见肩膀局部；云气泡约占画面左上角35%。"
        "②动作与关系：C2神情认真、略带希冀，单手放胸前，向右侧解释来意；"
        "云气泡承载他人评价语义（图示方式，无英文文字）；"
        "主画面下方图示气泡表达寻求安静生活愿望（沙发+时钟+宁静符号）。"
        "已扫描4对相邻句，四维度均无切换，保留5句豁免。"
        "③场景：萨维尔街宅邸起居室（S1），上午，自然光。"
        "C2站立于门旁，C1在右侧画面外（离画存在，C2视线方向暗示）。"
        "④光影与色彩：上午暖白光，C2清晰主体，背景略柔和，云气泡内色调偏回忆性暖米色。"
        "⑤主体与角色：逐格角色预算：主画面可辨识1人（C2）；云气泡为图示无可辨识角色。"
        "C2（引用C2）为唯一可辨识角色，近景，面朝右方说话，棕色卷发，表情认真带希望感。"
        "C1离画存在，C2视线方向暗示其在场。"
      )
    },
    {
      "id": "B1-11",
      "character_refs": ["C1", "C2"],
      "scene_refs": ["S1"],
      "covered_sentences": [
        "'Yes, someone at the Reform Club told you this I believe probably the same person who told me about you.",
        "Do you understand what type of person I'm looking for?'",
        "'Yes, sir.",
        "I do, and I think I'm perfect for the job.'"
      ],
      "layout": (
        "①构图与镜头：对话双格构图，左右二分 2:1（C1主导质询，C2简短回应）。"
        "左格（约2/3）：C1中近景，反打视角，镜头从C2左肩后方斜侧30°拍向C1面部，"
        "C2左肩背作为前景左缘约占左格宽度1/5，C1正面偏右15°，背景仅见壁炉左侧片段。"
        "右格（约1/3）：C2近景，正面偏左15°，表情自信坦然，镜头位于C2正前方偏右0.5米，"
        "背景仅见木门色块片段。"
        "比例锚点：左格C1面部占左格高度约2/3；右格C2面部占右格高度约3/4。"
        "②动作与关系：左格C1坐于扶手椅，视线平视C2方向，表情平静审视；"
        "对白图示气泡承载改革俱乐部信息来源语义（俱乐部建筑轮廓+双箭头互通图标）+"
        "询问语义（问号+仆从形态图标）。"
        "右格C2挺胸，微笑点头，表情自信，回应图示气泡内含对勾+手势图标，表达胜任语义。"
        "③场景：萨维尔街宅邸起居室（S1），上午，自然光。"
        "左格C1坐于扶手椅，椅背约在其腰背部高度；右格C2站立于约1.5米处。"
        "④光影与色彩：上午暖白光，左格略暗（壁炉侧），右格略亮（门侧自然光）。"
        "⑤主体与角色：逐格角色预算：左格可辨识1人（C1），右格可辨识1人（C2）。"
        "C1（引用C1）左格坐姿，冷静；C2（引用C2）右格站立，自信微笑。"
      )
    },
    {
      "id": "B1-12",
      "character_refs": ["C1", "C2"],
      "scene_refs": ["S1"],
      "covered_sentences": [
        "'Well then, what time is it now?'",
        "'Eleven twenty-two, Mr Fogg,' Passepartout replied, taking his pocket-watch out of a small side pocket.",
        "'Exactly four minutes late,' noted Phileas Fogg, looking at his own watch.",
        "'So let's say you started working for me as from eleven twenty-six.'"
      ],
      "layout": (
        "①构图与镜头：横排三格对话节拍（问时间→报时掏表→核查裁定）。"
        "左格（约1/3）：C1中近景，正面偏右20°，略俯视C2方向，镜头位于C1右前方偏上约0.5米，"
        "看向C1面部，背景仅见壁炉上方钟面下缘；前景无遮挡。"
        "中格（约1/3）：C2中近景，正面偏左15°，手从侧口袋掏出怀表，镜头位于C2正前方偏右平视，"
        "前景为怀表特写局部，背景仅见木门片段。"
        "右格（约1/3）：C1近景，从C2右肩后方过肩视角，C1双眼看向自己手中的怀表，"
        "镜头位于C2右肩后方，看向C1面部与手中表盘，背景仅见壁炉钟面一角。"
        "比例锚点：左格C1面部占左格高度约3/4；"
        "中格C2人物占中格高度约4/5，怀表置于前景约占中格宽度1/5；"
        "右格C1面部约占右格高度2/3，C2右肩背约占右格左缘宽度1/5。"
        "②动作与关系：左格C1目光看向C2，表情平静，对白图示气泡内含时钟图标+问号（询问时间）。"
        "中格C2表情略显吃惊，手从侧袋掏出圆形怀表，怀表钟面清晰（指向11:22图示方式）；"
        "对白图示气泡内含时刻图标。"
        "右格C1手持自己的怀表，与中格时刻对比；表情平静，对白图示气泡内含两个时钟对比图标"
        "（差值4分钟符号）+合同/任用签字图标（11:26任用宣告语义）。"
        "③场景：萨维尔街宅邸起居室（S1），上午，自然光。C1坐于扶手椅，C2站立对面，两人相距约1米。"
        "④光影与色彩：上午清晨暖白光，三格色调一致，怀表在中格形成小面积金属光泽亮点。"
        "⑤主体与角色：逐格角色预算：左格可辨识1人（C1），中格可辨识1人（C2），右格可辨识1人（C1）。"
        "C1（引用C1）在左格与右格；C2（引用C2）在中格主景，右格以肩背前景出现不计可辨识人物。"
      )
    }
  ]
}

with open("E:/coze-ai-nanobanana/docs/八十天环游世界/draft/draft_B1_7_12.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

d2 = json.load(open("E:/coze-ai-nanobanana/docs/八十天环游世界/draft/draft_B1_7_12.json", encoding="utf-8"))
items = d2["storyboard_draft"]
print(f"验证通过，共{len(items)}条")
for it in items:
    print(f"  {it['id']}: {len(it['covered_sentences'])}句")
