#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将HTML中的本地图片转换为Base64内嵌格式
这样可以实现"一键复制"，无需手动上传图片
"""

import os
import sys
import base64
import re
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def image_to_base64(image_path):
    """将图片转换为Base64编码"""
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')

            # 根据文件扩展名确定MIME类型
            ext = Path(image_path).suffix.lower()
            mime_types = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            mime_type = mime_types.get(ext, 'image/jpeg')

            return f"data:{mime_type};base64,{base64_data}"
    except Exception as e:
        print(f"[X] 转换图片失败: {image_path}")
        print(f"    错误: {str(e)}")
        return None


def embed_images_in_html(html_path, output_path=None):
    """
    将HTML中的本地图片引用替换为Base64内嵌

    Args:
        html_path: HTML文件路径
        output_path: 输出文件路径（如果为None，则覆盖原文件）
    """
    if output_path is None:
        output_path = html_path

    # 读取HTML内容
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"[X] 读取HTML失败: {html_path}")
        print(f"    错误: {str(e)}")
        return False

    # HTML文件所在目录
    html_dir = Path(html_path).parent

    # 查找所有图片引用（支持 src="..." 和 src='...'）
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'

    converted_count = 0
    skipped_count = 0

    def replace_image(match):
        nonlocal converted_count, skipped_count

        img_tag = match.group(0)
        img_src = match.group(1)

        # 跳过已经是Base64或HTTP(S)的图片
        if img_src.startswith('data:') or img_src.startswith('http://') or img_src.startswith('https://'):
            skipped_count += 1
            return img_tag

        # 构建图片完整路径
        if os.path.isabs(img_src):
            img_path = img_src
        else:
            img_path = html_dir / img_src

        # 检查文件是否存在
        if not os.path.exists(img_path):
            print(f"[!] 图片不存在: {img_src}")
            skipped_count += 1
            return img_tag

        # 转换为Base64
        base64_src = image_to_base64(img_path)
        if base64_src is None:
            skipped_count += 1
            return img_tag

        # 替换src属性
        new_img_tag = img_tag.replace(f'src="{img_src}"', f'src="{base64_src}"')
        new_img_tag = new_img_tag.replace(f"src='{img_src}'", f'src="{base64_src}"')

        converted_count += 1
        print(f"[OK] 已转换: {Path(img_src).name} ({len(base64_src)} bytes)")

        return new_img_tag

    # 替换所有图片
    new_html_content = re.sub(img_pattern, replace_image, html_content)

    # 保存结果
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_html_content)

        print(f"\n[SUCCESS] HTML处理完成！")
        print(f"    转换图片: {converted_count} 张")
        print(f"    跳过图片: {skipped_count} 张")
        print(f"    输出文件: {output_path}")

        # 显示文件大小
        file_size = os.path.getsize(output_path)
        size_mb = file_size / (1024 * 1024)
        print(f"    文件大小: {size_mb:.2f} MB")

        if size_mb > 5:
            print(f"\n[WARNING] 提示: 文件较大，某些平台可能有限制")

        return True

    except Exception as e:
        print(f"[X] 保存文件失败: {output_path}")
        print(f"    错误: {str(e)}")
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python embed_images_to_html.py <html文件路径> [输出路径]")
        print("\n示例:")
        print("  python embed_images_to_html.py article.html")
        print("  python embed_images_to_html.py article.html article_embedded.html")
        sys.exit(1)

    html_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(html_path):
        print(f"[X] 文件不存在: {html_path}")
        sys.exit(1)

    print(f"处理HTML文件: {html_path}\n")

    success = embed_images_in_html(html_path, output_path)

    sys.exit(0 if success else 1)
