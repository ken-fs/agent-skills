# 飞书多维表格集成配置指南

本指南将帮助你配置飞书多维表格，用于自动保存文章（标题、内容、创建时间）。

---

## 第一步：创建飞书应用

### 1. 登录飞书开放平台

访问：https://open.feishu.cn/app

### 2. 创建企业自建应用

1. 点击「创建企业自建应用」
2. 填写应用信息：
   - **应用名称**：文章管理助手（或任意名称）
   - **应用描述**：自动保存文章到多维表格
   - **应用图标**：可选
3. 点击「创建」

### 3. 获取应用凭证

创建完成后，进入应用详情页：

1. 在「凭证与基础信息」页面，找到：
   - **App ID**（应用ID）
   - **App Secret**（应用密钥）
2. 复制并保存这两个值（稍后需要配置到环境变量）

---

## 第二步：配置应用权限

### 1. 添加 API 权限

在应用管理页面，点击左侧「权限管理」，添加以下权限：

**必需权限**：
- `bitable:app` - 查看、评论、编辑和管理多维表格
  - 具体权限项：
    - `bitable:app:readonly` - 查看多维表格
    - `bitable:app:readwrite` - 编辑多维表格

**权限申请步骤**：
1. 点击「权限管理」
2. 搜索 `bitable`
3. 勾选相关权限
4. 点击「保存」

### 2. 发布应用版本

1. 在「版本管理与发布」页面
2. 点击「创建版本」
3. 填写版本说明（如：v1.0 - 初始版本）
4. 点击「保存」
5. 点击「申请发布」
6. 等待管理员审核（如果你是管理员，可以直接通过）

---

## 第三步：创建多维表格

### 1. 创建多维表格文档

1. 打开飞书，进入任意群组或个人空间
2. 点击「+」→「多维表格」
3. 创建新的多维表格

### 2. 配置表格字段

在多维表格中，创建以下三个字段：

| 字段名称 | 字段类型 | 说明 |
|---------|---------|------|
| **标题** | 单行文本 | 文章标题 |
| **内容** | 多行文本 | 文章正文内容 |
| **创建时间** | 日期 | 自动记录创建时间（包含日期和时间） |

**配置步骤**：
1. 点击列标题旁的「+」添加新字段
2. 选择字段类型
3. 输入字段名称（**必须**完全一致：标题、内容、创建时间）
4. 对于「创建时间」字段，选择「日期」类型，并勾选「包含时间」

### 3. 获取多维表格标识

**获取 App Token**：
1. 打开多维表格
2. 查看浏览器地址栏，URL 格式如下：
   ```
   https://xxx.feishu.cn/base/[APP_TOKEN]?table=[TABLE_ID]&view=[VIEW_ID]
   ```
3. 复制 `APP_TOKEN` 部分（通常是一长串字符，如：`bascnxxxxxxxxxxxxxx`）

**获取 Table ID**：
1. 在同一个 URL 中，复制 `table=` 后面的部分
2. 这就是 `TABLE_ID`（如：`tblxxxxxxxxxxxxxx`）

**示例 URL 解析**：
```
https://example.feishu.cn/base/bascnAbC123XYZ/wiki/wkcnDef456UVW?table=tblGhi789RST

App Token: bascnAbC123XYZ
Table ID: tblGhi789RST
```

---

## 第四步：授权应用访问多维表格

### 方法一：通过多维表格设置授权

1. 打开刚创建的多维表格
2. 点击右上角「...」→「高级设置」
3. 找到「应用访问权限」
4. 点击「添加应用」
5. 搜索并选择你创建的应用（如：文章管理助手）
6. 授予「可编辑」权限
7. 点击「确定」

### 方法二：通过开放平台授权（推荐）

1. 进入飞书开放平台 - 应用管理页面
2. 点击「可用性设置」
3. 在「可用范围」中选择：
   - 所有员工（推荐）
   - 或指定部门/人员
4. 保存设置

---

## 第五步：配置环境变量

### Windows 系统

**方式一：用户环境变量（推荐）**

1. 右键「此电脑」→「属性」→「高级系统设置」
2. 点击「环境变量」
3. 在「用户变量」区域，点击「新建」
4. 添加以下四个环境变量：

```
变量名: FEISHU_APP_ID
变量值: cli_xxxxxxxxxxxxx（你的 App ID）

变量名: FEISHU_APP_SECRET
变量值: xxxxxxxxxxxxx（你的 App Secret）

变量名: FEISHU_BITABLE_APP_TOKEN
变量值: bascnxxxxxxxxxxxxx（多维表格的 App Token）

变量名: FEISHU_BITABLE_TABLE_ID
变量值: tblxxxxxxxxxxxxx（表格的 Table ID）
```

5. 点击「确定」保存
6. **重启终端**（PowerShell 或 CMD）使配置生效

**方式二：通过 PowerShell 临时设置**

