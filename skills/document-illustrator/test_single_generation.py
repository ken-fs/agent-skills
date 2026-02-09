#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 generate_single_image.py 脚本
生成一张简单的测试图片
"""

import subprocess
import sys
from pathlib import Path

# 脚本路径
skill_root = Path(__file__).parent
script_path = skill_root / "scripts" / "generate_single_image.py"
style_file = skill_root / "styles" / "gradient-glass.md"
output_path = skill_root / "test_single_output.png"

# 测试参数
title = "AI 编程助手"
content = """
AI 编程助手正在改变软件开发的方式：
- Claude Code 提供智能代码生成
- Antigravity 代理保护隐私
- Document Illustrator 自动生成配图
"""

print("=" * 60)
print("测试 generate_single_image.py 脚本")
print("=" * 60)
print(f"\n标题: {title}")
print(f"风格: 渐变玻璃卡片")
print(f"比例: 16:9")
print(f"分辨率: 2K")
print(f"输出: {output_path}\n")

# 构建命令
cmd = [
    sys.executable,
    str(script_path),
    "--title", title,
    "--content", content,
    "--style-file", str(style_file),
    "--output", str(output_path),
    "--ratio", "16:9",
    "--resolution", "2K"
]

# 运行脚本
print("运行命令...")
print(f"{' '.join(cmd)}\n")

result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')

# 显示输出
if result.stdout:
    print(result.stdout)

if result.stderr:
    print("错误信息:", file=sys.stderr)
    print(result.stderr, file=sys.stderr)

# 检查结果
if result.returncode == 0:
    print("\n" + "=" * 60)
    print("✓ 测试成功！")
    print("=" * 60)
    print(f"\n图片已保存到: {output_path}")

    # 检查文件是否存在
    if output_path.exists():
        file_size = output_path.stat().st_size
        print(f"文件大小: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    else:
        print("警告: 输出文件不存在")
else:
    print("\n" + "=" * 60)
    print("✗ 测试失败")
    print("=" * 60)
    sys.exit(1)
