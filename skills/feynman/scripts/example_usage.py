#!/usr/bin/env python3
"""
飞书多维表格集成 - 使用示例
演示如何在不同场景下保存文章到飞书
"""

import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from save_to_feishu import save_article_to_feishu


def example_1_basic():
    """示例1: 基本用法 - 直接保存标题和内容"""
    print("\n=== 示例1: 基本用法 ===\n")

    title = "Python 装饰器学习笔记"
    content = """# Python 装饰器

## 核心概念
装饰器是Python中的一种设计模式，允许在不修改原函数代码的情况下，给函数添加新功能。

## 基本语法
```python
@decorator
def my_function():
    pass
```

## 实际应用
- 日志记录
- 性能测试
- 权限验证
- 缓存结果
"""

    result = save_article_to_feishu(title, content)
    print(f"保存结果: {'成功 ✓' if result else '失败 ✗'}\n")


def example_2_feynman_note():
    """示例2: Feynman 学习笔记格式"""
    print("\n=== 示例2: Feynman 学习笔记 ===\n")

    concept = "React Hooks"

    title = f"Feynman 学习笔记: {concept}"
    content = f"""# {concept}

## 简单解释
React Hooks 就像是给函数组件装上的"工具包"，让它们能做原本只有类组件才能做的事情。

## 类比
想象你原本只能用螺丝刀（函数组件），现在有了一个工具箱（Hooks），里面有扳手（useState）、电钻（useEffect）等各种工具，让你能完成更复杂的任务。

## 核心要点
1. useState - 让函数组件拥有状态
2. useEffect - 处理副作用（如数据获取、订阅）
3. 自定义 Hook - 复用状态逻辑

## 30秒版本
React Hooks 是 React 16.8 引入的新特性，让函数组件也能使用状态和生命周期功能，使代码更简洁、可复用性更强。
"""

    result = save_article_to_feishu(title, content)
    print(f"保存结果: {'成功 ✓' if result else '失败 ✗'}\n")


def example_3_markdown_article():
    """示例3: 完整的 Markdown 文章"""
    print("\n=== 示例3: Markdown 文章 ===\n")

    title = "JavaScript 异步编程最佳实践"
    content = """# JavaScript 异步编程最佳实践

## 前言
异步编程是 JavaScript 中最重要的概念之一，掌握它对于编写高性能的应用至关重要。

## 1. 从回调到 Promise

### 回调地狱问题
```javascript
getData(function(a) {
    getMoreData(a, function(b) {
        getMoreData(b, function(c) {
            // 回调地狱...
        });
    });
});
```

### Promise 解决方案
```javascript
getData()
    .then(a => getMoreData(a))
    .then(b => getMoreData(b))
    .then(c => {
        // 清晰的链式调用
    });
```

## 2. Async/Await 语法糖

使用 async/await 可以让异步代码看起来像同步代码：

```javascript
async function fetchData() {
    try {
        const a = await getData();
        const b = await getMoreData(a);
        const c = await getMoreData(b);
        return c;
    } catch (error) {
        console.error('Error:', error);
    }
}
```

## 3. 最佳实践

### 3.1 错误处理
- 始终使用 try/catch 或 .catch()
- 提供有意义的错误信息
- 考虑错误恢复策略

### 3.2 并发控制
```javascript
// 并行执行
const [result1, result2] = await Promise.all([
    fetchData1(),
    fetchData2()
]);

// 竞态执行
const fastest = await Promise.race([
    fetchFromServer1(),
    fetchFromServer2()
]);
```

### 3.3 避免常见陷阱
- 不要忘记 await 关键字
- 注意 forEach 中的 async 函数
- 合理使用 Promise.all vs 顺序执行

## 总结

掌握异步编程需要：
1. 理解 Event Loop 机制
2. 熟练使用 Promise 和 async/await
3. 懂得何时并行、何时串行
4. 做好错误处理

## 参考资料
- [MDN: Asynchronous JavaScript](https://developer.mozilla.org/)
- JavaScript.info: Promises
- You Don't Know JS: Async & Performance
"""

    result = save_article_to_feishu(title, content)
    print(f"保存结果: {'成功 ✓' if result else '失败 ✗'}\n")


def example_4_batch_save():
    """示例4: 批量保存多篇文章"""
    print("\n=== 示例4: 批量保存 ===\n")

    articles = [
        {
            "title": "TypeScript 类型守卫",
            "content": "类型守卫是 TypeScript 中用于缩小类型范围的机制..."
        },
        {
            "title": "CSS Grid 布局入门",
            "content": "Grid 是 CSS 中最强大的布局系统..."
        },
        {
            "title": "Git 工作流最佳实践",
            "content": "良好的 Git 工作流能大幅提升团队协作效率..."
        }
    ]

    success_count = 0
    for article in articles:
        if save_article_to_feishu(article["title"], article["content"]):
            success_count += 1
            print(f"✓ 已保存: {article['title']}")
        else:
            print(f"✗ 保存失败: {article['title']}")

    print(f"\n批量保存完成: {success_count}/{len(articles)} 篇成功\n")


def main():
    """主函数 - 运行所有示例"""
    print("\n" + "="*60)
    print("飞书多维表格集成 - 使用示例")
    print("="*60)

    # 检查环境变量配置
    required_vars = [
        "FEISHU_APP_ID",
        "FEISHU_APP_SECRET",
        "FEISHU_BITABLE_APP_TOKEN",
        "FEISHU_BITABLE_TABLE_ID"
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print("\n⚠️  警告: 以下环境变量未配置:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n请先配置环境变量，参考:")
        print("   ~/.agents/skills/feynman/references/feishu-setup-guide.md\n")
        return

    # 运行示例
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        examples = {
            "1": example_1_basic,
            "2": example_2_feynman_note,
            "3": example_3_markdown_article,
            "4": example_4_batch_save
        }

        if example_num in examples:
            examples[example_num]()
        else:
            print(f"未知示例: {example_num}")
            print("可用示例: 1, 2, 3, 4")
    else:
        # 运行所有示例
        example_1_basic()
        input("按回车继续下一个示例...")

        example_2_feynman_note()
        input("按回车继续下一个示例...")

        example_3_markdown_article()
        input("按回车继续下一个示例...")

        example_4_batch_save()

    print("="*60)
    print("所有示例执行完成！")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
