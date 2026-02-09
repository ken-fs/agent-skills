#!/usr/bin/env python3
"""
多源信息调研整合脚本
用于从多个平台收集和整合信息
"""

import json
import sys
from typing import List, Dict
from datetime import datetime


class ResearchAggregator:
    """调研信息聚合器"""

    def __init__(self, topic: str):
        self.topic = topic
        self.sources = {
            'web': [],
            'x': [],
            'reddit': [],
            'wechat': [],
            'xiaohongshu': []
        }
        self.insights = []
        self.cases = []
        self.pitfalls = []
        self.quotes = []

    def add_web_source(self, title: str, url: str, summary: str, key_points: List[str]):
        """添加Web搜索结果"""
        self.sources['web'].append({
            'title': title,
            'url': url,
            'summary': summary,
            'key_points': key_points,
            'timestamp': datetime.now().isoformat()
        })

    def add_x_source(self, author: str, content: str, url: str, engagement: dict):
        """添加X平台内容"""
        self.sources['x'].append({
            'author': author,
            'content': content,
            'url': url,
            'engagement': engagement,
            'timestamp': datetime.now().isoformat()
        })

    def add_reddit_source(self, subreddit: str, title: str, content: str, url: str, upvotes: int):
        """添加Reddit讨论"""
        self.sources['reddit'].append({
            'subreddit': subreddit,
            'title': title,
            'content': content,
            'url': url,
            'upvotes': upvotes,
            'timestamp': datetime.now().isoformat()
        })

    def add_wechat_source(self, account: str, title: str, summary: str, url: str):
        """添加公众号文章"""
        self.sources['wechat'].append({
            'account': account,
            'title': title,
            'summary': summary,
            'url': url,
            'timestamp': datetime.now().isoformat()
        })

    def add_xiaohongshu_source(self, author: str, content: str, tags: List[str], likes: int):
        """添加小红书内容"""
        self.sources['xiaohongshu'].append({
            'author': author,
            'content': content,
            'tags': tags,
            'likes': likes,
            'timestamp': datetime.now().isoformat()
        })

    def add_insight(self, insight: str, source_type: str):
        """添加关键洞察"""
        self.insights.append({
            'content': insight,
            'source': source_type,
            'timestamp': datetime.now().isoformat()
        })

    def add_case(self, title: str, description: str, source: str):
        """添加真实案例"""
        self.cases.append({
            'title': title,
            'description': description,
            'source': source,
            'timestamp': datetime.now().isoformat()
        })

    def add_pitfall(self, pitfall: str, solution: str = None):
        """添加常见误区"""
        self.pitfalls.append({
            'pitfall': pitfall,
            'solution': solution,
            'timestamp': datetime.now().isoformat()
        })

    def add_quote(self, quote: str, author: str, source: str):
        """添加金句/观点"""
        self.quotes.append({
            'quote': quote,
            'author': author,
            'source': source,
            'timestamp': datetime.now().isoformat()
        })

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            'total_sources': sum(len(sources) for sources in self.sources.values()),
            'by_platform': {
                platform: len(sources)
                for platform, sources in self.sources.items()
            },
            'insights_count': len(self.insights),
            'cases_count': len(self.cases),
            'pitfalls_count': len(self.pitfalls),
            'quotes_count': len(self.quotes)
        }

    def generate_report(self) -> str:
        """生成调研报告"""
        stats = self.get_statistics()

        report = f"""# 调研报告：{self.topic}

## 📊 数据统计
- 总信息源：{stats['total_sources']}条
  - Web搜索：{stats['by_platform']['web']}条
  - X平台：{stats['by_platform']['x']}条
  - Reddit：{stats['by_platform']['reddit']}条
  - 公众号：{stats['by_platform']['wechat']}条
  - 小红书：{stats['by_platform']['xiaohongshu']}条
- 关键洞察：{stats['insights_count']}个
- 真实案例：{stats['cases_count']}个
- 常见误区：{stats['pitfalls_count']}个
- 有价值观点：{stats['quotes_count']}条

## 💡 核心洞察
"""
        for idx, insight in enumerate(self.insights, 1):
            report += f"{idx}. {insight['content']} (来源：{insight['source']})\n"

        report += "\n## 📝 真实案例\n"
        for idx, case in enumerate(self.cases, 1):
            report += f"{idx}. **{case['title']}**\n   {case['description']}\n   来源：{case['source']}\n\n"

        report += "## ⚠️ 常见误区\n"
        for idx, pitfall in enumerate(self.pitfalls, 1):
            report += f"{idx}. {pitfall['pitfall']}\n"
            if pitfall['solution']:
                report += f"   解决方案：{pitfall['solution']}\n"
            report += "\n"

        report += "## 💬 有价值的观点\n"
        for idx, quote in enumerate(self.quotes, 1):
            report += f"{idx}. \"{quote['quote']}\"\n   — {quote['author']} ({quote['source']})\n\n"

        return report

    def export_json(self, filepath: str):
        """导出为JSON"""
        data = {
            'topic': self.topic,
            'sources': self.sources,
            'insights': self.insights,
            'cases': self.cases,
            'pitfalls': self.pitfalls,
            'quotes': self.quotes,
            'statistics': self.get_statistics(),
            'generated_at': datetime.now().isoformat()
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_json(cls, filepath: str):
        """从JSON加载"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        aggregator = cls(data['topic'])
        aggregator.sources = data['sources']
        aggregator.insights = data['insights']
        aggregator.cases = data['cases']
        aggregator.pitfalls = data['pitfalls']
        aggregator.quotes = data['quotes']

        return aggregator


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("""
Usage:
  Create new research:
    python multi_source_research.py "topic name"

  Load and view report:
    python multi_source_research.py --load research.json

  Export report:
    python multi_source_research.py --load research.json --export report.md
""")
        sys.exit(1)

    if sys.argv[1] == '--load':
        if len(sys.argv) < 3:
            print("Error: --load requires filepath")
            sys.exit(1)

        aggregator = ResearchAggregator.load_from_json(sys.argv[2])

        if '--export' in sys.argv:
            export_idx = sys.argv.index('--export')
            if len(sys.argv) > export_idx + 1:
                output_path = sys.argv[export_idx + 1]
                report = aggregator.generate_report()
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"✓ Report exported to {output_path}")
            else:
                print("Error: --export requires output path")
        else:
            print(aggregator.generate_report())

    else:
        topic = sys.argv[1]
        aggregator = ResearchAggregator(topic)

        # 示例：添加一些数据
        print(f"Created research aggregator for: {topic}")
        print("Use the ResearchAggregator API to add sources programmatically.")
        print(f"\nExample:")
        print(f"  aggregator = ResearchAggregator('{topic}')")
        print(f"  aggregator.add_web_source(...)")
        print(f"  aggregator.export_json('research.json')")


if __name__ == '__main__':
    main()
