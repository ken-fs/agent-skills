#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document Illustrator - 单图片生成工具
由 Claude 负责文档分析和内容归纳，此脚本只负责调用 Gemini API 生成图片
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# 设置 UTF-8 编码输出（Windows 兼容）
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def find_and_load_env():
    """
    智能查找并加载 .env 文件
    优先级：
    1. 当前脚本所在目录的上一级（Skill 根目录）
    2. 当前工作目录
    3. 用户主目录下的 .claude/skills/document-illustrator/
    """
    # 获取脚本所在目录的上一级（Skill 根目录）
    skill_root = Path(__file__).parent.parent
    env_path = skill_root / ".env"

    if env_path.exists():
        load_dotenv(env_path, override=True)
        return True

    # 尝试当前工作目录
    if Path(".env").exists():
        load_dotenv(".env", override=True)
        return True

    # 尝试 Claude Code Skill 标准位置
    claude_skill_env = Path.home() / ".claude" / "skills" / "document-illustrator" / ".env"
    if claude_skill_env.exists():
        load_dotenv(claude_skill_env, override=True)
        return True

    # 如果都没找到，尝试默认加载
    load_dotenv(override=True)
    return False


# 智能加载环境变量
find_and_load_env()


def get_image_dimensions(aspect_ratio, resolution):
    """
    根据比例和分辨率返回图片尺寸

    参数：
    - aspect_ratio: 图片比例（'1:1', '4:3', '2.35:1', '16:9', '9:16' 或自定义如 '3:2'）
    - resolution: '2K' 或 '4K'

    返回：(width, height)
    """
    # 预定义的比例和对应的分辨率
    dimensions = {
        "1:1": {
            "2K": (2048, 2048),
            "4K": (4096, 4096)
        },
        "4:3": {
            "2K": (2048, 1536),
            "4K": (4096, 3072)
        },
        "2.35:1": {
            "2K": (2560, 1089),
            "4K": (5120, 2179)
        },
        "16:9": {
            "2K": (2560, 1440),
            "4K": (3840, 2160)
        },
        "9:16": {
            "2K": (1440, 2560),
            "4K": (2160, 3840)
        },
        # 保持向后兼容
        "3:4": {
            "2K": (1920, 2560),
            "4K": (2880, 3840)
        }
    }

    # 如果是预定义的比例，直接返回
    if aspect_ratio in dimensions:
        if resolution not in dimensions[aspect_ratio]:
            # 如果分辨率不存在，使用 2K
            return dimensions[aspect_ratio]["2K"]
        return dimensions[aspect_ratio][resolution]

    # 如果是自定义比例（如 '3:2'），计算分辨率
    try:
        parts = aspect_ratio.split(':')
        if len(parts) == 2:
            width_ratio = float(parts[0])
            height_ratio = float(parts[1])

            # 基于2K或4K计算
            if resolution == '4K':
                base_pixels = 4096 * 2160  # 约 8.8M 像素
            else:
                base_pixels = 2560 * 1440  # 约 3.7M 像素

            # 保持比例，计算宽高
            ratio = width_ratio / height_ratio
            height = int((base_pixels / ratio) ** 0.5)
            width = int(height * ratio)

            return (width, height)
    except:
        pass

    # 默认返回 16:9 2K
    return (2560, 1440)


