#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书多维表格集成脚本 - 专业版（方案C）
用于将 Feynman 学习笔记自动记录到飞书多维表格，支持完整的学习管理功能
"""

import os
import sys
import json
import requests
import re
import base64
import zlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

# 设置标准输出编码为 UTF-8（Windows 兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 从环境变量读取配置
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_BITABLE_APP_TOKEN = os.getenv("FEISHU_BITABLE_APP_TOKEN", "")
FEISHU_BITABLE_TABLE_ID = os.getenv("FEISHU_BITABLE_TABLE_ID", "")

BASE_URL = "https://open.feishu.cn/open-apis"

# 复习间隔配置（基于遗忘曲线，单位：天）
REVIEW_INTERVALS = [1, 3, 7, 15, 30, 60]

# 默认分类标签选项
DEFAULT_CATEGORIES = [
    "前端开发", "后端开发", "算法与数据结构", "数据库",
    "网络协议", "操作系统", "DevOps", "云计算",
    "架构设计", "AI与机器学习", "移动开发", "安全",
    "测试", "工具与效率", "其他"
]

# 完成状态选项
COMPLETION_STATUS = {
    "learning": "🟡 学习中",
    "mastered": "🟢 已掌握",
    "review": "🔵 需复习",
    "deep_dive": "🟠 待深入",
    "archived": "⚪ 已归档"
}


def get_tenant_access_token() -> Optional[str]:
    """获取 tenant_access_token"""
    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        data = resp.json()
        if data.get("code") == 0:
            return data.get("tenant_access_token")
        else:
            print(f"❌ 获取 token 失败: {data.get('msg')}")
            return None
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    从文本中提取关键词（简单实现）

    Args:
        text: 待提取的文本
        max_keywords: 最大关键词数量

    Returns:
        关键词列表
    """
    # 常见技术关键词模式
    tech_patterns = [
        r'\b[A-Z][a-zA-Z]+\b',  # 大写开头的词（如 React, Python）
        r'\b\w+(?:JS|js)\b',     # JS相关（如 Node.js, Vue.js）
        r'\b[A-Z]{2,}\b',        # 全大写缩写（如 API, HTTP）
        r'\b\w+-\w+\b',          # 连字符词（如 cross-platform）
    ]

    keywords = set()
    for pattern in tech_patterns:
        matches = re.findall(pattern, text)
        keywords.update(matches)

    # 常见技术词汇
    common_tech_terms = [
        'async', 'await', 'promise', 'callback', 'function',
        'class', 'interface', 'type', 'module', 'component',
        'state', 'props', 'hook', 'context', 'reducer',
        'database', 'query', 'index', 'transaction', 'cache',
        'server', 'client', 'request', 'response', 'API',
        'frontend', 'backend', 'fullstack', 'microservice',
        'docker', 'kubernetes', 'deployment', 'CI/CD'
    ]

    text_lower = text.lower()
    for term in common_tech_terms:
        if term in text_lower:
            keywords.add(term.capitalize())

    # 限制数量并排序
    return sorted(list(keywords))[:max_keywords]


def calculate_next_review(learning_date: datetime, review_count: int = 0) -> datetime:
    """
    计算下次复习时间（基于遗忘曲线）

    Args:
        learning_date: 学习日期
        review_count: 已复习次数

    Returns:
        下次复习的日期时间
    """
    if review_count >= len(REVIEW_INTERVALS):
        # 超过预设间隔，使用最后一个间隔
        interval = REVIEW_INTERVALS[-1]
    else:
        interval = REVIEW_INTERVALS[review_count]

    return learning_date + timedelta(days=interval)


