# Feynman Skill - 飞书集成使用检查清单

使用此清单确保你已正确完成所有配置步骤并能顺利使用飞书多维表格集成功能。

---

## 📋 配置前准备清单

### ✅ 飞书账号和权限

- [ ] 拥有飞书企业账号
- [ ] 有权限创建企业自建应用
- [ ] 有权限创建多维表格
- [ ] 能够访问飞书开放平台 (https://open.feishu.cn)

### ✅ 本地环境

- [ ] 已安装 Python 3.7 或更高版本
  ```bash
  python --version  # 应显示 Python 3.7+
  ```
- [ ] 已安装 pip 包管理器
  ```bash
  pip --version
  ```
- [ ] 网络能正常访问飞书 API
  ```bash
  ping open.feishu.cn
  ```

---

## 🔧 飞书应用配置清单

### ✅ 第一步：创建应用

- [ ] 访问 https://open.feishu.cn/app
- [ ] 点击「创建企业自建应用」
- [ ] 填写应用名称（如：Feynman 学习助手）
- [ ] 填写应用描述
- [ ] 上传应用图标（可选）
- [ ] 创建成功

### ✅ 第二步：获取凭证

- [ ] 进入应用详情页
- [ ] 找到「凭证与基础信息」
- [ ] 复制 **App ID** 并保存
  ```
  格式：cli_xxxxxxxxxxxxx
  你的 App ID：_________________
  ```
- [ ] 复制 **App Secret** 并保存（注意保密）
  ```
  格式：xxxxxxxxxxxxx
  你的 App Secret：_________________
  ```

### ✅ 第三步：配置权限

- [ ] 点击左侧「权限管理」
- [ ] 搜索 `bitable`
- [ ] 勾选以下权限：
  - [ ] `bitable:app:readonly` - 查看多维表格
  - [ ] `bitable:app:readwrite` - 编辑多维表格
- [ ] 点击「保存」

### ✅ 第四步：发布应用

- [ ] 点击「版本管理与发布」
- [ ] 点击「创建版本」
- [ ] 填写版本说明（如：v1.0 初始版本）
- [ ] 点击「保存」
- [ ] 点击「申请发布」
- [ ] 等待审核通过（或自己通过）
- [ ] 应用状态变为「已发布」

---

## 📊 多维表格配置清单

### ✅ 第一步：创建多维表格

- [ ] 在飞书中创建新的多维表格
- [ ] 为表格命名（如：学习笔记库）

### ✅ 第二步：配置字段

创建以下三个字段（**字段名必须完全一致**）：

- [ ] **字段 1：标题**
  - [ ] 字段名：`标题`（不是 title）
  - [ ] 字段类型：单行文本

- [ ] **字段 2：内容**
  - [ ] 字段名：`内容`（不是 content）
  - [ ] 字段类型：多行文本
  - [ ] 启用富文本格式（可选）

- [ ] **字段 3：创建时间**
  - [ ] 字段名：`创建时间`（不是时间或创建日期）
  - [ ] 字段类型：日期
  - [ ] 勾选「包含时间」

### ✅ 第三步：获取表格标识

- [ ] 打开多维表格
- [ ] 查看浏览器地址栏
- [ ] 地址格式：`https://xxx.feishu.cn/base/{APP_TOKEN}?table={TABLE_ID}&view=xxx`
- [ ] 复制 **App Token**
  ```
  格式：bascnxxxxxxxxxxxxx
  你的 App Token：_________________
  ```
- [ ] 复制 **Table ID**
  ```
  格式：tblxxxxxxxxxxxxx
  你的 Table ID：_________________
  ```

### ✅ 第四步：授权应用访问

- [ ] 在多维表格中点击右上角「...」
- [ ] 选择「高级设置」
- [ ] 点击「应用访问权限」
- [ ] 点击「添加应用」
- [ ] 搜索并选择你创建的应用
- [ ] 授予「可编辑」权限
- [ ] 保存设置

---

## ⚙️ 环境变量配置清单

### ✅ 方式 A：使用配置向导（推荐）

- [ ] 打开 PowerShell
- [ ] 进入 scripts 目录
  ```powershell
  cd C:\Users\Administrator\.agents\skills\feynman\scripts
  ```
- [ ] 运行配置向导
  ```powershell
  .\setup.ps1
  ```
- [ ] 按提示输入所有配置信息
- [ ] 选择配置方式（推荐选择「2. 永久设置」）
- [ ] 等待配置完成

### ✅ 方式 B：手动配置（高级用户）

- [ ] 打开 PowerShell（以管理员身份）
- [ ] 执行以下命令（替换为你的实际值）：
  ```powershell
  [Environment]::SetEnvironmentVariable("FEISHU_APP_ID", "你的App ID", "User")
  [Environment]::SetEnvironmentVariable("FEISHU_APP_SECRET", "你的App Secret", "User")
  [Environment]::SetEnvironmentVariable("FEISHU_BITABLE_APP_TOKEN", "你的App Token", "User")
  [Environment]::SetEnvironmentVariable("FEISHU_BITABLE_TABLE_ID", "你的Table ID", "User")
  ```
- [ ] 同时在当前会话设置：
  ```powershell
  $env:FEISHU_APP_ID = "你的App ID"
  $env:FEISHU_APP_SECRET = "你的App Secret"
  $env:FEISHU_BITABLE_APP_TOKEN = "你的App Token"
  $env:FEISHU_BITABLE_TABLE_ID = "你的Table ID"
  ```

---

## ✅ 配置验证清单

### ✅ 第一步：安装依赖

- [ ] 安装 requests 库
  ```bash
  pip install requests
  ```

### ✅ 第二步：运行配置检查

- [ ] 进入 scripts 目录
  ```bash
  cd C:\Users\Administrator\.agents\skills\feynman\scripts
  ```
- [ ] 运行检查工具
  ```bash
  python check_config.py
  ```

### ✅ 第三步：验证检查结果

预期应该通过所有 5 项检查：

- [ ] ✅ [1/5] 检查环境变量配置
- [ ] ✅ [2/5] 验证应用凭证
- [ ] ✅ [3/5] 检查应用权限
- [ ] ✅ [4/5] 检查表格字段配置
- [ ] ✅ [5/5] 测试写入操作

**如果有任何错误，请根据错误提示进行修复后重新检查。**

---

## 🧪 功能测试清单

### ✅ 测试 1：快速测试

- [ ] 运行测试命令
  ```bash
  python save_to_feishu.py --test
  ```
- [ ] 看到成功提示：`✅ 文章已保存到飞书多维表格`
- [ ] 打开飞书多维表格，能看到测试记录

### ✅ 测试 2：从文件保存

- [ ] 创建测试文件 `test.md`
  ```markdown
  # 测试标题

  这是测试内容。
  ```
- [ ] 运行保存命令
  ```bash
  python save_to_feishu.py --file test.md
  ```
- [ ] 在飞书表格中验证记录

### ✅ 测试 3：使用示例

- [ ] 运行示例脚本
  ```bash
  python example_usage.py 1
  ```
- [ ] 验证保存成功

---

## 🎓 使用流程检查清单

### ✅ Feynman 学习流程

- [ ] 在 Claude Code 中使用 `/feynman` 命令
  ```
  /feynman React Hooks
  ```
- [ ] 完成 Feynman 四步学习法
- [ ] 看到保存提示：「Would you like to save this learning note to Feishu?」
- [ ] 回复「是」或「好」或「保存」
- [ ] 看到成功提示
- [ ] 在飞书表格中查看笔记

---

## 🐛 问题排查清单

### ❌ 如果出现「获取 token 失败」

- [ ] 检查 `FEISHU_APP_ID` 是否正确
- [ ] 检查 `FEISHU_APP_SECRET` 是否正确
- [ ] 确认应用已发布并启用
- [ ] 尝试重新生成 App Secret

### ❌ 如果出现「no permission」

- [ ] 检查应用权限是否包含 `bitable:app:readwrite`
- [ ] 检查是否在多维表格中授权了应用
- [ ] 确认应用发布状态为「已发布」
- [ ] 尝试重新授权应用访问表格

### ❌ 如果出现「field not found」

- [ ] 检查字段名是否为：`标题`、`内容`、`创建时间`
- [ ] 注意字段名大小写必须完全一致
- [ ] 检查是否有多余空格
- [ ] 重新创建字段（如果名称错误）

### ❌ 如果出现「环境变量未配置」

- [ ] 确认已设置所有 4 个环境变量
- [ ] 重启终端窗口
- [ ] 使用 `echo $env:FEISHU_APP_ID` 验证
- [ ] 重新运行配置向导

---

## 📚 文档阅读清单

建议按以下顺序阅读文档：

1. [ ] **快速开始** - `README.md`
   - 了解项目概述
   - 掌握快速开始步骤

2. [ ] **配置指南** - `references/feishu-setup-guide.md`
   - 详细的配置步骤
   - 图文并茂的说明

3. [ ] **快速参考** - `references/quick-reference.md`
   - 常用命令速查
   - 故障排查速查表

4. [ ] **使用示例** - `scripts/example_usage.py`
   - 实际代码示例
   - 多种使用场景

5. [ ] **优化总结** - `OPTIMIZATION_SUMMARY.md`
   - 完整功能说明
   - 扩展建议

---

## ✨ 完成检查

全部完成后，你应该能够：

- [ ] ✅ 使用 `/feynman` 命令学习新概念
- [ ] ✅ 自动保存学习笔记到飞书
- [ ] ✅ 在飞书多维表格中查看和管理笔记
- [ ] ✅ 使用命令行工具保存任意文章
- [ ] ✅ 使用 Python 代码批量保存笔记
- [ ] ✅ 运行配置检查工具诊断问题

---

## 🎉 恭喜！

如果你完成了以上所有检查项，说明飞书多维表格集成已成功配置！

**下一步：**
- 开始使用 `/feynman` 命令学习你感兴趣的概念
- 将所有笔记保存到飞书进行统一管理
- 定期回顾和复习已保存的笔记

---

## 📞 需要帮助？

如遇到问题，请：

1. **运行诊断工具**：`python check_config.py`
2. **查看故障排查**：`OPTIMIZATION_SUMMARY.md` → 故障排查指南
3. **参考完整文档**：`references/feishu-setup-guide.md`
4. **查看 API 文档**：https://open.feishu.cn/document/

---

**祝学习愉快！** 📚✨

*最后更新：2026-01-22*
