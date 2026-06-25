# 第 8 章分镜计划（分镜 id 格式 B8-{seq}）

总分镜数：33

句子总数自检：115 句，已覆盖 115 句，未覆盖 0 句，自检等式成立。

---

## 句子分配表（阶段一）

B8-1 | character_refs: ["C1", "C38"] | scene_refs: [] | 预估格数: 2
- I was at home for about ten days when a friend of mine came to see me.
- Captain Robinson owned a ship called the Hope-well, and he wanted me to sail with him.
- At first I did not want to go, but he offered me a lot of money, and in the end I agreed.

B8-2 | character_refs: ["C1", "C38"] | scene_refs: ["S27"] | 预估格数: 2
- We sailed in the Hope-well to the East Indies.
- There was bad news when we arrived there.
- The goods which Captain Robinson wanted to buy were not ready.

B8-3 | character_refs: ["C1", "C38"] | scene_refs: ["S27"] | 预估格数: 2
- 'I'll have to stay here and wait,' Captain Robinson told me.
- 'But you don't have to stay here with me, Gulliver.
- Let's buy a smaller ship, and you can go to the islands near here and buy and sell goods.'

B8-4 | character_refs: ["C1"] | scene_refs: [] | 预估格数: 1
- I agreed, and soon I was in command of a little ship of my own.
- （注：接受请求结果已与B8-3中的提议拆分；此句为新叙事阶段开端（格列佛独自出发），单独成镜，触发条件B——B8-3为提出建议，B8-4为被接受结果，情绪方向相反不同时刻）

B8-5 | character_refs: ["C1", "C40"] | scene_refs: [] | 预估格数: 4
- Unfortunately this little ship was attacked by pirates.
- They came on board, and they stole everything, including the ship itself.
- They were very fierce, and I thought they were going to kill me.
- They changed their minds, though, and decided to put me into a canoe with enough food and water for four days.
- （注：4步执行链——来袭→抢劫→威胁→放入独木舟，触发§4条件C（计划执行链≥3步），需4格；此处"they were going to kill me"含强烈恐惧，需情绪标记）

B8-6 | character_refs: ["C1"] | scene_refs: [] | 预估格数: 2
- I knew there were some islands in this part of the sea.
- I spent a few days going from one island to another.
- The islands were all small ones, and there were no people on them.
- There was also very little food.
- I began to think that I would die on one of these islands, and I was very unhappy.
- （注：已扫描4对相邻句，场景为同一片海域漂流，视觉焦点始终在格列佛漂流状态，时间为同一漂流阶段渐进，情绪为同一基调下渐进加深绝望，四维度均无强切换，保留5句豁免；句19含"very unhappy"，需情绪标记）

B8-7 | character_refs: ["C1"] | scene_refs: [] | 预估格数: 2
- One day I saw something very strange in the sky.
- It was afternoon, and the sun was very hot.
- Suddenly the sky became dark, and I could not see the sun at all.
- I looked up, and saw a huge object in the sky.
- （注：发现飞岛第一阶段——异象初现，4句；原句20-26共7句超过6句上限，在句23/24之间切分（句24是惊叹号高潮，视觉焦点切换到飞岛本体）；"One day"时间标记触发与B8-6的切分）

B8-8 | character_refs: ["C1"] | scene_refs: [] | 预估格数: 2
- It seemed to be an island, and it was flying!
- I looked at it through my telescope, and I saw people on the island.
- I was very surprised to see a flying island with people on it, and I did not know what to do.
- （注：发现飞岛第二阶段——确认飞岛有人，极度惊讶，3句；原句20-26强制拆分后的后半段；句26含"very surprised"，需情绪标记）

B8-9 | character_refs: ["C1"] | scene_refs: [] | 预估格数: 1
- I decided to call out to the people.
- Perhaps they would help me to escape.
- I shouted very loudly, and waved my arms.
- （注：格列佛主动呼救，3句连续动作同一节拍；与B8-8的切分由条件D触发——"被动发现"到"主动求救"是不同叙事阶段，第一阶段结束构成第二阶段入场条件）

