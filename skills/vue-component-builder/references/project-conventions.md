# AI Storyflow 前端项目约定

## 技术栈

- **框架**: Vue 3 (Composition API + `<script setup lang="ts">`)
- **UI 组件库**: Naive UI (`n-button`, `n-input`, `n-modal`, `n-dropdown`, `n-data-table` 等)
- **图标**: `@vicons/antd` 或 `@vicons/ionicons5`
- **状态管理**: Pinia (`defineStore` + Composition API 风格)
- **样式**: Scoped SCSS + Tailwind CSS 辅助
- **类型**: TypeScript 严格模式，禁止使用 `any`
- **构建工具**: Vite
- **路由**: Vue Router

## 目录结构

```
apps/web/src/
├── api/
│   ├── base.ts               # BaseService 基类
│   ├── endpoints.ts          # API_ENDPOINTS 常量
│   ├── index.ts              # Axios 实例
│   └── services/             # API 服务（继承 BaseService）
│       ├── index.ts           # 统一导出
│       ├── project.service.ts
│       ├── episode.service.ts
│       └── ...
├── components/               # 可复用组件
│   ├── common/               # 通用组件
│   ├── episode/              # 章节相关组件
│   ├── storyboard/           # 分镜相关组件
│   ├── metrics/              # 指标组件
│   ├── task/                 # 任务组件
│   └── ...
├── composables/              # 组合式函数（use* 命名）
│   ├── useEpisode.ts
│   ├── useStoryboard.ts
│   └── ...
├── constants/                # 常量定义
│   ├── enums.ts              # 枚举
│   ├── episode.ts            # 章节相关常量
│   ├── styles.ts             # 画风常量
│   ├── messages/             # 消息常量
│   ├── labels/               # 标签常量
│   └── ...
├── stores/                   # Pinia Store
│   ├── project.ts
│   └── jobs.ts
├── types/                    # 类型定义
│   └── index.ts              # 从 @ai-workflow/shared-types 重导出
├── views/                    # 页面视图
└── utils/                    # 工具函数
```

## Vue 组件结构规范

### SFC 文件结构顺序

```vue
<template>
  <!-- 模板 -->
</template>

<script setup lang="ts">
// 1. 导入
import { ref, computed } from 'vue'
import { NButton, NModal } from 'naive-ui'
import { SomeIcon } from '@vicons/antd'
import { useEpisode } from '@/composables/useEpisode'
import type { Episode } from '@/api/services/episode.service'
import { EpisodeStoryboardStatus } from '@/constants/episode'

// 2. Props 定义（interface + withDefaults）
interface Props {
  episode: Episode
  draggable?: boolean
  selected?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  draggable: false,
  selected: false,
})

// 3. Emits 定义
interface Emits {
  (e: 'click'): void
  (e: 'edit', episode: Episode): void
  (e: 'delete', episode: Episode): void
}

const emit = defineEmits<Emits>()

// 4. Composables
const { episodes, loading } = useEpisode(props.projectId)

// 5. 响应式状态
const isVisible = ref(false)
const formData = ref({ title: '' })

// 6. 计算属性
const hasScript = computed(() => {
  return props.episode.script && props.episode.script.trim().length > 0
})

// 7. 方法
const handleClick = () => {
  emit('click')
}
</script>

<style scoped lang="scss">
// 样式
</style>
```

### Props 定义规范

```typescript
// ✅ 正确：使用 interface + withDefaults
interface Props {
  title: string
  count?: number
  items?: string[]
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
  items: () => [],
})

// ❌ 错误：使用运行时声明
const props = defineProps({
  title: { type: String, required: true },
})
```

### Emits 定义规范

```typescript
// ✅ 正确：使用 interface 类型声明
interface Emits {
  (e: 'update', value: string): void
  (e: 'delete', id: string): void
}

const emit = defineEmits<Emits>()

// ❌ 错误：使用字符串数组
const emit = defineEmits(['update', 'delete'])
```

## API 服务规范

### 继承 BaseService

```typescript
import { BaseService } from '../base'
import { API_ENDPOINTS } from '../endpoints'

class EpisodeService extends BaseService {
  // 获取列表
  list(projectId: string): Promise<Episode[]> {
    return this.get(API_ENDPOINTS.EPISODES(projectId))
  }

  // 创建
  create(projectId: string, data: CreateEpisodeRequest): Promise<Episode> {
    return this.post(API_ENDPOINTS.EPISODES(projectId), data)
  }

  // 更新（必须使用 PUT，禁止 PATCH）
  update(projectId: string, episodeId: string, data: UpdateEpisodeRequest): Promise<Episode> {
    return this.put(API_ENDPOINTS.EPISODE(projectId, episodeId), data)
  }

  // 删除
  delete(projectId: string, episodeId: string): Promise<void> {
    return this.del<void>(API_ENDPOINTS.EPISODE(projectId, episodeId))
  }
}

export const episodeService = new EpisodeService()
```

### 端点定义

