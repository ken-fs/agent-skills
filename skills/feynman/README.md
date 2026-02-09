# Feynman Skill - 飞书多维表格集成

将 Feynman 学习笔记自动保存到飞书多维表格，方便后续回顾和管理。

---

## ✨ 功能特性

- ✅ 自动保存学习笔记到飞书多维表格
- ✅ 支持标题、内容、创建时间三个核心字段
- ✅ 完整的配置验证工具
- ✅ 丰富的使用示例
- ✅ 详细的配置指南

---

## 📁 文件结构

```
feynman/
├── SKILL.md                          # Skill 主配置文件
├── commands/
│   ├── feynman.md                    # Feynman 学习流程（含飞书集成）
│   ├── explain.md                    # 概念解释命令
│   └── simplify.md                   # 简化解释命令
├── scripts/
│   ├── save_to_feishu.py            # 核心保存脚本 ⭐
│   ├── check_config.py              # 配置检查工具 🔧
│   ├── example_usage.py             # 使用示例 📚
│   └── feishu_bitable.py            # 旧版本（已废弃）
└── references/
    └── feishu-setup-guide.md        # 完整配置指南 📖
```

---

## 🚀 快速开始

### 第一步：配置飞书

按照 [完整配置指南](references/feishu-setup-guide.md) 完成以下步骤：

1. **创建飞书应用** - 获取 App ID 和 App Secret
2. **配置应用权限** - 添加多维表格读写权限
3. **创建多维表格** - 添加"标题"、"内容"、"创建时间"字段
4. **获取表格标识** - 从 URL 中提取 App Token 和 Table ID
5. **配置环境变量** - 设置必需的环境变量

### 第二步：验证配置

运行配置检查工具，确保一切就绪：

```bash
cd C:\Users\Administrator\.agents\skills\feynman\scripts
python check_config.py
```

**预期输出**：
```
[1/5] 检查环境变量配置...
  ✓ 飞书应用 ID (FEISHU_APP_ID): cli_xxxxx...
  ✓ 飞书应用密钥 (FEISHU_APP_SECRET): xxxxx...
  ✓ 多维表格 App Token (FEISHU_BITABLE_APP_TOKEN): bascn...
  ✓ 表格 Table ID (FEISHU_BITABLE_TABLE_ID): tblxx...

[2/5] 验证应用凭证...
  ✓ 应用凭证有效，成功获取访问令牌

[3/5] 检查应用权限...
  ✓ 应用有权限访问多维表格

[4/5] 检查表格字段配置...
  ✓ 字段 '标题' 存在且类型正确 (文本)
  ✓ 字段 '内容' 存在且类型正确 (文本)
  ✓ 字段 '创建时间' 存在且类型正确 (日期)

[5/5] 测试写入操作...
  ✓ 写入测试成功，记录ID: recxxxxx
  ✓ 请在飞书多维表格中查看测试记录

🎉 所有检查通过！飞书集成配置正确。
```

### 第三步：开始使用

有多种使用方式：

#### 方式一：命令行测试

```bash
# 运行快速测试
python save_to_feishu.py --test

# 从文件保存
python save_to_feishu.py --file "article.md"
```

#### 方式二：在 Feynman 流程中使用

使用 `/feynman` 命令学习概念，完成后会自动询问是否保存到飞书：

```
User: /feynman React Hooks

Claude: [完成 Feynman 学习流程...]

Would you like to save this learning note to Feishu (飞书多维表格)?

User: 是

Claude: ✅ 学习笔记已保存到飞书多维表格
```

#### 方式三：Python 代码调用

```python
from scripts.save_to_feishu import save_article_to_feishu

title = "我的学习笔记"
content = """
# 学习内容

这里是笔记正文...
"""

save_article_to_feishu(title, content)
```

---

## 📚 使用示例

查看 [example_usage.py](scripts/example_usage.py) 了解更多用法：

```bash
# 运行所有示例
python example_usage.py

# 运行特定示例
python example_usage.py 1  # 基本用法
python example_usage.py 2  # Feynman 笔记格式
python example_usage.py 3  # Markdown 文章
python example_usage.py 4  # 批量保存
```

---

## 🔧 环境变量配置

需要配置以下 4 个环境变量：

