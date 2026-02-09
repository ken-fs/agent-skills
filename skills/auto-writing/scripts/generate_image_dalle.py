#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 OpenAI DALL-E 生成图片
"""

import openai
import sys
import os
from pathlib import Path

# 修复 Windows 控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 配置 OpenAI API
openai.api_key = "sk-f87144caa7294042a1e4968370cab90b"
# 如果使用代理
# openai.api_base = "http://127.0.0.1:8045/v1"


def generate_image(prompt: str, output_path: str) -> dict:
    """使用 DALL-E 生成图片"""
    try:
        # 创建输出目录
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # 优化提示词
        optimized_prompt = f"""
        Create a professional illustration for a tech blog: {prompt}
        Style: Pure hand-drawn line art, minimalist
        Lines: Single-color thin lines (dark brown #3D3D3D or black #1A1A1A), organic hand-drawn texture
        Background: Uniform beige #F5F0E6
        Fill: No fill or very subtle same-color wash
        Quality: High resolution, publication-ready
        FORBIDDEN: Gradients, shadows, 3D effects, complex textures, multiple colors
        Optional: Minimal handwritten English labels (max 3 words)
        """

        # 调用 DALL-E 3
        response = openai.Image.create(
            prompt=optimized_prompt,
            n=1,
            size="1024x1024",
            model="dall-e-3"
        )

        # 保存图片
        image_url = response['data'][0]['url']

        # 下载图片
        import requests
        img_data = requests.get(image_url).content

        with open(output_path, 'wb') as f:
            f.write(img_data)

        return {
            "success": True,
            "path": output_path,
            "url": image_url
        }

    except Exception as e:
        return {
            "success": False,
            "path": None,
            "error": str(e)
        }


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_image_dalle.py 'prompt' output.png")
        sys.exit(1)

    prompt = sys.argv[1]
    output_path = sys.argv[2]

    print(f"Generating image with DALL-E...")
    print(f"Prompt: {prompt}")

    result = generate_image(prompt, output_path)

    if result['success']:
        print(f"✓ Success: {result['path']}")
    else:
        print(f"✗ Failed: {result['error']}")


if __name__ == '__main__':
    main()
