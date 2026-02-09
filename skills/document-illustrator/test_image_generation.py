#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Gemini 图片生成功能
验证 Antigravity 代理是否支持图片生成模型
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
else:
    print(f"[FAIL] 未找到 .env 文件\n")
    sys.exit(1)

# 获取配置
api_key = os.environ.get("GEMINI_API_KEY")
api_endpoint = os.environ.get("GEMINI_API_ENDPOINT")

if not api_key:
    print("[FAIL] GEMINI_API_KEY 未设置\n")
    sys.exit(1)

print(f"API Endpoint: {api_endpoint or 'Default Google API'}\n")

# 导入库
try:
    import google.generativeai as genai
    print("[OK] google.generativeai 库已导入\n")
except ImportError:
    print("[FAIL] google.generativeai 库未安装\n")
    sys.exit(1)

# 配置 API
if api_endpoint:
    genai.configure(
        api_key=api_key,
        transport='rest',
        client_options={'api_endpoint': api_endpoint}
    )
else:
    genai.configure(api_key=api_key)

print("[OK] API 已配置\n")

# 测试不同的模型
test_models = [
    'gemini-3-pro-image-preview',  # Skill 脚本中使用的模型
    'gemini-2.0-flash-exp',         # 通用模型
    'gemini-3-flash',               # 已知可用的模型
]

print("=" * 60)
print("测试模型列表")
print("=" * 60)

for model_name in test_models:
    print(f"\n测试模型: {model_name}")
    print("-" * 60)

    try:
        model = genai.GenerativeModel(model_name)

        # 尝试生成简单文本
        print("  [1/2] 测试文本生成...")
        response = model.generate_content("Hello")

        if response and response.text:
            print(f"  [OK] 文本生成成功: {response.text[:50]}...")
        else:
            print("  [WARN] 文本生成返回空响应")

        # 尝试生成图片（如果支持）
        print("  [2/2] 测试图片生成...")
        try:
            # 尝试使用图片生成提示词
            image_prompt = """
            Create a minimalist gradient card design with:
            - Dark background
            - Glass morphism effect
            - Text: "Hello World"
            """

            response = model.generate_content(image_prompt)

            if response:
                print(f"  [OK] 图片生成请求已发送")

                # 检查响应类型
                if hasattr(response, 'parts'):
                    for i, part in enumerate(response.parts):
                        if hasattr(part, 'inline_data') and part.inline_data:
                            print(f"  [OK] 找到图片数据 (part {i})")
                        elif hasattr(part, 'text') and part.text:
                            print(f"  [INFO] 找到文本数据 (part {i}): {part.text[:50]}...")
                else:
                    print(f"  [WARN] 响应无 parts 属性")
            else:
                print("  [WARN] 图片生成返回空响应")

        except Exception as img_error:
            print(f"  [FAIL] 图片生成失败: {img_error}")

        print(f"  [SUMMARY] 模型 {model_name} 基本可用")

    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            print(f"  [FAIL] 模型不存在: {model_name}")
        else:
            print(f"  [FAIL] 调用失败: {error_msg[:100]}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
print("\n建议:")
print("- 如果某个模型支持图片生成，会显示 '找到图片数据'")
print("- 如果只有文本响应，说明模型不支持图片生成或需要特殊参数")
print("- 如果模型不存在，可能需要使用其他模型名称")
