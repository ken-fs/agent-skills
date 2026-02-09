# 飞书集成 - 3 分钟快速上手指南

> 从零开始，3 分钟完成配置并开始使用

---

## 🎯 你需要什么？

✅ 飞书企业账号
✅ Python 3.7+
✅ 5 分钟时间

---

## 📋 三步完成配置

### 第 1 步：创建飞书应用（2 分钟）

1. 访问 https://open.feishu.cn/app
2. 点击「创建企业自建应用」
3. 填写名称（如：学习助手），点击创建
4. 复制 **App ID** 和 **App Secret**
5. 在「权限管理」中添加：
   - ✅ `bitable:app:readonly`
   - ✅ `bitable:app:readwrite`
6. 点击「版本管理与发布」→「创建版本」→「申请发布」

### 第 2 步：创建多维表格（1 分钟）

1. 在飞书中创建新的多维表格
2. 添加三个字段（**名称必须完全一致**）：
   - `标题` - 单行文本
   - `内容` - 多行文本
   - `创建时间` - 日期（包含时间）
3. 从 URL 中复制 **App Token** 和 **Table ID**：
   ```
   https://xxx.feishu.cn/base/bascnXXX?table=tblXXX
                                ↑↑↑         ↑↑↑
                            App Token   Table ID
   ```
4. 在表格设置中添加应用权限（可编辑）

### 第 3 步：运行配置向导（1 分钟）

```powershell
cd C:\Users\Administrator\.agents\skills\feynman\scripts
.\setup.ps1
```

按提示输入刚才获取的 4 个值，选择「2. 永久设置」，完成！

---

## ✅ 验证配置

```bash
python check_config.py
```

如果看到 `🎉 所有检查通过！`，说明配置成功！

---

## 🚀 开始使用

### 方式 1：Feynman 学习（推荐）

```
/feynman React Hooks
```

学习完成后会询问是否保存，回复「是」即可。

### 方式 2：命令行保存

```bash
# 测试
python save_to_feishu.py --test

# 保存文件
python save_to_feishu.py --file article.md
```

### 方式 3：Python 代码

```python
from save_to_feishu import save_article_to_feishu

save_article_to_feishu("标题", "内容...")
```

---

## 🐛 遇到问题？

运行诊断工具：
```bash
python check_config.py
```

根据错误提示修复，常见问题：
- ❌ 字段名不匹配 → 确保是：`标题`、`内容`、`创建时间`
- ❌ 无权限 → 在表格设置中添加应用权限
- ❌ Token 失败 → 检查 App ID/Secret 是否正确

---

## 📚 更多帮助

- 📖 完整配置指南：`references/feishu-setup-guide.md`
- 🔖 快速参考卡：`references/quick-reference.md`
- ✅ 检查清单：`CHECKLIST.md`

---

**就这么简单！开始享受学习吧！** 🎉