```typescript
// endpoints.ts 中定义
export const API_ENDPOINTS = {
  EPISODES: (projectId: string) => `/projects/${projectId}/episodes`,
  EPISODE: (projectId: string, episodeId: string) =>
    `/projects/${projectId}/episodes/${episodeId}`,
} as const
```

## Composable 规范

```typescript
import { ref, computed, type Ref } from 'vue'
import { someService } from '@/api/services'

export function useSomething(id: Ref<string> | string) {
  const idRef = ref(id)

  // 状态
  const items = ref<Item[]>([])
  const loading = ref(false)
  const error = ref<Error | null>(null)

  // 计算属性
  const itemCount = computed(() => items.value.length)

  // 方法
  const fetchItems = async () => {
    loading.value = true
    error.value = null
    try {
      items.value = await someService.list(idRef.value)
    } catch (err) {
      error.value = err as Error
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    loading,
    error,
    itemCount,
    fetchItems,
  }
}
```

## Pinia Store 规范

```typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { someService } from '../api/services'
import type { SomeType } from '@ai-workflow/shared-types'

export const useSomeStore = defineStore('some', () => {
  // 状态
  const items = ref<SomeType[]>([])
  const current = ref<SomeType | null>(null)
  const loading = ref(false)

  // 方法
  const fetchItems = async () => {
    loading.value = true
    try {
      items.value = await someService.getList()
    } finally {
      loading.value = false
    }
  }

  const create = async (data: CreateDto) => {
    loading.value = true
    try {
      const item = await someService.create(data) as SomeType
      items.value.unshift(item)
      return item
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    current,
    loading,
    fetchItems,
    create,
  }
})
```

## 常量定义规范

### 枚举 + 标签模式

```typescript
// constants/xxx.ts

// 枚举定义
export enum SomeStatus {
  DRAFT = 'DRAFT',
  ACTIVE = 'ACTIVE',
  COMPLETED = 'COMPLETED',
}

// 中文标签映射
export const SOME_STATUS_LABELS: Record<SomeStatus, string> = {
  [SomeStatus.DRAFT]: '草稿',
  [SomeStatus.ACTIVE]: '进行中',
  [SomeStatus.COMPLETED]: '已完成',
}

// 数值常量
export const SOME_LIMITS = {
  MIN: 1,
  MAX: 100,
  DEFAULT: 10,
}
```

## 样式规范

### Scoped SCSS

```vue
<style scoped lang="scss">
.component-root {
  position: relative;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border: var(--border-default);
  border-radius: 20px;
  transition: all 0.2s ease-out;

  &:hover {
    transform: translateY(-4px);
    border: var(--border-hover);
  }

  &.is-active {
    border: 2px solid #5E5CE6;
  }
}
</style>
```

### 设计系统变量

项目使用 CSS 变量系统：
- `--border-default` — 默认边框
- `--border-hover` — 悬浮边框
- 主色调: `#6366f1` / `#4f46e5` (indigo)
- 文本色: `#0f172a`(标题), `#475569`(正文), `#64748b`(次要), `#94a3b8`(占位)
- 背景色: `#f8fafc`, `#f1f5f9`
- 圆角: `8px`(小), `10px`(中), `20px`(大/卡片)

## Naive UI 常用组件

| 类型 | 组件 | 用途 |
|------|------|------|
| 按钮 | `n-button` | 操作按钮 |
| 输入 | `n-input` | 文本输入 |
| 选择 | `n-select` | 下拉选择 |
| 模态框 | `n-modal` | 弹窗 |
| 对话框 | `n-dialog` | 确认对话框 |
| 消息 | `useMessage()` | 提示消息 |
| 下拉菜单 | `n-dropdown` | 下拉菜单 |
| 表格 | `n-data-table` | 数据表格 |
| 表单 | `n-form` + `n-form-item` | 表单 |
| 标签页 | `n-tabs` + `n-tab-pane` | 标签切换 |
| 抽屉 | `n-drawer` | 侧边抽屉 |
| 标签 | `n-tag` | 状态标签 |
| 空状态 | `n-empty` | 空数据提示 |
| 加载 | `n-spin` | 加载状态 |
| 分页 | `n-pagination` | 分页 |
| 提示 | `n-tooltip` | 悬浮提示 |
| 弹出 | `n-popconfirm` | 确认弹出 |

## 类型来源

- 共享类型从 `@ai-workflow/shared-types` 导入
- 前端专用类型在 `src/types/` 下定义
- API 服务的请求/响应类型在对应 `.service.ts` 文件中定义
- 组件 Props/Emits 类型在组件内部用 interface 定义

## 禁止事项

- ❌ 禁止使用 `any` 类型
- ❌ 禁止使用 PATCH 方法（更新用 PUT）
- ❌ 禁止硬编码 URL（用 `API_ENDPOINTS.*`）
- ❌ 禁止直接使用 axios（用 BaseService）
- ❌ 禁止使用 Element Plus 组件（用 Naive UI）
- ❌ 禁止硬编码状态字符串（用常量枚举）
- ❌ 禁止创建独立 API 文件（用 services/*.service.ts）
