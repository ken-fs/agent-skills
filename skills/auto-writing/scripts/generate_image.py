#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini API 图片生成脚本
用于自动生成文章配图
"""

import google.generativeai as genai
import sys
import json
import os
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def setup_gemini_api():
    """配置Gemini API"""
    genai.configure(
        api_key="sk-f87144caa7294042a1e4968370cab90b",
        transport='rest',
        client_options={'api_endpoint': 'http://127.0.0.1:8045'}
    )
    # 使用 Gemini 3 Pro Image 模型
    return genai.GenerativeModel('gemini-3-pro-image')


def generate_image(prompt: str, output_path: str) -> dict:
    """
    使用 Gemini 3 Pro Image 生成图片

    Args:
        prompt: 图片生成提示词
        output_path: 输出文件路径

    Returns:
        {"success": bool, "path": str, "error": str, "prompt": str}
    """
    # 自动检测输出格式并修正扩展名
    output_path = str(Path(output_path))
    if not output_path.endswith(('.jpg', '.jpeg', '.png')):
        # 默认使用 .jpg (Gemini 3 Pro Image 通常返回 JPEG)
        output_path = Path(output_path).with_suffix('.jpg')
    try:
        model = setup_gemini_api()

        # 为配图优化提示词
        optimized_prompt = f"""Create a clean, hand-drawn line art illustration for a tech blog article.

Image description: {prompt}

Style requirements (STRICT):
- Pure hand-drawn line art style, minimalist design
- Single-color thin lines (dark brown #3D3D3D or black #1A1A1A)
- Organic, slightly shaky hand-drawn texture, NOT mechanical straight lines
- Uniform high-end beige background (#F5F0E6)
- No fill or very subtle same-color wash
- Optional: minimal handwritten-style English labels (max 3 words)
- Suitable for WeChat article (16:9 or 4:3 ratio)
- Professional quality, publication-ready

FORBIDDEN:
- Gradients
- Shadows
- 3D effects
- Complex textures
- Multiple colors
"""

        print(f"Sending prompt to Gemini 3 Pro Image...")
        print(f"Prompt: {optimized_prompt[:100]}...")

        # 调用 Gemini 3 Pro Image 生成
        response = model.generate_content(optimized_prompt)

        # 创建输出目录
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # 处理不同类型的响应
        if hasattr(response, 'parts') and len(response.parts) > 0:
            for part in response.parts:
                # 检查是否有图片数据 (inline_data)
                if hasattr(part, 'inline_data') and part.inline_data is not None:
                    import base64

                    # 获取MIME类型和数据
                    mime_type = getattr(part.inline_data, 'mime_type', 'image/jpeg')
                    data = part.inline_data.data

                    # 根据MIME类型确定扩展名
                    if 'jpeg' in mime_type or 'jpg' in mime_type:
                        ext = '.jpg'
                    elif 'png' in mime_type:
                        ext = '.png'
                    elif 'webp' in mime_type:
                        ext = '.webp'
                    else:
                        ext = '.jpg'  # 默认

                    # 更新输出路径的扩展名
                    output_path = str(Path(output_path).with_suffix(ext))

                    # 解码数据
                    if isinstance(data, str):
                        image_data = base64.b64decode(data)
                    else:
                        image_data = data

                    # 保存图片
                    with open(output_path, 'wb') as f:
                        f.write(image_data)

                    print(f"✓ Image saved: {output_path} ({len(image_data)} bytes, {mime_type})")

                    return {
                        "success": True,
                        "path": output_path,
                        "error": None,
                        "prompt": optimized_prompt,
                        "size": len(image_data),
                        "mime_type": mime_type
                    }

        # 如果响应是文本而不是图片
        if hasattr(response, 'text') and response.text:
            # 可能返回的是图片URL或base64数据
            text = response.text.strip()

            # 尝试解析为base64
            if text.startswith('data:image'):
                import base64
                header, data = text.split(',', 1)
                image_data = base64.b64decode(data)
                with open(output_path, 'wb') as f:
                    f.write(image_data)

                return {
                    "success": True,
                    "path": output_path,
                    "error": None,
                    "prompt": optimized_prompt
                }

            # 或者是纯base64
            if len(text) > 100 and not text.startswith('http'):
                try:
                    import base64
                    image_data = base64.b64decode(text)
                    # 验证是否是图片数据
                    if image_data[:4] == b'\x89PNG' or image_data[:2] == b'\xff\xd8':
                        with open(output_path, 'wb') as f:
                            f.write(image_data)
                        return {
                            "success": True,
                            "path": output_path,
                            "error": None,
                            "prompt": optimized_prompt
                        }
                except:
                    pass

        # 如果以上都不成功，返回响应信息
        return {
            "success": False,
            "path": None,
            "error": "Could not extract image from response",
            "prompt": optimized_prompt,
            "response": str(response) if hasattr(response, 'text') else str(response)
        }

    except Exception as e:
        return {
            "success": False,
            "path": None,
            "error": f"{type(e).__name__}: {str(e)}",
            "prompt": prompt if 'prompt' in locals() else None
        }


def batch_generate(prompts_file: str, output_dir: str) -> list:
    """
    批量生成图片

    Args:
        prompts_file: JSON文件路径，包含提示词列表
        output_dir: 输出目录

    Returns:
        生成结果列表
    """
    try:
        with open(prompts_file, 'r', encoding='utf-8') as f:
            prompts = json.load(f)

        results = []
        for idx, prompt_info in enumerate(prompts, 1):
            prompt = prompt_info.get('prompt', '')
            filename = prompt_info.get('filename', f'image_{idx}.png')
            output_path = os.path.join(output_dir, filename)

            print(f"Generating {idx}/{len(prompts)}: {filename}")
            result = generate_image(prompt, output_path)
            results.append({
                "index": idx,
                "filename": filename,
                **result
            })

            if result['success']:
                print(f"  ✓ Success: {output_path}")
            else:
                print(f"  ✗ Failed: {result['error']}")

        return results

    except Exception as e:
        print(f"Error in batch generation: {e}")
        return []


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("""
Usage:
  Single image:
    python generate_image.py "prompt text" output.png

  Batch generation:
    python generate_image.py --batch prompts.json output_dir/

prompts.json format:
[
    {"prompt": "description 1", "filename": "image1.png"},
    {"prompt": "description 2", "filename": "image2.png"}
]
""")
        sys.exit(1)

    if sys.argv[1] == '--batch':
        if len(sys.argv) < 4:
            print("Error: --batch requires prompts_file and output_dir")
            sys.exit(1)

        prompts_file = sys.argv[2]
        output_dir = sys.argv[3]
        results = batch_generate(prompts_file, output_dir)

        # 输出结果摘要
        print(f"\n=== Generation Summary ===")
        print(f"Total: {len(results)}")
        print(f"Success: {sum(1 for r in results if r['success'])}")
        print(f"Failed: {sum(1 for r in results if not r['success'])}")

    else:
        prompt = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else 'output.png'

        result = generate_image(prompt, output_path)

        if result['success']:
            print(f"✓ Image generated: {result['path']}")
        else:
            print(f"✗ Failed: {result['error']}")
            if 'optimized_prompt' in result:
                print(f"\nOptimized prompt for manual use:")
                print(result['optimized_prompt'])


if __name__ == '__main__':
    main()