B8-10 | character_refs: [] | scene_refs: [] | 预估格数: 1
- Some of the people on the flying island heard me, and they looked down at me.
- Soon there was a crowd of people looking down at me.
- （注：视角切换到飞岛上人群，2句；§3触发切换第3条——叙述视角从格列佛（下方）切换到飞岛居民（上方俯视），必须切分）

B8-11 | character_refs: ["C1"] | scene_refs: [] | 预估格数: 3
- The island began to come close to me.
- Someone threw down a piece of rope with a chair tied to it.
- I climbed into the chair, and I was pulled up towards the mysterious island.
- （注：3步物理动作链——飞岛靠近→绳椅下落→被拉上去，触发§4条件C子集（≥3个互相依赖步骤），需3格）

B8-12 | character_refs: ["C1"] | scene_refs: ["S19"] | 预估格数: 2
- A crowd of people was waiting to welcome me when I arrived.
- They told me that the name of their island was Laputa.
- （注：到达飞岛，新叙事阶段；条件D触发——到达与上升是不同叙事功能阶段，2句）

B8-13 | character_refs: ["C1"] | scene_refs: ["S19"] | 预估格数: 2
- They were strange people.
- Their heads were very flat, and one eye looked up to the sky and the other eye looked in the opposite direction.
- The clothes of the rich people were strange, too.
- They had pictures of stars and musical instruments on them.
- （注：拉普塔人外貌描述第一段，4句，同一描述节拍；原句37-47共11句超6句，在句40/41切分）

B8-14 | character_refs: ["C1"] | scene_refs: ["S19"] | 预估格数: 2
- The rich people all had servants, and I saw that the servants carried sticks with them.
- Sometimes the servants touched their masters on the mouth or ears with the stick.
- I did not understand why they did this until someone explained it to me.
- （注：仆人棍子谜题，3句；与B8-13切分由视觉焦点切换触发——从外貌描述切换到行为观察）

B8-15 | character_refs: ["C1"] | scene_refs: ["S19"] | 预估格数: 2
- The rich people of the island were all mathematicians and thinkers.
- They were very busy with their thoughts.
- When someone wanted to speak to them, they did not notice.
- Their servants had to touch them with a stick to make them listen.
- （注：解释棍子谜底，4句，同一解释节拍；与B8-14切分由§3条件5触发——谜底揭晓属新戏剧性信息）

B8-16 | character_refs: ["C1", "C18"] | scene_refs: ["S20"] | 预估格数: 2
- Some of the people took me to the King's palace, and he invited me to have dinner with him.
- The King was a very polite man, and he wanted me to be his guest and learn their language.
- （注：进入王宫，新场景；2句，空间切换触发切分）

B8-17 | character_refs: ["C1"] | scene_refs: ["S20"] | 预估格数: 2
- The people of the island were only interested in mathematics and music.
- They spent their time solving mathematical problems, and thinking about music.
- They were very good at making theories, but they were not practical people at all.
- They could not make proper clothes or build decent houses.
- （注：对拉普塔人局限的整体评价，4句；原句50-56共7句超6句上限，在句53/54切分）

B8-18 | character_refs: ["C1"] | scene_refs: ["S20"] | 预估格数: 1
- No one wanted to talk to me about my adventures, or to learn about my country.
- All they wanted to do was talk about mathematics and music.
- After a while, they stopped talking to me completely.
- （注：格列佛被孤立的结果，3句；与B8-17切分由视觉焦点切换触发——从"拉普塔人的整体状态"切换到"格列佛个人处境"）

B8-19 | character_refs: ["C1", "C19"] | scene_refs: ["S20"] | 预估格数: 2
- There was a very important man at the court who became a friend of mine.
- He was a cousin of the King, and had a very important position in the country.
- Everyone thought he was stupid because he was not good at mathematics or music.
- He was the only man on the island who was interested in talking to me about my adventures and about England.
- He asked me many questions about the places I had visited, and their systems of government.
- （注：已扫描4对相邻句，视觉焦点（介绍堂兄）、空间（飞岛宫廷）、时间（在岛期间）、情绪（温和友谊）四维度均无强切换，保留5句豁免）

