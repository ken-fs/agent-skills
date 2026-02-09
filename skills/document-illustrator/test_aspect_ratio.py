#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图片比例计算功能
"""

import sys
from pathlib import Path

# 添加scripts目录到路径
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from generate_illustrations import calculate_resolution_dimensions

def test_aspect_ratios():
    """测试各种比例的分辨率计算"""

    print("=" * 60)
    print("图片比例计算测试")
    print("=" * 60)
    print()

    # 测试预定义比例
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
        # 测试自定义比例
        ('3:2', '2K'),
        ('3:2', '4K'),
        ('21:9', '2K'),
        ('5:4', '2K'),
    ]

    print("预定义比例测试：")
    print("-" * 60)
    for aspect_ratio, resolution in test_cases[:10]:
        result = calculate_resolution_dimensions(aspect_ratio, resolution)
        print(f"{aspect_ratio:8s} @ {resolution}: {result}")

    print()
    print("自定义比例测试：")
    print("-" * 60)
    for aspect_ratio, resolution in test_cases[10:]:
        result = calculate_resolution_dimensions(aspect_ratio, resolution)
        print(f"{aspect_ratio:8s} @ {resolution}: {result}")

    print()
    print("=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_aspect_ratios()
