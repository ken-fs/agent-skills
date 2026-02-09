#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试所有支持的图片比例"""

import sys
from pathlib import Path

# 添加scripts目录到路径
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from generate_single_image import get_image_dimensions

def test_all_aspect_ratios():
    """测试所有支持的比例"""

    print("=" * 70)
    print("测试所有支持的图片比例")
    print("=" * 70)
    print()

    # 测试所有预定义比例
    test_cases = [
        ('1:1', '2K'),
        ('1:1', '4K'),
        ('4:3', '2K'),
        ('4:3', '4K'),
        ('2.35:1', '2K'),
        ('2.35:1', '4K'),
        ('16:9', '2K'),
        ('16:9', '4K'),
        ('9:16', '2K'),
        ('9:16', '4K'),
        ('3:4', '2K'),  # 向后兼容
        ('3:4', '4K'),  # 向后兼容
        # 自定义比例
        ('3:2', '2K'),
        ('21:9', '2K'),
        ('5:4', '2K'),
    ]

    print("预定义比例测试：")
    print("-" * 70)

    for aspect_ratio, resolution in test_cases[:12]:
        try:
            width, height = get_image_dimensions(aspect_ratio, resolution)
            status = "✓"
            print(f"{status} {aspect_ratio:8s} @ {resolution}: {width}x{height}")
        except Exception as e:
            print(f"✗ {aspect_ratio:8s} @ {resolution}: 错误 - {e}")

    print()
    print("自定义比例测试：")
    print("-" * 70)

    for aspect_ratio, resolution in test_cases[12:]:
        try:
            width, height = get_image_dimensions(aspect_ratio, resolution)
            status = "✓"
            print(f"{status} {aspect_ratio:8s} @ {resolution}: {width}x{height}")
        except Exception as e:
            print(f"✗ {aspect_ratio:8s} @ {resolution}: 错误 - {e}")

    print()
    print("=" * 70)
    print("✅ 所有比例测试完成！")
    print("=" * 70)

if __name__ == "__main__":
    test_all_aspect_ratios()