def auto_categorize(concept: str, content: str) -> List[str]:
    """
    根据概念和内容自动分类

    Args:
        concept: 概念名称
        content: 学习内容

    Returns:
        分类标签列表
    """
    categories = []
    combined_text = (concept + " " + content).lower()

    # 分类关键词映射
    category_keywords = {
        "前端开发": ["react", "vue", "angular", "javascript", "typescript", "html", "css", "dom", "webpack", "前端"],
        "后端开发": ["node", "python", "java", "go", "rust", "api", "server", "后端", "服务器"],
        "算法与数据结构": ["算法", "数据结构", "排序", "搜索", "树", "图", "链表", "栈", "队列", "复杂度"],
        "数据库": ["sql", "mysql", "postgresql", "mongodb", "redis", "数据库", "查询", "索引"],
        "网络协议": ["http", "tcp", "udp", "ip", "dns", "网络", "协议", "socket"],
        "操作系统": ["linux", "unix", "windows", "进程", "线程", "内存", "操作系统"],
        "DevOps": ["docker", "kubernetes", "ci/cd", "jenkins", "gitlab", "devops", "部署"],
        "云计算": ["aws", "azure", "gcp", "云", "serverless", "lambda"],
        "架构设计": ["架构", "设计模式", "微服务", "分布式", "高可用", "负载均衡"],
        "AI与机器学习": ["ai", "machine learning", "deep learning", "neural", "tensorflow", "pytorch", "人工智能"],
        "移动开发": ["ios", "android", "react native", "flutter", "移动", "app"],
        "安全": ["security", "加密", "认证", "授权", "xss", "csrf", "安全"],
        "测试": ["test", "testing", "unit test", "jest", "pytest", "测试"],
    }

    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in combined_text:
                categories.append(category)
                break  # 每个分类只添加一次

    # 如果没有匹配到任何分类，添加"其他"
    if not categories:
        categories.append("其他")

    return categories


