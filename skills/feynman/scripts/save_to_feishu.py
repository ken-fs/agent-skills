#!/usr/bin/env python3
"""
飞书多维表格集成脚本 - 简化版
用于将文章保存到飞书多维表格（标题、内容、创建时间）
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
            print(f"❌ 获取 token 失败: {data.get('msg')}")
            return None
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None


def save_article_to_feishu(title: str, content: str) -> bool:
    """
    保存文章到飞书多维表格

    Args:
        title: 文章标题
        content: 文章内容

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

    # 构建 API URL
    url = f"{BASE_URL}/bitable/v1/apps/{FEISHU_BITABLE_APP_TOKEN}/tables/{FEISHU_BITABLE_TABLE_ID}/records"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 构建记录数据
    # 注意: 字段名必须与飞书多维表格中的字段名完全一致
    fields = {
        "标题": title,
        "内容": content,
        "创建时间": int(datetime.now().timestamp() * 1000)  # 飞书日期字段需要毫秒时间戳
    }

    payload = {"fields": fields}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        data = resp.json()

        if data.get("code") == 0:
            record_id = data.get("data", {}).get("record", {}).get("record_id")
            print(f"✅ 文章已保存到飞书多维表格")
            print(f"   标题: {title[:50]}{'...' if len(title) > 50 else ''}")
            print(f"   记录ID: {record_id}")
            return True
        else:
            print(f"❌ 保存失败: {data.get('msg')}")
            print(f"   错误代码: {data.get('code')}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False


def save_from_file(file_path: str) -> bool:
    """
    从文件读取文章并保存到飞书

    Args:
        file_path: 文章文件路径（支持 .md, .txt, .json）

    Returns:
        bool: 是否保存成功
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 如果是 JSON 格式，尝试解析
        if file_path.endswith('.json'):
            data = json.loads(content)
            title = data.get('title', '未命名文章')
            content = data.get('content', content)
        else:
            # 尝试从 Markdown 或文本中提取标题
            lines = content.strip().split('\n')
            if lines and lines[0].startswith('#'):
                title = lines[0].lstrip('#').strip()
                content = '\n'.join(lines[1:]).strip()
            else:
                # 使用文件名作为标题
                import os.path
                title = os.path.splitext(os.path.basename(file_path))[0]

        return save_article_to_feishu(title, content)

    except FileNotFoundError:
        print(f"❌ 文件不存在: {file_path}")
        return False
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False


if __name__ == "__main__":
    import sys

    # 命令行使用示例
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            # 测试模式
            test_title = "测试文章 - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            test_content = """这是一篇测试文章。

## 测试内容

这是用来测试飞书多维表格集成的示例文章。

### 功能特点
- 自动保存标题
- 自动保存内容
- 自动记录创建时间
"""
            if save_article_to_feishu(test_title, test_content):
                print("\n✅ 测试成功！")
            else:
                print("\n❌ 测试失败，请检查配置")

        elif sys.argv[1] == "--file":
            # 从文件读取
            if len(sys.argv) > 2:
                file_path = sys.argv[2]
                save_from_file(file_path)
            else:
                print("用法: python save_to_feishu.py --file <文件路径>")

        else:
            print("用法:")
            print("  python save_to_feishu.py --test              # 运行测试")
            print("  python save_to_feishu.py --file <文件路径>   # 从文件保存")
    else:
        print("用法:")
        print("  python save_to_feishu.py --test              # 运行测试")
        print("  python save_to_feishu.py --file <文件路径>   # 从文件保存")
