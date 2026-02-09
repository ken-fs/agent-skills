#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书集成简化测试 - 逐步调试
"""

import os
import sys
import json
import requests
from datetime import datetime

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

def get_token():
    """获取访问令牌"""
    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    payload = {"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    resp = requests.post(url, json=payload, timeout=10)
    data = resp.json()
    if data.get("code") == 0:
        return data.get("tenant_access_token")
    return None

def test_minimal():
    """最小化测试 - 只发送必需字段"""
    print("🧪 测试1: 最小化字段测试\n")

    token = get_token()
    if not token:
        print("❌ 获取token失败")
        return False

    url = f"{BASE_URL}/bitable/v1/apps/{FEISHU_BITABLE_APP_TOKEN}/tables/{FEISHU_BITABLE_TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 测试1: 只发送概念字段
    print("→ 尝试只发送 '概念' 字段...")
    fields = {
        "概念": "测试概念1"
    }
    payload = {"fields": fields}

    resp = requests.post(url, headers=headers, json=payload, timeout=15)
    data = resp.json()

    if data.get("code") == 0:
        print("✅ 成功！基础字段可以保存")
        record_id = data.get("data", {}).get("record", {}).get("record_id")
        print(f"   记录ID: {record_id}\n")
        return True
    else:
        print(f"❌ 失败: {data.get('msg')} (代码: {data.get('code')})")
        print(f"   详细: {json.dumps(data, ensure_ascii=False, indent=2)}\n")
        return False

def test_with_multiselect():
    """测试2: 添加多选字段"""
    print("🧪 测试2: 添加分类标签（多选）\n")

    token = get_token()
    if not token:
        return False

    url = f"{BASE_URL}/bitable/v1/apps/{FEISHU_BITABLE_APP_TOKEN}/tables/{FEISHU_BITABLE_TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("→ 发送 '概念' + '分类标签'...")
    fields = {
        "概念": "测试概念2",
        "分类标签": ["前端开发"]
    }
    payload = {"fields": fields}

    resp = requests.post(url, headers=headers, json=payload, timeout=15)
    data = resp.json()

    if data.get("code") == 0:
        print("✅ 成功！多选字段正常")
        record_id = data.get("data", {}).get("record", {}).get("record_id")
        print(f"   记录ID: {record_id}\n")
        return True
    else:
        print(f"❌ 失败: {data.get('msg')} (代码: {data.get('code')})")
        print(f"   详细: {json.dumps(data, ensure_ascii=False, indent=2)}\n")
        return False

def test_with_text_fields():
    """测试3: 添加文本字段"""
    print("🧪 测试3: 添加所有文本字段\n")

    token = get_token()
    if not token:
        return False

    url = f"{BASE_URL}/bitable/v1/apps/{FEISHU_BITABLE_APP_TOKEN}/tables/{FEISHU_BITABLE_TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("→ 发送所有文本字段...")
    fields = {
        "概念": "测试概念3",
        "分类标签": ["前端开发", "后端开发"],
        "简单解释": "这是简单解释",
        "类比": "这是类比",
        "知识空白": "这是知识空白",
        "精炼解释": "这是精炼解释",
        "核心要点": "这是核心要点",
        "测试问题": "这是测试问题",
        "掌握程度": "⭐⭐⭐",
        "AI关键词": "React, Hooks, useState"
    }
    payload = {"fields": fields}

    resp = requests.post(url, headers=headers, json=payload, timeout=15)
    data = resp.json()

    if data.get("code") == 0:
        print("✅ 成功！所有文本字段正常")
        record_id = data.get("data", {}).get("record", {}).get("record_id")
        print(f"   记录ID: {record_id}\n")
        return True
    else:
        print(f"❌ 失败: {data.get('msg')} (代码: {data.get('code')})")
        print(f"   详细: {json.dumps(data, ensure_ascii=False, indent=2)}\n")
        return False

def test_with_date():
    """测试4: 添加日期字段"""
    print("🧪 测试4: 添加日期字段\n")

    token = get_token()
    if not token:
        return False

    url = f"{BASE_URL}/bitable/v1/apps/{FEISHU_BITABLE_APP_TOKEN}/tables/{FEISHU_BITABLE_TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("→ 发送带日期字段...")
    learning_date = datetime.now()
    fields = {
        "概念": "测试概念4",
        "学习日期": int(learning_date.timestamp() * 1000)
    }
    payload = {"fields": fields}

    resp = requests.post(url, headers=headers, json=payload, timeout=15)
    data = resp.json()

    if data.get("code") == 0:
        print("✅ 成功！日期字段正常")
        record_id = data.get("data", {}).get("record", {}).get("record_id")
        print(f"   记录ID: {record_id}\n")
        return True
    else:
        print(f"❌ 失败: {data.get('msg')} (代码: {data.get('code')})")
        print(f"   详细: {json.dumps(data, ensure_ascii=False, indent=2)}\n")
        return False

def test_with_single_select():
    """测试5: 添加单选字段"""
    print("🧪 测试5: 添加完成状态（单选）\n")

    token = get_token()
    if not token:
        return False

    url = f"{BASE_URL}/bitable/v1/apps/{FEISHU_BITABLE_APP_TOKEN}/tables/{FEISHU_BITABLE_TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("→ 发送带单选字段...")
    fields = {
        "概念": "测试概念5",
        "完成状态": "🟢 已掌握"
    }
    payload = {"fields": fields}

    resp = requests.post(url, headers=headers, json=payload, timeout=15)
    data = resp.json()

    if data.get("code") == 0:
        print("✅ 成功！单选字段正常")
        record_id = data.get("data", {}).get("record", {}).get("record_id")
        print(f"   记录ID: {record_id}\n")
        return True
    else:
        print(f"❌ 失败: {data.get('msg')} (代码: {data.get('code')})")
        print(f"   详细: {json.dumps(data, ensure_ascii=False, indent=2)}\n")
        return False

def test_complete():
    """测试6: 完整测试"""
    print("🧪 测试6: 完整字段组合测试\n")

    token = get_token()
    if not token:
        return False

    url = f"{BASE_URL}/bitable/v1/apps/{FEISHU_BITABLE_APP_TOKEN}/tables/{FEISHU_BITABLE_TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("→ 发送完整数据...")
    learning_date = datetime.now()
    fields = {
        "概念": "React Hooks 完整测试",
        "分类标签": ["前端开发"],
        "简单解释": "React Hooks 是让函数组件使用状态的方法",
        "类比": "就像给自行车加装了变速器",
        "知识空白": "Hook 底层实现不清楚",
        "精炼解释": "React Hooks 是 React 16.8 引入的特性",
        "核心要点": "1. 让代码更简洁\n2. 遵循规则很重要",
        "测试问题": "React Hooks 让函数组件管理状态",
        "掌握程度": "⭐⭐⭐⭐",
        "学习日期": int(learning_date.timestamp() * 1000),
        "完成状态": "🟢 已掌握",
        "AI关键词": "React, Hooks, useState, useEffect",
        "思维导图": "https://example.com/mindmap"
    }
    payload = {"fields": fields}

    resp = requests.post(url, headers=headers, json=payload, timeout=15)
    data = resp.json()

    if data.get("code") == 0:
        print("✅ 成功！完整测试通过")
        record_id = data.get("data", {}).get("record", {}).get("record_id")
        print(f"   记录ID: {record_id}")
        print(f"   🔗 查看: https://my.feishu.cn/base/{FEISHU_BITABLE_APP_TOKEN}?table={FEISHU_BITABLE_TABLE_ID}&record={record_id}\n")
        return True
    else:
        print(f"❌ 失败: {data.get('msg')} (代码: {data.get('code')})")
        print(f"   详细: {json.dumps(data, ensure_ascii=False, indent=2)}\n")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  飞书集成逐步调试工具")
    print("=" * 60)
    print()

    tests = [
        ("基础字段", test_minimal),
        ("多选字段", test_with_multiselect),
        ("文本字段", test_with_text_fields),
        ("日期字段", test_with_date),
        ("单选字段", test_with_single_select),
        ("完整测试", test_complete)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            if not result:
                print(f"⚠️  '{name}' 测试失败，停止后续测试\n")
                break
        except Exception as e:
            print(f"❌ '{name}' 测试异常: {e}\n")
            results.append((name, False))
            break

    print("=" * 60)
    print("  测试结果汇总")
    print("=" * 60)
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name:12s} : {status}")

    all_passed = all(r for _, r in results)
    if all_passed:
        print("\n🎉 所有测试通过！飞书集成配置正确！")
    else:
        print("\n⚠️  部分测试失败，请根据上述错误信息调整配置")