def save_feynman_note_pro(
    concept: str,
    simple_explanation: str,
    analogy: str,
    gaps: str,
    refined_explanation: str,
    key_takeaways: str,
    test_question: str,
    categories: Optional[List[str]] = None,
    mastery_level: int = 3,
    related_concepts: Optional[List[str]] = None,
    learning_duration: Optional[int] = None,
    completion_status: str = "learning",
    remaining_questions: str = "",
    mindmap_url: str = "",
    auto_extract_keywords: bool = True,
    auto_categorize_enabled: bool = True
) -> bool:
    """
    保存 Feynman 笔记到飞书（专业版）

    Args:
        concept: 概念名称
        simple_explanation: 简单解释
        analogy: 类比
        gaps: 知识空白
        refined_explanation: 精炼解释
        key_takeaways: 核心要点
        test_question: 测试问题
        categories: 分类标签（可选，为空则自动分类）
        mastery_level: 掌握程度（1-5星，默认3星）
        related_concepts: 相关概念列表
        learning_duration: 学习时长（分钟）
        completion_status: 完成状态（learning/mastered/review/deep_dive/archived）
        remaining_questions: 待深入问题
        mindmap_url: 思维导图链接
        auto_extract_keywords: 是否自动提取关键词
        auto_categorize_enabled: 是否自动分类

    Returns:
        bool: 是否保存成功
    """
    # 验证环境变量
    if not all([FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_BITABLE_APP_TOKEN, FEISHU_BITABLE_TABLE_ID]):
        print("❌ 缺少必要的环境变量配置，请检查:")
        print(f"  FEISHU_APP_ID: {'✓' if FEISHU_APP_ID else '✗'}")
        print(f"  FEISHU_APP_SECRET: {'✓' if FEISHU_APP_SECRET else '✗'}")
        print(f"  FEISHU_BITABLE_APP_TOKEN: {'✓' if FEISHU_BITABLE_APP_TOKEN else '✗'}")
        print(f"  FEISHU_BITABLE_TABLE_ID: {'✓' if FEISHU_BITABLE_TABLE_ID else '✗'}")
        return False

    # 获取访问令牌
    token = get_tenant_access_token()
    if not token:
        return False

    # 自动分类
    if categories is None or (auto_categorize_enabled and not categories):
        categories = auto_categorize(concept, simple_explanation + " " + refined_explanation)

    # 自动提取关键词
    ai_keywords = []
    if auto_extract_keywords:
        full_content = f"{concept} {simple_explanation} {refined_explanation}"
        ai_keywords = extract_keywords(full_content)

    # 计算下次复习时间
    learning_date = datetime.now()
    next_review = calculate_next_review(learning_date, review_count=0)

    # 构建 API URL
    url = f"{BASE_URL}/bitable/v1/apps/{FEISHU_BITABLE_APP_TOKEN}/tables/{FEISHU_BITABLE_TABLE_ID}/records"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 构建记录数据（适配用户表格配置）
    # 注意：用户的表格字段类型为单行文本，所以需要截断长文本
    def truncate_text(text: str, max_length: int = 5000) -> str:
        """截断文本以适应单行文本字段"""
        return text[:max_length] if len(text) > max_length else text

    # 生成 Mermaid mindmap 语法并创建在线 URL
    def generate_mermaid_mindmap_url() -> str:
        """生成 Mermaid mindmap 语法并返回在线查看 URL"""
        # 清理文本，移除特殊字符
        def clean_text(text: str, max_len: int = 50) -> str:
            text = text.replace('"', "'").replace('\n', ' ').replace('\r', '')
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:max_len] + "..." if len(text) > max_len else text

        # 构建 Mermaid mindmap 语法
        mermaid_lines = ["mindmap"]
        mermaid_lines.append(f"  root(({clean_text(concept, 30)}))")

        # 添加核心理解分支
        if simple_explanation:
            mermaid_lines.append("    核心理解")
            summary = clean_text(simple_explanation, 60)
            mermaid_lines.append(f"      {summary}")

        # 添加类比分支
        if analogy:
            mermaid_lines.append("    类比说明")
            analogy_text = clean_text(analogy, 60)
            mermaid_lines.append(f"      {analogy_text}")

        # 添加核心要点分支
        if key_takeaways:
            mermaid_lines.append("    核心要点")
            takeaway_lines = key_takeaways.split('\n')[:3]
            for line in takeaway_lines:
                if line.strip():
                    clean_line = clean_text(line.strip().lstrip('0123456789.-) '), 40)
                    if clean_line:
                        mermaid_lines.append(f"      {clean_line}")

        # 添加知识空白分支
        if gaps:
            mermaid_lines.append("    知识空白")
            gap_lines = gaps.split('\n')[:2]
            for gap in gap_lines:
                if gap.strip():
                    clean_gap = clean_text(gap.strip(), 40)
                    mermaid_lines.append(f"      {clean_gap}")

        # 添加学习状态分支
        mermaid_lines.append("    学习状态")
        mermaid_lines.append(f"      掌握: {'⭐' * mastery_level}")
        status = COMPLETION_STATUS.get(completion_status, COMPLETION_STATUS['learning'])
        mermaid_lines.append(f"      状态: {status}")

        # 生成完整的 Mermaid 代码
        mermaid_code = '\n'.join(mermaid_lines)

        # 创建 Mermaid Live Editor URL
        # 正确的格式: https://mermaid.live/edit#pako:COMPRESSED_BASE64
        # 使用 pako (zlib deflate) 压缩
        mermaid_config = {
            "code": mermaid_code,
            "mermaid": {"theme": "default"},
            "autoSync": True,
            "updateDiagram": True
        }

        try:
            # 将配置转为 JSON 字符串
            json_str = json.dumps(mermaid_config, ensure_ascii=False)

            # 使用 zlib deflate 压缩（pako 兼容格式）
            compressed = zlib.compress(json_str.encode('utf-8'), level=9)[2:-4]  # 去除 zlib 头尾

            # Base64 URL-safe 编码
            encoded = base64.urlsafe_b64encode(compressed).decode('utf-8').rstrip('=')

            # 生成在线 URL
            online_url = f"https://mermaid.live/edit#pako:{encoded}"

            return online_url
        except Exception as e:
            # 如果压缩失败，返回简单的文本说明
            print(f"生成思维导图 URL 失败: {e}")
            return f"思维导图: {concept} (查看完整笔记获取详情)"

    # 生成思维导图（Markdown树状结构，用于备份）
    def generate_mindmap_markdown() -> str:
        """生成Markdown格式的思维导图结构（备份文本版）"""
        mindmap_parts = [
            f"## 思维导图: {concept}\n\n",
            f"### 📌 中心概念\n",
            f"**{concept}**\n\n",
        ]

        # 添加简单解释分支
        if simple_explanation:
            simple_summary = simple_explanation[:100] + "..." if len(simple_explanation) > 100 else simple_explanation
            mindmap_parts.append(f"### 🎯 核心理解\n")
            mindmap_parts.append(f"- {simple_summary.replace(chr(10), ' ')}\n\n")

        # 添加类比分支
        if analogy:
            analogy_summary = analogy[:100] + "..." if len(analogy) > 100 else analogy
            mindmap_parts.append(f"### 🔄 类比\n")
            mindmap_parts.append(f"- {analogy_summary.replace(chr(10), ' ')}\n\n")

        # 添加知识结构
        if gaps:
            mindmap_parts.append(f"### 🔍 知识空白\n")
            gap_lines = gaps.split('\n')[:3]  # 最多3个空白
            for gap in gap_lines:
                if gap.strip():
                    mindmap_parts.append(f"- {gap.strip()[:80]}\n")
            mindmap_parts.append("\n")

        # 添加核心要点
        if key_takeaways:
            mindmap_parts.append(f"### ⭐ 核心要点\n")
            takeaway_lines = key_takeaways.split('\n')
            for line in takeaway_lines:
                if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith('-')):
                    clean_line = line.strip().lstrip('0123456789.-) ')
                    if clean_line:
                        mindmap_parts.append(f"- {clean_line}\n")
            mindmap_parts.append("\n")

        # 添加关键词云
        if ai_keywords:
            mindmap_parts.append(f"### 🔑 关键词\n")
            mindmap_parts.append(f"`{' | '.join(ai_keywords[:8])}`\n\n")

        # 添加学习状态
        mindmap_parts.append(f"### 📊 学习状态\n")
        mindmap_parts.append(f"- 掌握程度: {'⭐' * mastery_level}\n")
        mindmap_parts.append(f"- 完成状态: {COMPLETION_STATUS.get(completion_status, COMPLETION_STATUS['learning'])}\n")
        mindmap_parts.append(f"- 分类: {', '.join(categories)}\n")

        return "".join(mindmap_parts)

    # 生成完整的Markdown格式学习笔记（用于"正文内容"字段）
    def generate_full_content() -> str:
        """生成完整的Feynman学习笔记（Markdown格式）"""
        content_parts = [
            f"# {concept}\n",
            f"**分类**: {', '.join(categories)}\n",
            f"**掌握程度**: {'⭐' * mastery_level}\n",
            f"**完成状态**: {COMPLETION_STATUS.get(completion_status, COMPLETION_STATUS['learning'])}\n",
            "\n---\n",
            "\n## Step 1: 简单解释\n",
            f"\n{simple_explanation}\n",
            "\n### 类比\n",
            f"\n{analogy}\n",
            "\n---\n",
            "\n## Step 2: 知识空白\n",
            f"\n{gaps}\n",
            "\n---\n",
            "\n## Step 4: 精炼解释\n",
            f"\n{refined_explanation}\n",
            "\n### 核心要点\n",
            f"\n{key_takeaways}\n",
            "\n---\n",
            "\n## 30秒电梯测试\n",
            f"\n{test_question}\n"
        ]

        # 如果有AI关键词，添加到笔记中
        if ai_keywords:
            content_parts.append(f"\n**关键词**: {', '.join(ai_keywords[:10])}\n")

        return "".join(content_parts)

    # 生成完整内容和思维导图
    full_content = generate_full_content()
    mindmap_markdown = generate_mindmap_markdown()  # 生成 Markdown 格式思维导图

    fields = {
        "概念": concept,
        "正文内容": truncate_text(full_content),  # 完整的Markdown笔记
        "分类标签": categories,  # 多选类型，正常
        "简单解释": truncate_text(simple_explanation),  # 单行文本
        "类比": truncate_text(analogy),  # 单行文本
        "知识空白": truncate_text(gaps),  # 单行文本
        "精炼解释": truncate_text(refined_explanation),  # 单行文本
        "核心要点": truncate_text(key_takeaways),  # 单行文本
        "测试问题": truncate_text(test_question),  # 单行文本
        "掌握程度": mastery_level,  # 评分类型，传入数字 1-5
        "学习日期": int(learning_date.timestamp() * 1000),
        "完成状态": COMPLETION_STATUS.get(completion_status, COMPLETION_STATUS["learning"]),
    }

    # 添加可选字段（适配单行文本）
    if ai_keywords:
        # AI关键词是单行文本，用逗号分隔
        fields["AI关键词"] = ", ".join(ai_keywords[:10])  # 最多10个关键词

    # 保存 Markdown 格式的思维导图
    if mindmap_url:
        # 如果用户手动提供了思维导图URL，优先使用
        fields["思维导图"] = mindmap_url
    else:
        # 否则使用 Markdown 格式的思维导图
        fields["思维导图"] = truncate_text(mindmap_markdown)

    # 注意：以下字段在用户表格中不存在，已移除
    # - 下次复习（但我们仍在后台计算，用于显示）
    # - 学习时长
    # - 待深入问题

    # 注意：相关概念需要记录ID，暂时不支持自动关联
    # 后续可以通过查询已有记录来实现

    payload = {"fields": fields}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        data = resp.json()

        if data.get("code") == 0:
            record_id = data.get("data", {}).get("record", {}).get("record_id")
            print(f"\n✅ Feynman 学习笔记已保存到飞书多维表格！")
            print(f"   📌 概念: {concept}")
            print(f"   🏷️  分类: {', '.join(categories)}")
            print(f"   ⭐ 掌握程度: {'⭐' * mastery_level}")
            print(f"   📅 下次复习: {next_review.strftime('%Y-%m-%d')}")
            if ai_keywords:
                print(f"   🔑 关键词: {', '.join(ai_keywords[:5])}{'...' if len(ai_keywords) > 5 else ''}")
            print(f"   🆔 记录ID: {record_id}")
            print(f"   🔗 查看链接: https://my.feishu.cn/base/{FEISHU_BITABLE_APP_TOKEN}?table={FEISHU_BITABLE_TABLE_ID}&record={record_id}\n")
            return True
        else:
            print(f"❌ 保存失败: {data.get('msg')}")
            print(f"   错误代码: {data.get('code')}")
            if data.get('code') == 1254044:
                print(f"   💡 提示: 请检查多维表格字段配置是否与脚本匹配")
                print(f"   📖 参考文档: feynman/references/table-setup-guide-pro.md")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False


