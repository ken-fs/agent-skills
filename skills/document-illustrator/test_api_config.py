#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Gemini API 配置
验证 API 密钥和自定义 endpoint 是否正确配置
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 设置 UTF-8 编码输出
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 加载 .env 文件
skill_root = Path(__file__).parent
env_path = skill_root / ".env"

if env_path.exists():
    load_dotenv(env_path, override=True)
    print(f"✓ 已加载环境变量: {env_path}\n")
else:
    print(f"⚠️  未找到 .env 文件: {env_path}\n")

# 检查 API 密钥
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    print(f"✓ GEMINI_API_KEY 已设置")
    print(f"  密钥: {api_key[:20]}... (已隐藏)\n")
else:
    print("✗ GEMINI_API_KEY 未设置\n")
    sys.exit(1)

# 检查自定义 endpoint
api_endpoint = os.environ.get("GEMINI_API_ENDPOINT")
if api_endpoint:
    print(f"✓ GEMINI_API_ENDPOINT 已设置")
    print(f"  Endpoint: {api_endpoint}\n")
else:
    print("⚠️  GEMINI_API_ENDPOINT 未设置（将使用默认 Google API）\n")

# 尝试导入库
print("检查依赖库...")
try:
    from google import genai
    from google.genai import types
    print("✓ google-genai 库已安装\n")
except ImportError:
    print("✗ google-genai 库未安装")
    print("请运行: pip install google-genai\n")
    sys.exit(1)

# 测试 API 连接
print("测试 API 连接...")
try:
    # 创建客户端
    if api_endpoint:
        print(f"使用自定义 endpoint: {api_endpoint}")
        client = genai.Client(
            api_key=api_key,
            http_options={
                'api_version': 'v1alpha',
                'url': api_endpoint
            }
        )
    else:
        print("使用默认 Google API endpoint")
        client = genai.Client(api_key=api_key)

    print("✓ API 客户端创建成功\n")

    # 尝试生成简单内容
    print("测试内容生成...")
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents="Say 'Hello from Document Illustrator!'"
    )

    if response and hasattr(response, 'text'):
        print(f"✓ API 调用成功")
        print(f"  响应: {response.text}\n")
    else:
        print("⚠️  API 调用成功但响应格式异常\n")

    print("=" * 60)
    print("✨ 配置验证成功！")
    print("=" * 60)

except Exception as e:
    print(f"✗ API 调用失败: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)
