# Feynman Technique

Apply the full Feynman learning technique to deeply understand a concept.

## Instructions

Work through all four steps of the Feynman technique. Be honest about gaps—they're the point.

**Always respond in Chinese (中文).**

### Output Format

**Concept**: [What are we trying to understand?]

---

## Step 1: Explain It Simply

*Explain as if teaching someone with no background in this field*

### Simple Explanation

[Write a plain-language explanation. Use everyday words. Avoid jargon. Aim for a bright 12-year-old to understand.]

### Analogy

[Create an analogy using something familiar to illustrate the concept]

---

## Step 2: Identify Gaps

*Where did the explanation get fuzzy, hand-wavy, or require jargon?*

### Gaps Found

| Gap | What I Said | What I'm Not Sure About |
|-----|-------------|------------------------|
| 1 | [vague part] | [the underlying question] |
| 2 | [vague part] | [the underlying question] |
| 3 | [vague part] | [the underlying question] |

### Jargon Used

| Term | Can I Explain It Simply? |
|------|-------------------------|
| [term] | Yes / No / Partially |

---

## Step 3: Fill the Gaps

*Research or think through each gap*

### Gap 1: [Topic]
- **The question**: [What wasn't clear?]
- **The answer**: [What I learned]
- **Now I can explain it as**: [Simple version]

### Gap 2: [Topic]
- **The question**: [What wasn't clear?]
- **The answer**: [What I learned]
- **Now I can explain it as**: [Simple version]

### Gap 3: [Topic]
- **The question**: [What wasn't clear?]
- **The answer**: [What I learned]
- **Now I can explain it as**: [Simple version]

---

## Step 4: Refined Explanation

*Rewrite the complete explanation with gaps filled and simpler language*

### Final Simple Explanation

[The improved, complete explanation in plain language]

### Improved Analogy

[A refined or new analogy that better captures the concept]

### Key Takeaways

1. [Core insight 1]
2. [Core insight 2]
3. [Core insight 3]

---

**Remaining Questions**
[What still feels unclear? These are topics for deeper study]

**Test Question**
If someone asked me to explain this in 30 seconds, I'd say:
> [Elevator pitch version]

---

## Post-Learning Action

After completing the Feynman analysis, ask the user:

**"Would you like to save this learning note to Feishu (飞书多维表格)?"**

If the user agrees (yes/好/保存), execute the following Python script to save the note:

```python
import sys
import os

# Add scripts directory to path
scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
sys.path.insert(0, scripts_dir)

from save_to_feishu import save_article_to_feishu

# Prepare the content
title = f"Feynman 学习笔记: {concept}"
content = f"""# {concept}

## 简单解释
{simple_explanation}

## 类比
{analogy}

## 发现的知识空白
{gaps_found}

## 精炼后的解释
{refined_explanation}

## 核心要点
{key_takeaways}

## 待深入问题
{remaining_questions}

## 30秒版本
{test_question}
"""

# Save to Feishu
if save_article_to_feishu(title, content):
    print("✅ 学习笔记已保存到飞书多维表格")
else:
    print("❌ 保存失败，请检查飞书配置")
    print("配置指南: ~/.agents/skills/feynman/references/feishu-setup-guide.md")
```

## Guidelines

- Don't pretend to understand—gaps are valuable
- Use analogies from everyday life
- If you need jargon, define it simply
- Shorter is usually better
- The "explain to a child" bar is high—take it seriously
- After completion, offer to save to Feishu for future reference

$ARGUMENTS