def parse_feynman_markdown(markdown_content: str) -> Dict[str, Any]:
    """
    从 Markdown 格式的 Feynman 笔记中解析数据

    Args:
        markdown_content: Markdown 格式的学习笔记

    Returns:
        解析后的数据字典
    """
    data = {
        "concept": "",
        "simple_explanation": "",
        "analogy": "",
        "gaps": "",
        "refined_explanation": "",
        "key_takeaways": "",
        "test_question": "",
    }

    # 提取概念
    concept_match = re.search(r'\*\*Concept\*\*:\s*\[(.*?)\]', markdown_content)
    if concept_match:
        data["concept"] = concept_match.group(1)

    # 提取简单解释
    simple_match = re.search(r'## Step 1: Explain It Simply\s*.*?### Simple Explanation\s*(.*?)(?=###|##|$)',
                            markdown_content, re.DOTALL)
    if simple_match:
        data["simple_explanation"] = simple_match.group(1).strip()

    # 提取类比
    analogy_match = re.search(r'### Analogy\s*(.*?)(?=---|##|$)', markdown_content, re.DOTALL)
    if analogy_match:
        data["analogy"] = analogy_match.group(1).strip()

    # 提取知识空白
    gaps_match = re.search(r'## Step 2: Identify Gaps\s*(.*?)(?=##|$)', markdown_content, re.DOTALL)
    if gaps_match:
        data["gaps"] = gaps_match.group(1).strip()

    # 提取精炼解释
    refined_match = re.search(r'### Final Simple Explanation\s*(.*?)(?=###|##|$)', markdown_content, re.DOTALL)
    if refined_match:
        data["refined_explanation"] = refined_match.group(1).strip()

    # 提取核心要点
    takeaways_match = re.search(r'### Key Takeaways\s*(.*?)(?=---|##|$)', markdown_content, re.DOTALL)
    if takeaways_match:
        data["key_takeaways"] = takeaways_match.group(1).strip()

    # 提取测试问题
    test_match = re.search(r'If someone asked me to explain this in 30 seconds.*?\n\s*>\s*(.*?)(?=##|$)',
                          markdown_content, re.DOTALL)
    if test_match:
        data["test_question"] = test_match.group(1).strip()

    return data


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            # 测试模式
            print("🧪 运行 Feynman 飞书集成测试（专业版）...\n")

            test_data = {
                "concept": "React Hooks 测试",
                "simple_explanation": "React Hooks 是一种让函数组件也能使用状态和其他 React 特性的方法。",
                "analogy": "就像给普通自行车加装了变速器和刹车系统，让它拥有了山地车的功能。",
                "gaps": "1. Hook 的底层实现原理不清楚\n2. 为什么不能在条件语句中使用 Hook",
                "refined_explanation": "React Hooks 是 React 16.8 引入的特性，让函数组件能够使用状态管理、生命周期等功能。最常用的是 useState 和 useEffect。",
                "key_takeaways": "1. Hooks 让代码更简洁\n2. 遵循 Hooks 规则很重要\n3. 自定义 Hook 可以复用逻辑",
                "test_question": "React Hooks 让函数组件也能管理状态和副作用，最常用的是 useState 和 useEffect。",
                "mastery_level": 4,
                "completion_status": "mastered",
                "learning_duration": 45,
                "remaining_questions": "Hook 在 Fiber 架构中是如何工作的？"
            }

            if save_feynman_note_pro(**test_data):
                print("✅ 测试成功！请检查你的飞书多维表格。")
                print(f"🔗 表格链接: https://my.feishu.cn/base/{FEISHU_BITABLE_APP_TOKEN}?table={FEISHU_BITABLE_TABLE_ID}")
            else:
                print("❌ 测试失败，请检查配置。")
                print("\n📋 故障排查步骤:")
                print("1. 检查环境变量是否正确配置")
                print("2. 确认飞书应用已发布并授权")
                print("3. 验证多维表格字段配置")
                print("4. 查看参考文档: feynman/references/table-setup-guide-pro.md")

        elif sys.argv[1] == "--parse" and len(sys.argv) > 2:
            # 解析 Markdown 文件
            file_path = sys.argv[2]
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                data = parse_feynman_markdown(content)
                print(f"✅ 已解析文件: {file_path}")
                print(json.dumps(data, indent=2, ensure_ascii=False))

                # 询问是否保存
                if input("\n是否保存到飞书？(y/n): ").lower() == 'y':
                    save_feynman_note_pro(**data)

            except FileNotFoundError:
                print(f"❌ 文件不存在: {file_path}")
            except Exception as e:
                print(f"❌ 解析失败: {e}")

        else:
            print("用法:")
            print("  python feishu_bitable_pro.py --test                    # 运行测试")
            print("  python feishu_bitable_pro.py --parse <文件路径>         # 解析并保存 Markdown 文件")
    else:
        print("🎓 Feynman 学习笔记 - 飞书多维表格集成（专业版）")
        print("\n用法:")
        print("  python feishu_bitable_pro.py --test                    # 运行测试")
        print("  python feishu_bitable_pro.py --parse <文件路径>         # 解析并保存 Markdown 文件")
        print("\n功能特性:")
        print("  ✅ 自动分类标签")
        print("  ✅ AI 关键词提取")
        print("  ✅ 复习提醒计算")
        print("  ✅ 掌握程度评分")
        print("  ✅ 学习时长统计")
        print("  ✅ 完整数据追踪")
        print("\n配置文档:")
        print("  📖 feynman/references/table-setup-guide-pro.md")
        print("  📖 feynman/references/feishu-setup-guide.md")
