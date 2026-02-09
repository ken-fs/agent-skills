# 飞书多维表格集成 - 快速参考卡

---

## 🚀 快速开始（3 步完成）

### 1️⃣ 运行配置向导

```powershell
# PowerShell (推荐)
cd C:\Users\Administrator\.agents\skills\feynman\scripts
.\setup.ps1

# 或使用批处理
setup.bat
```

### 2️⃣ 验证配置

```bash
python check_config.py
```

### 3️⃣ 开始使用

```bash
# 测试
python save_to_feishu.py --test

# 或在 Claude Code 中
/feynman React Hooks
```

---

## 📋 必需的环境变量

| 变量 | 示例值 | 获取位置 |
|------|--------|---------|
| `FEISHU_APP_ID` | `cli_a1b2c3d4e5` | 开放平台 → 应用详情 |
| `FEISHU_APP_SECRET` | `xyz123abc456` | 开放平台 → 应用详情 |
| `FEISHU_BITABLE_APP_TOKEN` | `bascnXXXXXX` | 表格 URL 中 `/base/{token}` |
| `FEISHU_BITABLE_TABLE_ID` | `tblXXXXXX` | 表格 URL 中 `table={id}` |

---

## 🔧 手动配置（PowerShell）

```powershell
# 设置环境变量（永久）
[Environment]::SetEnvironmentVariable("FEISHU_APP_ID", "cli_xxxxx", "User")
[Environment]::SetEnvironmentVariable("FEISHU_APP_SECRET", "your_secret", "User")
[Environment]::SetEnvironmentVariable("FEISHU_BITABLE_APP_TOKEN", "bascnxxxxx", "User")
[Environment]::SetEnvironmentVariable("FEISHU_BITABLE_TABLE_ID", "tblxxxxx", "User")

# 在当前会话生效
$env:FEISHU_APP_ID = "cli_xxxxx"
$env:FEISHU_APP_SECRET = "your_secret"
$env:FEISHU_BITABLE_APP_TOKEN = "bascnxxxxx"
$env:FEISHU_BITABLE_TABLE_ID = "tblxxxxx"
```

---

## 📊 多维表格字段配置

在飞书多维表格中创建以下字段（**名称必须完全一致**）：

```
┌──────────┬──────────┬────────────────┐
│ 字段名   │ 字段类型 │ 配置要求       │
├──────────┼──────────┼────────────────┤
│ 标题     │ 单行文本 │ -              │
│ 内容     │ 多行文本 │ 启用富文本     │
│ 创建时间 │ 日期     │ 包含日期+时间  │
└──────────┴──────────┴────────────────┘
```

---

## 💻 常用命令

### 配置和测试

```bash
# 运行配置向导
.\setup.ps1

# 检查配置
python check_config.py

# 快速测试
python save_to_feishu.py --test

# 查看使用示例
python example_usage.py
```

### 保存文章

```bash
# 从文件保存
python save_to_feishu.py --file article.md

# 在 Python 中调用
from save_to_feishu import save_article_to_feishu
save_article_to_feishu("标题", "内容...")
```

---

## 🐛 常见问题速查

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `获取 token 失败` | App ID/Secret 错误 | 检查环境变量，确认应用已发布 |
| `no permission` | 未授权访问表格 | 在表格设置中添加应用权限 |
| `field not found` | 字段名不匹配 | 确保字段名为：标题、内容、创建时间 |
| `invalid field type` | 字段类型错误 | 检查字段类型是否正确 |

---

## 🔍 获取 App Token 和 Table ID

打开多维表格，查看浏览器地址栏：

```
https://xxx.feishu.cn/base/bascnAbC123/wiki/xxx?table=tblXyz789&view=xxx
                           ↑↑↑↑↑↑↑↑↑↑↑↑            ↑↑↑↑↑↑↑↑↑
                           App Token             Table ID
```

复制对应部分即可。

---

## 📝 使用示例代码

### 基本用法

```python
from save_to_feishu import save_article_to_feishu

save_article_to_feishu(
    title="我的学习笔记",
    content="这是笔记内容..."
)
```

### Feynman 笔记格式

```python
title = f"Feynman 学习笔记: {concept}"
content = f"""# {concept}

## 简单解释
{simple_explanation}

## 类比
{analogy}

## 核心要点
{key_takeaways}
"""

save_article_to_feishu(title, content)
```

### 批量保存

```python
articles = [
    {"title": "笔记1", "content": "内容1"},
    {"title": "笔记2", "content": "内容2"}
]

for article in articles:
    save_article_to_feishu(article["title"], article["content"])
```

---

## 🔐 安全检查清单

- [ ] 不要将 App Secret 提交到 Git 仓库
- [ ] 使用环境变量存储敏感信息
- [ ] 在 `.gitignore` 添加：`.env`, `*secret*`
- [ ] 定期轮换 App Secret
- [ ] 限制应用的可用范围

---

## 📚 完整文档位置

| 文档 | 路径 |
|------|------|
| 🏠 总览 | `README.md` |
| 📖 配置指南 | `references/feishu-setup-guide.md` |
| 💾 保存脚本 | `scripts/save_to_feishu.py` |
| 🔧 配置检查 | `scripts/check_config.py` |
| 📚 使用示例 | `scripts/example_usage.py` |
| ⚙️ 配置向导 | `scripts/setup.ps1` |

---

## 🎯 工作流程

```
┌─────────────────┐
│ 1. 运行配置向导 │
│   setup.ps1     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. 验证配置     │
│   check_config  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. 使用 Feynman │
│   /feynman ...  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. 保存到飞书   │
│   自动询问      │
└─────────────────┘
```

---

## 📞 获取帮助

1. **配置问题**：运行 `python check_config.py` 诊断
2. **使用问题**：查看 `example_usage.py` 示例
3. **详细指南**：阅读 `feishu-setup-guide.md`
4. **API 文档**：https://open.feishu.cn/document/

---

**提示**：将此文件保存为书签，随时查阅！ 🔖