B8-20 | character_refs: ["C1", "C18", "C19"] | scene_refs: ["S20"] | 预估格数: 2
- After a month on the flying island, I wanted to leave.
- The people were kind to me, but they only wanted to talk about mathematics and music.
- They were not interested in me.
- I learnt that the King of the island was also the King of the country below the island.
- This country is called Balnibarbi, and its capital city is called Lagado.
- I asked the King's permission to visit the other parts of his realm, and he gave it to me.
- （注：已扫描5对相邻句，整体属格列佛决定离岛的决策过程，视觉焦点（格列佛主观想法+向国王请求）、空间（飞岛）、时间（一个月后）、情绪（平静决定）四维度无强切换，保留6句豁免）

B8-21 | character_refs: ["C1", "C19"] | scene_refs: ["S20"] | 预估格数: 2
- My friend, the King's cousin, was sorry to see me go.
- 'I'll miss you,' he said, 'I've enjoyed our conversations.
- But when you are in Balnibarbi, please see my friend Lord Munodi.
- He'll show you the country.'
- （注：堂兄依依惜别并嘱咐，4句；句69-71为同一说话者连续台词，无说话方切换，属单对话节拍，合并为1镜）

B8-22 | character_refs: ["C1", "C20"] | scene_refs: ["S21"] | 预估格数: 3
- I met Lord Munodi in the capital city, Lagado.
- He was a very polite and intelligent man, and he took me on a tour of the country.
- I saw that the whole country was very badly organised.
- The houses in the towns were very ugly, and the people seemed poor.
- The land in the countryside seemed rich, but there were very few farms.
- I told Lord Munodi what I thought.
- （注：已扫描5对相邻句，到达拉格多并参观全过程；视觉焦点/空间/时间/情绪均属同一叙事单元（到达后所见所感），四维度无强切换，保留6句豁免）

B8-23 | character_refs: ["C1", "C20"] | scene_refs: ["S21"] | 预估格数: 2
- 'Every country has its own traditions,' he said quietly.
- 'Our country is certainly different to England.'
- （注：蒙诺地委婉回应，同一说话者连续2句，1个对话节拍；与B8-22切分由§3说话方切换触发——格列佛告知→蒙诺地回应）

B8-24 | character_refs: ["C1", "C20"] | scene_refs: [] | 预估格数: 2
- He took me to see his own farm, and this was very different to the other farms in the country.
- Everything was very well organised, and the people seemed happy and rich.
- （注：新场景（蒙诺地农场），时间/空间切换触发切分，2句）

B8-25 | character_refs: ["C1", "C20"] | scene_refs: [] | 预估格数: 2
- 'What a difference!' I said.
- 'Your farm is the best in the whole country.'
- 'Thank you,' he replied.
- 'I'm happy that you like my farm.'
- （注：格列佛赞叹→蒙诺地感谢，2回合轻松对话，4句；原句82-89共8句超6句，在句85/86切分；§4条件B在此不触发——双方情绪方向一致（互相满意），非期待→落空结构）

B8-26 | character_refs: ["C1", "C20"] | scene_refs: [] | 预估格数: 2
- Then he looked very sad.
- 'But it will not always be like this.
- I have just received some bad news.
- I will soon have to change everything, and make this farm like the others you have seen.'
- （注：情绪强切换——"Then he looked very sad"标志从轻松对话到悲伤，§4条件B触发（情绪方向相反：友好互赞→悲伤坏消息），必须独立成镜；4句；"looked very sad"需情绪标记）

B8-27 | character_refs: ["C1", "C20"] | scene_refs: [] | 预估格数: 1
- I was very surprised at what he told me, and I asked him to explain.
- Then he told me the recent history of Balnibarbi.
- （注：过渡性叙事，2句，格列佛惊讶并请求解释；"very surprised"需情绪标记）

B8-28 | character_refs: ["C1", "C20"] | scene_refs: [] | 预估格数: 3
- 'About forty years ago,' he said, 'the country was all like this.
- The towns were well organised, and the farms were rich.
- Then some people from Balnibarbi went up to Laputa.
- They stayed there for about five months.
- When they came back here, they brought with them ideas about mathematics and music.
- They asked the King to begin an academy at Lagado.
- （注：蒙诺地讲述历史前段——40年前好→拉普塔归来→带回想法→建学院，6句；原句92-100共9句超6句，在句97/98切分（句98"That is the cause of the problem"是从历史叙述切换到现状结论的视觉焦点变化）；6句已达绝对上限）

