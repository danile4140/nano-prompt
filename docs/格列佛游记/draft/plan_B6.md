# 第 6 章分镜计划（分镜 id 格式 B6-{seq}）

总分镜数：14

自检等式：5+4+1+2+3+3+3+3+5+2+4+4+3 = 45，未覆盖句数 = 0 ✓

---

## 句子分配表

B6-1 | character_refs: [C1, C9, C11, C13] | scene_refs: [S10] | 预估格数: 2
豁免说明：已扫描 4 对相邻句，四维度均无切换（视觉焦点为格列佛受访客围观的日常状态，时间为连续日子，空间为农夫家，情绪基调为平静愉快，句5农夫朋友的观察仍属同一"访客来看格列佛"情境），保留 5 句。
- I was happy with the farmer and his family, and the days passed quickly.
- There were always a lot of visitors to the house.
- They came to see me.
- They were all interested in the little man that the farmer had found in the field.
- One of the farmer's friends noticed that everybody in the village wanted to see me.

B6-2 | character_refs: [C9, C13] | scene_refs: [S10] | 预估格数: 2
- 'You could make a lot of money,' he told the farmer.
- 'Everybody in the village has seen the little man.
- Why don't you take him into town on market day?
- Make the people pay you to see him.'

B6-3 | character_refs: [C9] | scene_refs: [S10] | 预估格数: 1
触发-转折因果链（条件B）：句10（农夫接受建议）为触发动作，与 B6-4（格洛达尔奇反对）构成情绪方向相反的因果对，必须独立成镜。
- The farmer thought this was a good idea.

B6-4 | character_refs: [C11] | scene_refs: [S10] | 预估格数: 2
触发-转折因果链（条件B）：与 B6-3 对应，格洛达尔奇的反对（担心 + 知道格列佛羞于表演）为转折结果，必须独立成镜。
- Glumdalclitch did not like the idea, because she was afraid the people would hurt me.
- She also knew that I was very modest, and that I would not want to perform for the public.

B6-5 | character_refs: [C1, C9, C11] | scene_refs: [] | 预估格数: 2
注：旅途场景无对应 scene_refs ID，留空；画面为户外骑马出行路上。
- The next morning, however, the farmer took Glumdalclitch and me to town.
- They put me into a box on one of the horses, and the journey was very uncomfortable for me.
- The horse moved very violently, and it was like being in a ship during a storm.

B6-6 | character_refs: [C1, C9, C11] | scene_refs: [S12] | 预估格数: 2
- When we arrived at the town, we stayed in a hotel.
- The farmer told the people in the town about me, and lots of them came to see me.
- We organised a show for them.

B6-7 | character_refs: [C1, C11] | scene_refs: [S12] | 预估格数: 3
计划执行链（条件C）：句19（指令"站起来"）→ 句20（执行+鞠躬）→ 句21（观众反应），三步相互依赖，必须按步骤数分格，3 格。
- 'Stand up!' Glumdalclitch told me.
- I stood up, and bowed politely to the people in the room.
- They laughed, and clapped their hands.

B6-8 | character_refs: [C1, C11] | scene_refs: [S12] | 预估格数: 3
计划执行链（条件C）：句22（指令"拔剑"）→ 句23（执行+凶猛看人）→ 句24（观众再次反应），三步相互依赖，必须按步骤数分格，3 格。
- 'Take out your sword!' she said next.
- I took out my sword, and looked fiercely at the people in the room.
- Once again, everybody laughed and clapped their hands.

B6-9 | character_refs: [C1, C9] | scene_refs: [] | 预估格数: 2
注：巡演各城，无固定场景 ID，scene_refs 留空；画面可用地图路线图或序列条呈现多城镇巡演。
- The farmer made a lot of money, and he decided to travel to other towns.
- We went from town to town.
- Everyone came to see us, and I was very popular.

B6-10 | character_refs: [C1] | scene_refs: [] | 预估格数: 2
豁免说明：已扫描 4 对相邻句，四维度均无切换（视觉焦点始终为格列佛本人的状态，时间为连续悲苦生活时期，空间为各地巡演途中，情绪基调为持续痛苦与绝望的渐进深化），保留 5 句。
- We lived like this for a long time.
- It was a terrible life for me.
- I did not like to be a spectacle for the people.
- I was unhappy, and I became ill.
- Every day I lost strength, and I thought I was going to die.

B6-11 | character_refs: [C11, C9] | scene_refs: [] | 预估格数: 2
多主体独立表态（条件A）：句33 格洛达尔奇担忧 vs 句34 农夫父亲冷漠，两主体对格列佛病情的反应截然相反，删去任一格则该主体的表态从画面消失，必须分格展示。
- Glumdalclitch was worried about me, but her father just wanted to make as much money as possible from me.
- He did not care about me at all.

B6-12 | character_refs: [C1, C9, C11] | scene_refs: [S12] | 预估格数: 2
注：首都旅馆无专属场景 ID，借用 S12（小镇旅馆表演室）；后续 prompt 写作时注明首都规模更大。
- One day we came to the capital city of Brobdingnag.
- We performed our show for the people as usual.
- A lot of people came to see me, and the farmer was happy.
- We decided to stay in the city for a while.

B6-13 | character_refs: [C9] | scene_refs: [S12] | 预估格数: 2
注：使者（宫廷来人）无对应角色 ID，不列入 character_refs；句41-42 为使者连续台词，同一说话者无切换。
- Soon the whole city was talking about me.
- One day a man from the palace came to talk to the farmer.
- 'The Queen wants to see this little man,' he said.
- 'Bring him to the palace tonight.'

B6-14 | character_refs: [C1, C9, C11] | scene_refs: [S12] | 预估格数: 2
触发-转折因果链（条件B）：B6-13 使者传旨（触发/严肃事件）→ B6-14 三人兴奋（结果/情绪反转），情绪方向从"严肃传旨"转为"激动兴奋"，必须独立成镜。
- The farmer, Glumdalclitch and I were very excited.
- We decided to perform a very special show for the Queen.
- We wanted to please her.