```powershell
$env:FEISHU_APP_ID = "cli_xxxxxxxxxxxxx"
$env:FEISHU_APP_SECRET = "xxxxxxxxxxxxx"
$env:FEISHU_BITABLE_APP_TOKEN = "bascnxxxxxxxxxxxxx"
$env:FEISHU_BITABLE_TABLE_ID = "tblxxxxxxxxxxxxx"
```

⚠️ 注意：此方法仅在当前终端会话有效，关闭后失效。

### macOS / Linux 系统

编辑 `~/.bashrc` 或 `~/.zshrc`：

```bash
export FEISHU_APP_ID="cli_xxxxxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxx"
export FEISHU_BITABLE_APP_TOKEN="bascnxxxxxxxxxxxxx"
export FEISHU_BITABLE_TABLE_ID="tblxxxxxxxxxxxxx"
```

保存后执行：
```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

---

## 第六步：测试集成

### 1. 安装依赖

确保已安装 Python 3.7+ 和 requests 库：

```bash
pip install requests
```

### 2. 运行测试

```bash
cd C:\Users\Administrator\.agents\skills\feynman\scripts
python save_to_feishu.py --test
```

**预期输出**：
```
✅ 文章已保存到飞书多维表格
   标题: 测试文章 - 2026-01-22 14:30:00
   记录ID: recxxxxxxxxxxxxx
✅ 测试成功！
```

### 3. 验证结果

1. 打开你的飞书多维表格
2. 应该能看到一条新记录：
   - **标题**：测试文章 - [当前时间]
   - **内容**：测试内容（包含 Markdown 格式）
   - **创建时间**：当前时间

---

## 使用方式

### 方法一：直接调用 Python 函数

```python
from scripts.save_to_feishu import save_article_to_feishu

# 保存文章
title = "我的文章标题"
content = """
这是文章的内容。

可以包含多段落、Markdown 格式等。
"""

save_article_to_feishu(title, content)
```

### 方法二：从文件保存

```bash
# 保存 Markdown 文件
python save_to_feishu.py --file "article.md"

# 保存 JSON 文件
python save_to_feishu.py --file "article.json"
```

**JSON 文件格式**：
```json
{
  "title": "文章标题",
  "content": "文章内容..."
}
```

### 方法三：集成到 Feynman Skill

在 Feynman 学习流程完成后，自动保存笔记到飞书：

```python
# 在 feynman 命令中调用
from scripts.save_to_feishu import save_article_to_feishu

# 学习完成后保存
save_article_to_feishu(
    title=f"Feynman 学习笔记: {concept}",
    content=f"""# {concept}

## 简单解释
{simple_explanation}

## 类比
{analogy}

## 核心要点
{key_takeaways}
"""
)
```

---

## 常见问题

### Q1: 提示"获取 token 失败"

**可能原因**：
- App ID 或 App Secret 配置错误
- 应用未发布或未通过审核

**解决方法**：
1. 检查环境变量配置是否正确
2. 确认应用已发布并启用
3. 重新生成 App Secret 并更新配置

### Q2: 提示"保存失败: no permission"

**可能原因**：
- 应用未授权访问该多维表格
- 权限范围不足

**解决方法**：
1. 按照「第四步」重新授权应用
2. 确保应用有 `bitable:app:readwrite` 权限

### Q3: 字段名不匹配错误

**错误信息**：`field not found` 或 `invalid field`

**解决方法**：
1. 确保多维表格中的字段名**完全一致**：
   - `标题`（不是"标题名称"或"title"）
   - `内容`（不是"正文"或"content"）
   - `创建时间`（不是"时间"或"创建日期"）
2. 检查字段类型是否正确：
   - 标题：单行文本
   - 内容：多行文本
   - 创建时间：日期（包含时间）

### Q4: App Token 或 Table ID 找不到

**解决方法**：
1. 打开多维表格
2. 仔细查看浏览器地址栏
3. 使用浏览器开发者工具（F12）→ Network 选项卡
4. 刷新页面，查看请求中的 `app_token` 和 `table_id` 参数

---

## 安全建议

1. **不要**将 App ID 和 App Secret 提交到代码仓库
2. 使用环境变量或密钥管理工具存储凭证
3. 定期轮换 App Secret
4. 限制应用的可用范围和权限
5. 在 `.gitignore` 中添加：
   ```
   .env
   *.key
   *secret*
   ```

---

## 参考文档

- [飞书开放平台文档](https://open.feishu.cn/document/)
- [多维表格 API 文档](https://open.feishu.cn/document/server-docs/docs/bitable-v1/bitable-overview)
- [飞书应用权限说明](https://open.feishu.cn/document/server-docs/api-call-guide/token-management/app-access-token)

---

## 技术支持

如遇到问题，可以：
1. 查看飞书开放平台的 API 调试工具
2. 检查应用的「事件与回调」日志
3. 使用 `--test` 模式进行调试
4. 查看完整的错误信息和响应代码