B8-29 | character_refs: ["C1", "C20"] | scene_refs: [] | 预估格数: 2
- That is the cause of the problem.
- The professors at the academy have all got new ideas - but none of their ideas work.
- They are destroying the country.'
- （注：历史叙述的结论段，3句；与B8-28切分由叙事功能切换触发——从历史经过切换到现状结论，属§4条件D（不同叙事阶段）的弱触发）

B8-30 | character_refs: ["C1", "C20"] | scene_refs: ["S22"] | 预估格数: 2
- I told Lord Munodi that I wanted to see this academy, and he asked a friend to take me there.
- The academy was one of the strangest places I have ever seen.
- It was full of professors, and each professor was working on a different project.
- （注：前往参观学院，新场景（S22学院），3句；空间切换触发切分）

B8-31 | character_refs: ["C1", "C21"] | scene_refs: ["S22"] | 预估格数: 2
- The first professor that I saw had a special project.
- He wanted to extract sunlight from cucumbers.
- 'We can use the sunlight to heat the houses in winter,' he told me.
- He was sure that his project would be a great success.
- （注：第一位教授（提取阳光），4句，同一场景同一人物介绍节拍）

B8-32 | character_refs: ["C1", "C22"] | scene_refs: ["S22"] | 预估格数: 2
- There was a school of languages in the academy, and I went there to see what the professors were doing.
- One professor had a project to make conversations shorter.
- He was working on a language that only had nouns in it.
- （注：移动到语言学院区域，新视觉焦点/空间位移，3句；与B8-31切分由空间位移触发——从阳光教授工作台移到语言学院）

B8-33 | character_refs: ["C1", "C23"] | scene_refs: ["S22"] | 预估格数: 2
- Another professor had a project for a new kind of language.
- 'Words are really the names of things,' he explained to me.
- 'In my new language, we use things instead of words.
- Everybody carries a bag with the things in it that he wants to talk about.
- When he wants to talk, he brings out the thing he wants to talk about, and shows it to the people.'
- （注：已扫描4对相邻句，物件语言教授连续解释，同一说话者，同一场景，同一话题，情绪基调一致，四维度均无切换，保留5句豁免）

---

## 覆盖验证

原文总句数：115
| 分镜 | 覆盖句数 | 原文句序 |
|------|---------|---------|
| B8-1 | 3 | 1-3 |
| B8-2 | 3 | 4-6 |
| B8-3 | 3 | 7-9 |
| B8-4 | 1 | 10 |
| B8-5 | 4 | 11-14 |
| B8-6 | 5 | 15-19 |
| B8-7 | 4 | 20-23 |
| B8-8 | 3 | 24-26 |
| B8-9 | 3 | 27-29 |
| B8-10 | 2 | 30-31 |
| B8-11 | 3 | 32-34 |
| B8-12 | 2 | 35-36 |
| B8-13 | 4 | 37-40 |
| B8-14 | 3 | 41-43 |
| B8-15 | 4 | 44-47 |
| B8-16 | 2 | 48-49 |
| B8-17 | 4 | 50-53 |
| B8-18 | 3 | 54-56 |
| B8-19 | 5 | 57-61 |
| B8-20 | 6 | 62-67 |
| B8-21 | 4 | 68-71 |
| B8-22 | 6 | 72-77 |
| B8-23 | 2 | 78-79 |
| B8-24 | 2 | 80-81 |
| B8-25 | 4 | 82-85 |
| B8-26 | 4 | 86-89 |
| B8-27 | 2 | 90-91 |
| B8-28 | 6 | 92-97 |
| B8-29 | 3 | 98-100 |
| B8-30 | 3 | 101-103 |
| B8-31 | 4 | 104-107 |
| B8-32 | 3 | 108-110 |
| B8-33 | 5 | 111-115 |
| **合计** | **115** | |

未覆盖句数：0 ✓
最大 covered_sentences：6（B8-20、B8-22、B8-28）≤ 6句上限 ✓