| 变量名 | 说明 | 获取方式 |
|--------|------|---------|
| `FEISHU_APP_ID` | 飞书应用 ID | 开放平台 - 应用详情 - 凭证与基础信息 |
| `FEISHU_APP_SECRET` | 飞书应用密钥 | 开放平台 - 应用详情 - 凭证与基础信息 |
| `FEISHU_BITABLE_APP_TOKEN` | 多维表格 App Token | 多维表格 URL 中的 `/base/{token}` 部分 |
| `FEISHU_BITABLE_TABLE_ID` | 表格 Table ID | 多维表格 URL 中的 `table={id}` 部分 |

### Windows 配置示例

**PowerShell (临时)**：
```powershell
$env:FEISHU_APP_ID = "cli_xxxxx"
$env:FEISHU_APP_SECRET = "xxxxx"
$env:FEISHU_BITABLE_APP_TOKEN = "bascnxxxxx"
$env:FEISHU_BITABLE_TABLE_ID = "tblxxxxx"
```

**系统环境变量 (永久)**：
1. 右键"此电脑" → "属性" → "高级系统设置"
2. "环境变量" → "新建"
3. 添加上述 4 个变量
4. 重启终端

### macOS/Linux 配置示例

编辑 `~/.bashrc` 或 `~/.zshrc`：

```bash
export FEISHU_APP_ID="cli_xxxxx"
export FEISHU_APP_SECRET="xxxxx"
export FEISHU_BITABLE_APP_TOKEN="bascnxxxxx"
export FEISHU_BITABLE_TABLE_ID="tblxxxxx"
```

---

## 📊 多维表格字段要求

在飞书多维表格中创建以下字段（**字段名必须完全一致**）：

| 字段名 | 字段类型 | 配置要求 |
|--------|---------|---------|
| **标题** | 单行文本 | - |
| **内容** | 多行文本 | 启用富文本格式 |
| **创建时间** | 日期 | 包含日期和时间 |

---

## ❓ 常见问题

### Q1: 提示"获取 token 失败"

**解决方法**：
1. 检查 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 是否正确
2. 确认应用已发布并启用
3. 运行 `python check_config.py` 诊断问题

### Q2: 提示"no permission"

**解决方法**：
1. 在飞书多维表格中，点击右上角"..." → "高级设置"
2. "应用访问权限" → "添加应用" → 选择你的应用
3. 授予"可编辑"权限

### Q3: 字段名不匹配错误

**解决方法**：
确保多维表格中的字段名**完全一致**（区分大小写）：
- ✅ `标题` `内容` `创建时间`
- ❌ `title` `content` `时间`

### Q4: 如何找到 App Token 和 Table ID？

打开多维表格，查看浏览器地址栏：

```
https://xxx.feishu.cn/base/[APP_TOKEN]?table=[TABLE_ID]&view=xxx
                            ^^^^^^^^^^        ^^^^^^^^^^
```

---

## 🔒 安全建议

1. ❌ **不要**将 App Secret 提交到代码仓库
2. ✅ 使用环境变量存储敏感信息
3. ✅ 定期轮换 App Secret
4. ✅ 限制应用的可用范围和权限
5. ✅ 在 `.gitignore` 中添加：
   ```
   .env
   *.key
   *secret*
   ```

---

## 📖 完整文档

- [飞书配置完整指南](references/feishu-setup-guide.md) - 图文详解配置步骤
- [save_to_feishu.py](scripts/save_to_feishu.py) - 核心保存脚本源码
- [check_config.py](scripts/check_config.py) - 配置验证工具源码
- [example_usage.py](scripts/example_usage.py) - 使用示例源码

---

## 🎯 下一步

1. ✅ 完成飞书配置
2. ✅ 运行 `check_config.py` 验证配置
3. ✅ 使用 `/feynman` 命令学习新概念
4. ✅ 将笔记保存到飞书多维表格
5. ✅ 在飞书中管理和回顾学习笔记

---

## 📝 更新日志

### v2.0 - 2026-01-22

- ✨ 简化字段为：标题、内容、创建时间
- ✨ 新增配置检查工具 `check_config.py`
- ✨ 新增使用示例 `example_usage.py`
- 📖 完善配置指南文档
- 🔧 优化错误提示和调试信息

### v1.0

- 🎉 初始版本，支持 Feynman 笔记保存

---

## 📞 技术支持

如遇到问题，可以：

1. 运行 `python check_config.py` 进行诊断
2. 查看 [完整配置指南](references/feishu-setup-guide.md)
3. 检查[飞书开放平台文档](https://open.feishu.cn/document/)
4. 查看应用的事件与回调日志

---

**享受学习，享受记录！** 📚✨