def generate_image(title, content, style_prompt, output_path, aspect_ratio="16:9", resolution="2K", is_cover=False):
    """
    调用 Gemini API 生成单张配图

    参数：
    - title: 图片标题
    - content: 图片内容文本
    - style_prompt: 风格提示词
    - output_path: 输出文件路径（包含文件名）
    - aspect_ratio: 图片比例（'1:1', '4:3', '2.35:1', '16:9', '9:16' 或自定义如 '3:2'）
    - resolution: 分辨率 '2K' 或 '4K'
    - is_cover: 是否为封面图

    返回：成功返回图片路径，失败返回 None
    """
    try:
        import google.generativeai as genai
    except ImportError:
        print("错误: 未安装 google-generativeai 库", file=sys.stderr)
        print("请运行: pip install google-generativeai", file=sys.stderr)
        sys.exit(1)

    # 获取 API 密钥
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("错误: 未设置 GEMINI_API_KEY 环境变量", file=sys.stderr)
        print("请在 .env 文件中设置: GEMINI_API_KEY=your-api-key", file=sys.stderr)
        sys.exit(1)

    # 获取自定义 API endpoint（可选）
    api_endpoint = os.environ.get("GEMINI_API_ENDPOINT")

    # 配置 API
    if api_endpoint:
        genai.configure(
            api_key=api_key,
            transport='rest',
            client_options={'api_endpoint': api_endpoint}
        )
    else:
        genai.configure(api_key=api_key)

    # 组合提示词 - 添加比例和分辨率要求
    dimensions = get_image_dimensions(aspect_ratio, resolution)
    size_instruction = f"\n\n图片规格:\n- 比例: {aspect_ratio}\n- 分辨率: {dimensions[0]}x{dimensions[1]}\n- 尺寸: {resolution}"

    if is_cover:
        # 封面图的提示词，强调概括性和引导性
        full_prompt = f"""{style_prompt}

这是一张封面图，需要概括整个文档的核心信息。

标题：{title}

核心内容（需要在一张图中体现）：
{content}

要求：
- 封面图需要突出主题，具有引导性
- 信息要精炼但完整，能代表整个系列
- 视觉冲击力强，吸引读者注意
{size_instruction}
"""
    else:
        # 普通内容配图
        full_prompt = f"""{style_prompt}

根据以下内容生成配图：

标题：{title}

内容：
{content}
{size_instruction}
"""

    try:
        # 使用 gemini-3-pro-image 模型
        model = genai.GenerativeModel('gemini-3-pro-image')
        response = model.generate_content(full_prompt)

        # 检查响应是否有效
        if response is None:
            print(f"错误: API 返回空响应", file=sys.stderr)
            return None

        if not hasattr(response, 'parts') or response.parts is None:
            print(f"错误: API 响应中没有 parts 属性", file=sys.stderr)
            return None

        # 保存图片
        for part in response.parts:
            if hasattr(part, 'inline_data') and part.inline_data is not None:
                # 确保输出目录存在
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)

                # 保存图片数据
                with open(output_path, 'wb') as f:
                    f.write(part.inline_data.data)

                return output_path

        print(f"警告: 图片生成失败 - 未收到图片数据", file=sys.stderr)
        return None

    except Exception as e:
        import traceback
        print(f"错误: 图片生成失败 - {e}", file=sys.stderr)
        print(f"详细错误信息:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return None


def main():
    """主流程"""
    parser = argparse.ArgumentParser(
        description='Document Illustrator - 单图片生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 生成普通内容配图（16:9）
  python generate_single_image.py \\
    --title "AI 工具演化" \\
    --content "从 Rules 到 Skills 的演化历程..." \\
    --style-file ../styles/ticket.md \\
    --output /path/to/output/image-01.png \\
    --ratio 16:9 \\
    --resolution 2K

  # 生成超宽电影比例封面图（2.35:1）
  python generate_single_image.py \\
    --title "Cowork 入门指南" \\
    --content "把AI助手请进你的文件夹..." \\
    --style-file ../styles/gradient-glass.md \\
    --output /path/to/output/cover.png \\
    --ratio 2.35:1 \\
    --resolution 2K \\
    --cover

  # 生成竖屏配图（9:16）
  python generate_single_image.py \\
    --title "小红书图文教程" \\
    --content "竖屏内容展示..." \\
    --style-file ../styles/vector-illustration.md \\
    --output /path/to/output/vertical.png \\
    --ratio 9:16 \\
    --resolution 2K

  # 使用自定义比例（3:2）
  python generate_single_image.py \\
    --title "自定义比例示例" \\
    --content "内容..." \\
    --style-file ../styles/gradient-glass.md \\
    --output /path/to/output/custom.png \\
    --ratio 3:2 \\
    --resolution 2K

环境变量:
  GEMINI_API_KEY: Google AI API 密钥（必需）
"""
    )

    parser.add_argument('--title', required=True, help='图片标题')
    parser.add_argument('--content', required=True, help='图片内容文本')
    parser.add_argument('--style-file', required=True, help='风格提示词文件路径')
    parser.add_argument('--output', required=True, help='输出文件路径（包含文件名）')
    parser.add_argument(
        '--ratio',
        default='16:9',
        help='图片比例（支持: 1:1, 4:3, 2.35:1, 16:9, 9:16, 3:4 或自定义如 3:2，默认: 16:9）'
    )
    parser.add_argument(
        '--resolution',
        choices=['2K', '4K'],
        default='2K',
        help='分辨率（默认: 2K）'
    )
    parser.add_argument(
        '--cover',
        action='store_true',
        help='标记为封面图（会使用不同的提示词策略）'
    )

    args = parser.parse_args()

    # 读取风格提示词
    style_file_path = Path(args.style_file)
    if not style_file_path.exists():
        print(f"错误: 风格文件不存在: {args.style_file}", file=sys.stderr)
        sys.exit(1)

    with open(style_file_path, 'r', encoding='utf-8') as f:
        style_prompt = f.read()

    # 显示生成信息
    image_type = "封面图" if args.cover else "内容配图"
    print(f"正在生成{image_type}...")
    print(f"  标题: {args.title}")
    print(f"  比例: {args.ratio}")
    print(f"  分辨率: {args.resolution}")

    width, height = get_image_dimensions(args.ratio, args.resolution)
    print(f"  尺寸: {width}x{height}")

    # 生成图片
    result_path = generate_image(
        title=args.title,
        content=args.content,
        style_prompt=style_prompt,
        output_path=args.output,
        aspect_ratio=args.ratio,
        resolution=args.resolution,
        is_cover=args.cover
    )

    if result_path:
        print(f"✓ 已保存: {result_path}")
        sys.exit(0)
    else:
        print(f"✗ 生成失败", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
