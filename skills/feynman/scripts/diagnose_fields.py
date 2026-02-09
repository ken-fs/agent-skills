#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书表格字段诊断工具
"""

import os
import sys
import json
import requests

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

def get_tenant_access_token():
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

def get_table_fields():
    """获取表格所有字段"""
    token = get_tenant_access_token()
    if not token:
        return None

    url = f"{BASE_URL}/bitable/v1/apps/{FEISHU_BITABLE_APP_TOKEN}/tables/{FEISHU_BITABLE_TABLE_ID}/fields"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()

        if data.get("code") == 0:
            return data.get("data", {}).get("items", [])
        else:
            print(f"❌ 获取字段失败: {data.get('msg')}")
            return None
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

if __name__ == "__main__":
    print("🔍 飞书表格字段诊断工具\n")
    print("=" * 60)

    # 脚本期望的字段列表
    expected_fields = {
        "概念": "单行文本",
        "分类标签": "多选",
        "简单解释": "多行文本",
        "类比": "多行文本",
        "知识空白": "多行文本",
        "精炼解释": "多行文本",
        "核心要点": "多行文本",
        "测试问题": "多行文本",
        "掌握程度": "评分",
        "学习日期": "日期",
        "下次复习": "日期",
        "完成状态": "单选",
        "AI关键词": "多选",
        "学习时长": "数字",
        "待深入问题": "多行文本",
        "思维导图": "URL"
    }

    print("\n📋 脚本期望的字段列表：")
    for i, (name, field_type) in enumerate(expected_fields.items(), 1):
        print(f"  {i:2d}. {name:12s} ({field_type})")

    print("\n" + "=" * 60)
    print("\n🔄 正在获取表格实际字段...\n")

    fields = get_table_fields()

    if fields:
        print(f"✅ 成功获取到 {len(fields)} 个字段\n")
        print("=" * 60)
        print("\n📊 表格实际字段列表：\n")

        actual_field_names = {}
        field_type_mapping = {
            1: "单行文本",
            2: "多行文本",
            3: "单选",
            4: "多选",
            5: "日期",
            7: "数字",
            15: "URL",
            23: "评分"
        }

        for i, field in enumerate(fields, 1):
            field_name = field.get("field_name", "")
            field_type_code = field.get("type", 0)
            field_type = field_type_mapping.get(field_type_code, f"未知({field_type_code})")
            field_id = field.get("field_id", "")

            actual_field_names[field_name] = field_type
            print(f"  {i:2d}. {field_name:15s} ({field_type:10s}) [ID: {field_id}]")

        print("\n" + "=" * 60)
        print("\n🔍 对比分析：\n")

        missing_fields = []
        type_mismatch = []
        extra_fields = []
        matched_fields = []

        # 检查缺失的字段
        for expected_name, expected_type in expected_fields.items():
            if expected_name not in actual_field_names:
                missing_fields.append((expected_name, expected_type))
            elif actual_field_names[expected_name] != expected_type:
                type_mismatch.append((expected_name, expected_type, actual_field_names[expected_name]))
            else:
                matched_fields.append(expected_name)

        # 检查多余的字段
        for actual_name in actual_field_names:
            if actual_name not in expected_fields:
                extra_fields.append(actual_name)

        # 显示匹配的字段
        if matched_fields:
            print(f"✅ 匹配正确 ({len(matched_fields)} 个):")
            for name in matched_fields:
                print(f"   ✓ {name}")
            print()

        # 显示缺失的字段
        if missing_fields:
            print(f"❌ 缺失字段 ({len(missing_fields)} 个):")
            for name, field_type in missing_fields:
                print(f"   ✗ {name:15s} (需要类型: {field_type})")
            print()

        # 显示类型不匹配的字段
        if type_mismatch:
            print(f"⚠️  类型不匹配 ({len(type_mismatch)} 个):")
            for name, expected, actual in type_mismatch:
                print(f"   ! {name:15s} 期望: {expected:10s} 实际: {actual}")
            print()

        # 显示多余的字段
        if extra_fields:
            print(f"ℹ️  额外字段 ({len(extra_fields)} 个，可忽略):")
            for name in extra_fields:
                print(f"   + {name}")
            print()

        print("=" * 60)

        # 给出修复建议
        if missing_fields or type_mismatch:
            print("\n🔧 修复建议：\n")

            if missing_fields:
                print("需要添加以下字段：")
                for name, field_type in missing_fields:
                    print(f"  • 字段名：{name}")
                    print(f"    类型：{field_type}")
                    if name == "下次复习":
                        print(f"    配置：日期类型，可不勾选'包含时间'")
                    elif name == "学习时长":
                        print(f"    配置：数字类型，单位：分钟")
                    elif name == "待深入问题":
                        print(f"    配置：多行文本，建议开启富文本")
                    elif name == "思维导图":
                        print(f"    配置：URL 类型")
                    print()

            if type_mismatch:
                print("需要修改以下字段类型：")
                for name, expected, actual in type_mismatch:
                    print(f"  • 字段名：{name}")
                    print(f"    当前类型：{actual}")
                    print(f"    应改为：{expected}")
                    print()
        else:
            print("\n🎉 恭喜！所有字段配置正确，可以运行测试了！")
            print("\n运行命令：python feishu_bitable_pro.py --test")
    else:
        print("❌ 无法获取表格字段，请检查配置")

    print("\n" + "=" * 60)
