#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""临时脚本：保存当前学习笔记到飞书"""

import sys
import os

# 直接设置环境变量（绕过需要重启终端的问题）
os.environ["FEISHU_APP_ID"] = "cli_a90846c997795bc4"
os.environ["FEISHU_APP_SECRET"] = "JdXarMiUhwCgbrp97OjUhdp28IJvuQ6k"
os.environ["FEISHU_BITABLE_APP_TOKEN"] = "DLMfbXCvNaGsbksuqKPcoVBFnZK"
os.environ["FEISHU_BITABLE_TABLE_ID"] = "tblAJ5G6R4YoRnGH"

# 导入飞书模块
from feishu_bitable_pro import save_feynman_note_pro

# 学习笔记内容
concept = "刻意练习"

simple_explanation = """刻意练习就是一种**特殊的练习方法**，它和我们平常说的"多练习"完全不同。

核心要素：
1. **走出舒适区** - 故意选择你做不好的部分去练
2. **有明确目标** - 不是"我要练钢琴"，而是"我要把第3小节的八度音阶练到不出错"
3. **需要专注** - 全神贯注，不能边练边聊天
4. **有即时反馈** - 马上知道自己做对没有
5. **不断调整** - 根据反馈改进方法

核心思想：**天才不是天生的，而是通过正确方法练出来的**。关键不是练多久，而是**怎么练**。"""

analogy = """就像玩游戏打怪升级：
- **普通练习**：反复打新手村的史莱姆，打100次还是1级
- **刻意练习**：总是挑战比自己等级高一点的怪物，每次都要动脑筋想策略，看血条反馈调整打法，经验值蹭蹭涨

**健身房版**：
- 普通练习：每天举10kg哑铃50次，很轻松但肌肉不长
- 刻意练习：每周增加1-2kg，每组都举到力竭，请教练纠正动作，记录数据调整计划"""

gaps = """1. **舒适区边界**：最佳学习区在60-70%成功率的难度
2. **即时反馈**：可以录下来自己看、对比高手表现、用客观指标衡量
3. **天赋作用**：起步阶段天赋影响不大，99%的人还没练到需要担心天赋的程度
4. **一万小时定律**：忽略了练习质量，刻意练习1000小时 > 普通练习10000小时
5. **心理表征**：刻意练习的本质是建立更好的心理表征（大脑内部的信息模式）"""

refined_explanation = """**刻意练习**是一种科学的练习方法，告诉我们高手和普通人的差距主要不是天赋，而是**练习方法**。

5个核心要素：
1. **挑战甜蜜点** - 总是练习刚好够不到的东西（成功率60-70%）
2. **全神贯注** - 像考试一样专注
3. **明确的小目标** - 不是"练钢琴"，而是"把这4小节练到不看谱也不出错"
4. **即时反馈** - 马上知道对错（教练指导、录像回看、数据衡量）
5. **反复调整** - 根据反馈不断改进方法

**最重要的发现**：刻意练习会在大脑中建立"心理表征"，让复杂的事情变得简单。"""

key_takeaways = """1. **质量 > 数量** - 专注练习1小时，胜过分心练习10小时
2. **舒适是敌人** - 如果练习很轻松舒服，说明你在浪费时间
3. **反馈是关键** - 没有反馈的练习，只是在重复错误
4. **大脑可塑性** - 正确的练习会物理改变大脑结构
5. **人人可成为高手** - 刻意练习能让普通人达到专家水平

**设计刻意练习计划的5步法**：
1. 拆解技能树（把大目标拆成可练习的小技能）
2. 找到瓶颈（练最薄弱的，不是最喜欢的）
3. 设计小目标（SMART原则）
4. 设置反馈循环（每15-30分钟检查一次）
5. 循序渐进提高难度（掌握60-70%后立刻增加难度）"""

test_question = """刻意练习就是**专注练习你不会的，而不是重复你会的**。它有4个关键：1) 总是挑战刚好够不到的难度 2) 全神贯注不分心 3) 马上得到反馈知道对错 4) 根据反馈调整方法。普通人和高手的差距，90%来自练习方法，而不是天赋。一万小时定律是错的，关键不是练多久，而是**怎么练**。"""

remaining_questions = """1. 如何在编程中应用刻意练习？
2. 如何为不同技能领域设计专属的练习计划？
3. 如何在没有导师的情况下建立有效的反馈机制？
4. 心理表征在不同领域中如何具体体现？"""

# 调用保存函数
try:
    result = save_feynman_note_pro(
        concept=concept,
        simple_explanation=simple_explanation,
        analogy=analogy,
        gaps=gaps,
        refined_explanation=refined_explanation,
        key_takeaways=key_takeaways,
        test_question=test_question,
        mastery_level=4,  # 4星
        completion_status="learning",  # 学习中
        learning_duration=30,  # 估算学习时长30分钟
        remaining_questions=remaining_questions
    )

    if result:
        print("\n✅ 保存成功！")
        print(f"记录ID: {result.get('record_id', 'N/A')}")
    else:
        print("\n❌ 保存失败，请检查配置")

except Exception as e:
    print(f"\n❌ 发生错误: {e}")
    import traceback
    traceback.print_exc()
