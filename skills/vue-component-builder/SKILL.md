---
name: vue-component-builder
description: 为 AI Storyflow 项目生成符合规范的 Vue 3 组件、API 服务、Composable 和 Pinia Store。基于项目实际架构（Vue 3 + Naive UI + TypeScript + Pinia + Scoped SCSS）。当用户请求创建 Vue 组件、新建页面、添加 API 服务、编写 composable 或 store 时触发。触发关键词包括："创建组件"、"新建页面"、"添加组件"、"写一个Vue组件"、"create component"、"add a dialog/card/form"。
---

# Vue Component Builder

为 AI Storyflow 前端项目生成符合代码规范的 Vue 3 组件及相关代码。所有生成的代码严格遵循项目的 `CODE_STANDARDS.md`、`AGENTS.md` 和 `API_STANDARDS.md` 规范。

## 触发场景

- 创建新的 Vue SFC 组件（`.vue` 文件）
- 创建 API 服务（`*.service.ts`）
- 创建 Composable（`use*.ts`）
- 创建 Pinia Store
- 创建常量定义文件
- 为现有功能模块添加新的 UI 组件

## 工作流程

### 第一步：确认组件需求

确认以下信息后再生成代码：

1. **组件类型**: 展示组件 / 表单组件 / 对话框 / 卡片 / 页面视图
2. **放置位置**: `components/<module>/` 或 `views/`
3. **数据来源**: 是否需要新增 API 服务或 composable
4. **是否需要新增常量**: 枚举、标签映射、限制值等

### 第二步：确定需要生成的文件

根据组件需求，确定完整的文件清单：

| 需求 | 生成文件 | 位置 |
|------|---------|------|
| UI 组件 | `ComponentName.vue` | `src/components/<module>/` |
| 页面 | `PageName.vue` | `src/views/<module>/` |
| API 服务 | `xxx.service.ts` | `src/api/services/` |
| API 端点 | 更新 `endpoints.ts` | `src/api/endpoints.ts` |
| Composable | `useXxx.ts` | `src/composables/` |
| Store | `xxx.ts` | `src/stores/` |
| 常量 | `xxx.ts` | `src/constants/` |
| 类型 | 更新 `types/index.ts` 或在 service 中定义 | `src/types/` |

### 第三步：按顺序生成代码

按以下顺序生成，确保依赖关系正确：

1. 常量定义（枚举 + 标签映射）
2. 类型定义
3. API 端点（更新 `endpoints.ts`）
4. API 服务（继承 `BaseService`）
5. Composable 或 Store
6. Vue 组件

### 第四步：代码规范检查

生成完成后，逐项检查：

- [ ] 所有注释使用中文
- [ ] 无硬编码字符串（状态、消息、URL 等均使用常量）
- [ ] 无 `any` 类型
- [ ] API 更新操作使用 `PUT`（非 `PATCH`）
- [ ] API 端点在 `endpoints.ts` 中定义
- [ ] API 服务继承 `BaseService`
- [ ] 使用 Naive UI 组件（非 Element Plus）
- [ ] Props 使用 `interface + withDefaults` 定义
- [ ] Emits 使用 `interface` 类型声明
- [ ] 样式使用 `<style scoped lang="scss">`

## 核心规范参考

生成代码前，读取 `references/project-conventions.md` 获取完整的项目约定，包括：
- Vue SFC 结构顺序
- Props/Emits 定义规范
- API 服务模式（BaseService 继承）
- Composable 模式
- Pinia Store 模式
- 常量定义模式（枚举 + 标签映射）
- 样式规范（设计系统变量、圆角、色彩）
- Naive UI 组件速查表

## 关键约束

### 必须使用 Naive UI

```vue
<!-- ✅ 正确 -->
<n-button type="primary" @click="handleSubmit">提交</n-button>
<n-modal v-model:show="showModal" preset="dialog" title="确认">
  <n-form ref="formRef" :model="formData" :rules="rules">
    <n-form-item label="标题" path="title">
      <n-input v-model:value="formData.title" placeholder="请输入标题" />
    </n-form-item>
  </n-form>
</n-modal>

<!-- ❌ 禁止使用 Element Plus -->
<el-button>不要使用</el-button>
```

### 图标使用 @vicons

```typescript
import { AddOutlined, DeleteOutlined } from '@vicons/antd'
import { RefreshOutline } from '@vicons/ionicons5'

// 在 Naive UI 中使用
<n-button>
  <template #icon>
    <n-icon><AddOutlined /></n-icon>
  </template>
  新建
</n-button>
```

### 中文注释

```typescript
// 获取章节列表        ✅
// Get episode list    ❌
```

### 禁止 any 类型

```typescript
// ✅ 正确
const items = ref<Episode[]>([])
const handleSelect = (key: string) => { ... }

// ❌ 错误
const items = ref<any[]>([])
const handleSelect = (key: any) => { ... }
```

### API 更新用 PUT

```typescript
// ✅ 正确
update(id: string, data: UpdateDto): Promise<Entity> {
  return this.put(API_ENDPOINTS.ENTITY(id), data)
}

// ❌ 禁止
update(id: string, data: UpdateDto): Promise<Entity> {
  return this.patch(API_ENDPOINTS.ENTITY(id), data)
}
```

## 文件命名规范

| 类型 | 命名规则 | 示例 |
|------|---------|------|
| Vue 组件 | PascalCase | `EpisodeCard.vue`, `BatchProductionDialog.vue` |
| API 服务 | kebab-case + `.service.ts` | `episode.service.ts` |
| Composable | camelCase, `use` 前缀 | `useEpisode.ts` |
| Store | camelCase | `project.ts`, `jobs.ts` |
| 常量 | camelCase | `episode.ts`, `enums.ts` |
| 类型 | camelCase | `index.ts`, `error.ts` |

## 组件分类与放置

| 组件类型 | 目录 | 示例 |
|---------|------|------|
| 通用/可复用 | `components/common/` | `ModelSelector.vue` |
| 章节相关 | `components/episode/` | `EpisodeCard.vue`, `EpisodeCreateDialog.vue` |
| 分镜相关 | `components/storyboard/` | `ShotTable.vue`, `BeatList.vue` |
| 指标/数据 | `components/metrics/` | `GenerationMetricsCard.vue` |
| 任务/进度 | `components/task/` | `GlobalTaskIndicator.vue` |
| 主体库 | `components/subject/` | `SubjectLibrary.vue` |
| 提示词 | `components/prompt/` | `PromptList.vue` |
| 项目配置 | `components/project/` | `ModelConfigForm.vue` |
| 页面视图 | `views/<module>/` | `ProjectInfo.vue` |

## Resources

### references/

- `project-conventions.md` — 完整的项目前端约定，包含 Vue SFC 结构、API 服务模式、Composable 模式、Store 模式、常量定义、样式规范和 Naive UI 组件速查表。生成代码前务必参考此文件。
