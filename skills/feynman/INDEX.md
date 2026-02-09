# 📚 Feynman Skill 文档导航索引

> 快速找到你需要的文档

---

## 🎯 我想...

### 快速开始使用

👉 **[QUICKSTART.md](QUICKSTART.md)** - 3 分钟快速上手
- 最简化的配置步骤
- 立即开始使用

### 了解项目概况

👉 **[README.md](README.md)** - 项目总览
- 功能特性介绍
- 文件结构说明
- 常用命令参考

### 完整配置飞书

👉 **[references/feishu-setup-guide.md](references/feishu-setup-guide.md)** - 完整配置指南
- 创建飞书应用（图文详解）
- 配置应用权限
- 创建多维表格
- 环境变量配置
- 常见问题解答

### 快速查找命令

👉 **[references/quick-reference.md](references/quick-reference.md)** - 快速参考卡
- 常用命令速查
- 环境变量清单
- 故障排查速查表

### 按步骤完成配置

👉 **[CHECKLIST.md](CHECKLIST.md)** - 配置检查清单
- 详细的配置步骤
- 逐项检查清单
- 配置验证指南

### 学习如何使用

👉 **[scripts/example_usage.py](scripts/example_usage.py)** - 使用示例
- 基本用法示例
- Feynman 笔记格式
- Markdown 文章保存
- 批量保存操作

### 了解优化内容

👉 **[OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md)** - 优化总结
- 功能对比（新版 vs 旧版）
- 使用场景说明
- 扩展建议
- 故障排查指南

### 了解项目架构

👉 **[DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md)** - 目录结构
- 可视化文件树
- 文件依赖关系
- 模块功能说明
- 快速导航

### 查看完整报告

👉 **[FINAL_REPORT.md](FINAL_REPORT.md)** - 完成报告
- 交付文件清单
- 技术架构说明
- 使用流程说明
- 版本信息

---

## 🔧 我遇到了...

### 不知道如何配置

→ 运行配置向导：
```powershell
cd scripts
.\setup.ps1
```

### 配置完想验证是否正确

→ 运行配置检查：
```bash
python check_config.py
```

### 找不到 App Token 或 Table ID

→ 查看：[feishu-setup-guide.md](references/feishu-setup-guide.md) - 第三步

### 提示"no permission"

→ 查看：[OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md) - 故障排查指南

### 字段名不匹配错误

→ 确保字段名为：`标题`、`内容`、`创建时间`（完全一致）

### 环境变量未生效

→ 重启终端窗口，或查看：[quick-reference.md](references/quick-reference.md) - 手动配置

---

## 📖 按角色选择文档

### 初学者路径

1. **[QUICKSTART.md](QUICKSTART.md)** - 快速上手
2. **[feishu-setup-guide.md](references/feishu-setup-guide.md)** - 详细配置
3. **[CHECKLIST.md](CHECKLIST.md)** - 验证配置
4. **[example_usage.py](scripts/example_usage.py)** - 学习使用

### 高级用户路径

1. **[README.md](README.md)** - 项目概况
2. **[quick-reference.md](references/quick-reference.md)** - 快速参考
3. **[OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md)** - 深入了解
4. **[DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md)** - 架构设计

### 开发者路径

1. **[FINAL_REPORT.md](FINAL_REPORT.md)** - 完整报告
2. **[DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md)** - 架构文档
3. **[scripts/save_to_feishu.py](scripts/save_to_feishu.py)** - 源码阅读
4. **[scripts/check_config.py](scripts/check_config.py)** - 源码阅读

---

## 🛠️ 工具脚本索引

### 配置工具

| 脚本 | 用途 | 命令 |
|------|------|------|
| `setup.ps1` | PowerShell 配置向导 | `.\setup.ps1` |
| `setup.bat` | 批处理配置向导 | `setup.bat` |
| `check_config.py` | 配置验证工具 | `python check_config.py` |

### 功能脚本

| 脚本 | 用途 | 命令 |
|------|------|------|
| `save_to_feishu.py` | 保存到飞书 | `python save_to_feishu.py --test` |
| `example_usage.py` | 使用示例 | `python example_usage.py` |

---

## 📑 文档类型分类

### 📘 入门文档

- [QUICKSTART.md](QUICKSTART.md) - 快速上手
- [README.md](README.md) - 项目总览
- [quick-reference.md](references/quick-reference.md) - 快速参考

### 📗 配置文档

- [feishu-setup-guide.md](references/feishu-setup-guide.md) - 完整配置指南
- [CHECKLIST.md](CHECKLIST.md) - 配置检查清单

### 📙 使用文档

- [example_usage.py](scripts/example_usage.py) - 使用示例
- [quick-reference.md](references/quick-reference.md) - 命令速查

### 📕 深入文档

- [OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md) - 优化总结
- [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) - 架构文档
- [FINAL_REPORT.md](FINAL_REPORT.md) - 完成报告

---

## 🎯 常见任务快捷方式

### 首次配置

```bash
# 1. 运行配置向导
.\setup.ps1

# 2. 验证配置
python check_config.py

# 3. 测试功能
python save_to_feishu.py --test
```

### 日常使用

```bash
# Feynman 学习
/feynman [概念]

# 命令行保存
python save_to_feishu.py --file article.md

# 查看示例
python example_usage.py
```

### 故障排查

```bash
# 1. 运行诊断
python check_config.py

# 2. 查看文档
# OPTIMIZATION_SUMMARY.md - 故障排查指南

# 3. 检查清单
# CHECKLIST.md - 问题排查清单
```

---

## 📞 获取帮助的优先级

1. **运行诊断工具** → `python check_config.py`
2. **查看快速参考** → [quick-reference.md](references/quick-reference.md)
3. **查看故障排查** → [OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md)
4. **查看完整配置指南** → [feishu-setup-guide.md](references/feishu-setup-guide.md)
5. **查看检查清单** → [CHECKLIST.md](CHECKLIST.md)

---

## 📂 完整文件清单

```
feynman/
├── 📄 README.md                    - 项目总览
├── 📄 QUICKSTART.md                - 快速上手（3 分钟）
├── 📄 CHECKLIST.md                 - 配置检查清单
├── 📄 OPTIMIZATION_SUMMARY.md      - 优化总结
├── 📄 DIRECTORY_STRUCTURE.md       - 目录结构
├── 📄 FINAL_REPORT.md              - 完成报告
├── 📄 INDEX.md                     - 本文档（导航索引）
│
├── 📁 scripts/
│   ├── save_to_feishu.py          - 核心保存脚本
│   ├── check_config.py            - 配置检查工具
│   ├── example_usage.py           - 使用示例
│   ├── setup.ps1                  - PowerShell 配置向导
│   └── setup.bat                  - 批处理配置向导
│
└── 📁 references/
    ├── feishu-setup-guide.md      - 完整配置指南
    └── quick-reference.md         - 快速参考卡
```

---

**提示**：建议将本文档加入书签，作为快速导航入口！ 🔖
