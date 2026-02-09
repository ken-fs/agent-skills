#!/usr/bin/env python3
"""
公众号格式优化脚本
将Markdown转换为公众号编辑器友好的格式
"""

import sys
import re
from typing import List, Tuple


class WeChatFormatter:
    """公众号格式转换器"""

    def __init__(self):
        self.config = {
            'line_break': '\n\n',  # 段落间距
            'section_break': '\n\n---\n\n',  # 章节分隔
            'golden_sentence_marker': '✨',  # 金句标记
            'image_placeholder': '[图片]',  # 图片占位符
        }

    def format_title(self, text: str, level: int = 1) -> str:
        """
        格式化标题

        公众号标题建议：
        - H1: 文章主标题（一般不用，由公众号标题承担）
        - H2: 主要章节（## 标题）
        - H3: 次级章节（### 标题）
        """
        if level == 1:
            # H1 作为文章标题，居中加粗
            return f"\n\n## {text}\n\n"
        elif level == 2:
            # H2 主章节，加粗
            return f"\n\n## {text}\n\n"
        elif level == 3:
            # H3 次级章节
            return f"\n\n### {text}\n\n"
        else:
            return f"\n\n{'#' * level} {text}\n\n"

    def format_golden_sentence(self, text: str) -> str:
        """格式化金句（高亮显示）"""
        # 公众号中金句可以用引用块或特殊符号
        return f"\n\n> {self.config['golden_sentence_marker']} {text}\n\n"

    def format_code_block(self, code: str, language: str = '') -> str:
        """格式化代码块"""
        # 公众号对代码块的支持有限，使用引用块
        return f"\n\n```{language}\n{code}\n```\n\n"

    def format_quote(self, text: str) -> str:
        """格式化引用"""
        return f"\n\n> {text}\n\n"

    def format_list(self, items: List[str], ordered: bool = False) -> str:
        """格式化列表"""
        if ordered:
            return '\n'.join(f"{i+1}. {item}" for i, item in enumerate(items))
        else:
            return '\n'.join(f"- {item}" for item in items)

    def format_image(self, alt_text: str = '', url: str = '') -> str:
        """格式化图片"""
        if url:
            return f"\n\n![]({url})\n\n"
        else:
            return f"\n\n{self.config['image_placeholder']}\n\n"

    def clean_ai_patterns(self, text: str) -> str:
        """
        清理AI写作模式

        移除：
        - 过度的"首先、其次、最后"
        - "值得注意的是"、"需要指出的是"
        - 多余的感叹号
        """
        # 替换常见AI模式
        patterns = [
            (r'首先，', ''),
            (r'其次，', ''),
            (r'最后，', ''),
            (r'值得注意的是，', ''),
            (r'需要指出的是，', ''),
            (r'总而言之，', ''),
            (r'综上所述，', ''),
            (r'!!+', '!'),  # 多个感叹号替换为一个
        ]

        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text)

        return text

    def optimize_paragraph_spacing(self, text: str) -> str:
        """优化段落间距"""
        # 移除多余的空行（超过2个连续换行）
        text = re.sub(r'\n{3,}', '\n\n', text)

        # 确保段落间有足够间距
        text = re.sub(r'([。！？])\n([^\n])', r'\1\n\n\2', text)

        return text

    def convert_markdown_to_wechat(self, markdown: str) -> str:
        """
        将Markdown转换为公众号格式

        处理：
        - 标题层级
        - 代码块
        - 引用块
        - 列表
        - 图片
        - 金句（标记为特殊引用）
        """
        lines = markdown.split('\n')
        output = []
        in_code_block = False
        code_buffer = []
        code_lang = ''

        for line in lines:
            # 处理代码块
            if line.startswith('```'):
                if in_code_block:
                    # 结束代码块
                    output.append(self.format_code_block('\n'.join(code_buffer), code_lang))
                    code_buffer = []
                    in_code_block = False
                else:
                    # 开始代码块
                    code_lang = line[3:].strip()
                    in_code_block = True
                continue

            if in_code_block:
                code_buffer.append(line)
                continue

            # 处理标题
            title_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if title_match:
                level = len(title_match.group(1))
                title_text = title_match.group(2)
                output.append(self.format_title(title_text, level))
                continue

            # 处理金句（以✨或💎等标记的引用）
            if line.startswith('> ✨') or line.startswith('> 💎'):
                golden_text = line[4:].strip()
                output.append(self.format_golden_sentence(golden_text))
                continue

            # 处理普通引用
            if line.startswith('> '):
                quote_text = line[2:].strip()
                output.append(self.format_quote(quote_text))
                continue

            # 处理图片
            image_match = re.match(r'!\[([^\]]*)\]\(([^\)]+)\)', line)
            if image_match:
                alt_text = image_match.group(1)
                url = image_match.group(2)
                output.append(self.format_image(alt_text, url))
                continue

            # 处理普通文本
            if line.strip():
                output.append(line)
            else:
                output.append('')

        result = '\n'.join(output)

        # 清理AI模式
        result = self.clean_ai_patterns(result)

        # 优化段落间距
        result = self.optimize_paragraph_spacing(result)

        return result

    def add_section_breaks(self, text: str) -> str:
        """在主要章节间添加分隔符"""
        # 在## 标题前添加分隔线
        text = re.sub(r'\n\n(## [^\n]+)', r'\n\n---\n\n\1', text)
        return text

    def format_full_article(self, markdown: str, add_breaks: bool = True) -> str:
        """格式化完整文章"""
        result = self.convert_markdown_to_wechat(markdown)

        if add_breaks:
            result = self.add_section_breaks(result)

        return result


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("""
Usage:
  Convert Markdown file:
    python wechat_formatter.py input.md [output.md]

  Convert from stdin:
    cat input.md | python wechat_formatter.py --stdin
""")
        sys.exit(1)

    formatter = WeChatFormatter()

    if sys.argv[1] == '--stdin':
        # 从标准输入读取
        markdown = sys.stdin.read()
        result = formatter.format_full_article(markdown)
        print(result)

    else:
        # 从文件读取
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None

        with open(input_file, 'r', encoding='utf-8') as f:
            markdown = f.read()

        result = formatter.format_full_article(markdown)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✓ Converted to WeChat format: {output_file}")
        else:
            print(result)


if __name__ == '__main__':
    main()
