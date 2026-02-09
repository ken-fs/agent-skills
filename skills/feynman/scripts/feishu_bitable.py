#!/usr/bin/env python3
"""
飞书多维表格集成脚本
用于将 Feynman 学习笔记自动记录到飞书多维表格
"""

import os
import json
import requests
from datetime import datetime
from typing import Optional, Dict, Any

# 从环境变量读取配置
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_BITABLE_APP_TOKEN = os.getenv("FEISHU_BITABLE_APP_TOKEN", "")
FEISHU_BITABLE_TABLE_ID = os.getenv("FEISHU_BITABLE_TABLE_ID", "")

BASE_URL = "https://open.feishu.cn/open-apis"


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
            print(f"获取 token 失败: {data.get('msg')}")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None


def add_record_to_bitable(
    concept: str,
    simple_explanation: str,
    analogy: str,
    gaps: str,
    refined_explanation: str,
    key_takeaways: str,
    test_question: str,
    remaining_questions: str = ""
) -> bool:
    """
    添加记录到飞书多维表格

    多维表格需要包含以下字段：
    - 概念 (文本)
    - 简单解释 (文本)
    - 类比 (文本)
    - 知识空白 (文本)
    - 精炼解释 (文本)
    - 核心要点 (文本)
    - 测试问题 (文本)
    - 待深入问题 (文本)
    - 学习日期 (日期)
    """
    token = get_tenant_access_token()
    if not token:
        return False

    url = f"{BASE_URL}/bitable/v1/apps/{FEISHU_BITABLE_APP_TOKEN}/tables/{FEISHU_BITABLE_TABLE_ID}/records"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 构建记录数据
    fields = {
        "概念": concept,
        "简单解释": simple_explanation,
        "类比": analogy,
        "知识空白": gaps,
        "精炼解释": refined_explanation,
        "核心要点": key_takeaways,
        "测试问题": test_question,
        "待深入问题": remaining_questions,
        "学习日期": int(datetime.now().timestamp() * 1000)  # 飞书日期字段需要毫秒时间戳
    }

    payload = {"fields": fields}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        data = resp.json()
        if data.get("code") == 0:
            record_id = data.get("data", {}).get("record", {}).get("record_id")
            print(f"✅ 记录已保存到飞书多维表格，记录ID: {record_id}")
            return True
        else:
            print(f"❌ 保存失败: {data.get('msg')}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False


def save_feynman_note(note_data: Dict[str, Any]) -> bool:
    """
    保存 Feynman 笔记到飞书

    note_data 结构:
    {
        "concept": "概念名称",
        "simple_explanation": "简单解释",
        "analogy": "类比",
        "gaps": "发现的知识空白",
        "refined_explanation": "精炼后的解释",
        "key_takeaways": "核心要点",
        "test_question": "30秒测试问题",
        "remaining_questions": "待深入的问题"
    }
    """
    return add_record_to_bitable(
        concept=note_data.get("concept", ""),
        simple_explanation=note_data.get("simple_explanation", ""),
        analogy=note_data.get("analogy", ""),
        gaps=note_data.get("gaps", ""),
        refined_explanation=note_data.get("refined_explanation", ""),
        key_takeaways=note_data.get("key_takeaways", ""),
        test_question=note_data.get("test_question", ""),
        remaining_questions=note_data.get("remaining_questions", "")
    )


if __name__ == "__main__":
    # 测试示例
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_data = {
            "concept": "测试概念",
            "simple_explanation": "这是一个简单的解释",
            "analogy": "就像...",
            "gaps": "1. 不清楚的地方",
            "refined_explanation": "精炼后的解释",
            "key_takeaways": "1. 要点1\n2. 要点2",
            "test_question": "30秒版本",
            "remaining_questions": "需要深入研究的问题"
        }

        if save_feynman_note(test_data):
            print("测试成功！")
        else:
            print("测试失败，请检查配置")
