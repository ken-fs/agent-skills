#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 gemini-3-pro-image 模型的图片生成功能
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
    print(f"[OK] 已加载环境变量\n")

api_key = os.environ.get("GEMINI_API_KEY")
api_endpoint = os.environ.get("GEMINI_API_ENDPOINT")

print(f"API Key: {api_key[:20]}...")
print(f"API Endpoint: {api_endpoint}\n")

# 导入库
import google.generativeai as genai

# 配置 API（使用用户提供的方式）
genai.configure(
    api_key=api_key,
    transport='rest',
    client_options={'api_endpoint': api_endpoint}
)

print("[OK] API 已配置\n")

# 测试 gemini-3-pro-image 模型
print("=" * 60)
print("测试 gemini-3-pro-image 模型")
print("=" * 60)

try:
    model = genai.GenerativeModel('gemini-3-pro-image')

    # 测试图片生成
    print("\n[测试] 图片生成测试...")
    image_prompt = """
    Create a minimalist gradient card design with:
    - Dark background with deep purple to blue gradient
    - Glass morphism effect with semi-transparent layers
    - Large text: "Hello World"
    - Modern, clean aesthetic
    """

    print(f"提示词: {image_prompt[:80]}...")
    response = model.generate_content(image_prompt)
    print(f"[OK] API 请求成功")

    # 检查并保存图片
    print("\n[检查响应] 分析响应内容...")
    saved = False

    if hasattr(response, 'parts') and response.parts:
        print(f"响应包含 {len(response.parts)} 个部分:")
        for i, part in enumerate(response.parts):
            if hasattr(part, 'inline_data') and part.inline_data:
                print(f"\n  [Part {i}] 图片数据 ✓")
                print(f"    MIME类型: {part.inline_data.mime_type}")
                print(f"    数据大小: {len(part.inline_data.data)} bytes")

                # 保存图片
                output_path = skill_root / f"test_output.png"
                with open(output_path, 'wb') as f:
                    f.write(part.inline_data.data)

                print(f"    [OK] 已保存到: {output_path}")
                saved = True

            elif hasattr(part, 'text') and part.text:
                print(f"\n  [Part {i}] 文本数据")
                print(f"    内容: {part.text[:100]}...")
    else:
        print("[WARN] 响应没有 parts 属性或为空")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

    if saved:
        print("\n✓ gemini-3-pro-image 支持图片生成！")
        print("可以使用此模型更新 skill 脚本")
    else:
        print("\n✗ gemini-3-pro-image 不支持图片生成")
        print("或需要特殊参数配置")

except Exception as e:
    print(f"\n[FAIL] 测试失败: {e}")
    import traceback
    traceback.print_exc()
