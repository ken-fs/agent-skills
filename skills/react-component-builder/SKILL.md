---
name: react-component-builder
description: This skill should be used when users want to quickly create React components. Triggers include "创建组件", "新建组件", "写一个React组件", "build a component", "create a Button/Card/Modal component". Supports all component types including UI, form, layout, and data display components using TypeScript, Tailwind CSS, and shadcn/ui.
---

# React Component Builder

快速创建符合最佳实践的 React 组件，支持 TypeScript、Tailwind CSS 和 shadcn/ui。

## 组件类型

| 类型 | 示例 | 特点 |
|------|------|------|
| **UI 组件** | Button, Card, Badge, Avatar | 基础展示，高复用性 |
| **表单组件** | Input, Select, Checkbox, DatePicker | 受控/非受控，验证支持 |
| **布局组件** | Container, Grid, Stack, Sidebar | Flexbox/Grid 布局 |
| **数据展示** | Table, List, DataCard, Stat | 数据绑定，分页排序 |
| **反馈组件** | Modal, Toast, Alert, Skeleton | 用户交互反馈 |
| **导航组件** | Navbar, Tabs, Breadcrumb, Pagination | 路由集成 |

## 组件创建流程

1. 确定组件类型和功能需求
2. 设计 Props 接口（TypeScript interface）
3. 实现组件结构和样式（Tailwind CSS）
4. 添加交互逻辑（useState, useEffect 等）
5. 导出组件和类型

## 组件模板

### 基础组件结构

```tsx
import { type ComponentProps, forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface ComponentNameProps extends ComponentProps<'div'> {
  variant?: 'default' | 'primary' | 'secondary'
  size?: 'sm' | 'md' | 'lg'
}

const ComponentName = forwardRef<HTMLDivElement, ComponentNameProps>(
  ({ className, variant = 'default', size = 'md', children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          // 基础样式
          'inline-flex items-center justify-center rounded-md',
          // 变体样式
          variant === 'default' && 'bg-background text-foreground',
          variant === 'primary' && 'bg-primary text-primary-foreground',
          variant === 'secondary' && 'bg-secondary text-secondary-foreground',
          // 尺寸样式
          size === 'sm' && 'h-8 px-3 text-sm',
          size === 'md' && 'h-10 px-4 text-base',
          size === 'lg' && 'h-12 px-6 text-lg',
          className
        )}
        {...props}
      >
        {children}
      </div>
    )
  }
)

ComponentName.displayName = 'ComponentName'

export { ComponentName, type ComponentNameProps }
```

### 表单组件结构

```tsx
import { type ComponentProps, forwardRef, useId } from 'react'
import { cn } from '@/lib/utils'

interface InputProps extends Omit<ComponentProps<'input'>, 'size'> {
  label?: string
  error?: string
  size?: 'sm' | 'md' | 'lg'
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, size = 'md', ...props }, ref) => {
    const id = useId()

    return (
      <div className="flex flex-col gap-1.5">
        {label && (
          <label htmlFor={id} className="text-sm font-medium text-foreground">
            {label}
          </label>
        )}
        <input
          id={id}
          ref={ref}
          className={cn(
            'flex w-full rounded-md border border-input bg-background px-3 ring-offset-background',
            'placeholder:text-muted-foreground',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
            'disabled:cursor-not-allowed disabled:opacity-50',
            size === 'sm' && 'h-8 text-sm',
            size === 'md' && 'h-10 text-base',
            size === 'lg' && 'h-12 text-lg',
            error && 'border-destructive focus-visible:ring-destructive',
            className
          )}
          {...props}
        />
        {error && <p className="text-sm text-destructive">{error}</p>}
      </div>
    )
  }
)

Input.displayName = 'Input'

export { Input, type InputProps }
```

## 样式规范

### Tailwind CSS 类名顺序

1. **布局**: `flex`, `grid`, `block`, `inline-flex`
2. **定位**: `relative`, `absolute`, `fixed`
3. **尺寸**: `w-*`, `h-*`, `min-*`, `max-*`
4. **间距**: `p-*`, `m-*`, `gap-*`
5. **边框**: `border`, `rounded-*`
6. **背景**: `bg-*`
7. **文字**: `text-*`, `font-*`
8. **效果**: `shadow-*`, `opacity-*`
9. **过渡**: `transition-*`, `duration-*`
10. **状态**: `hover:*`, `focus:*`, `disabled:*`

### cn 工具函数

确保项目中有 `cn` 工具函数：

```tsx
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

## shadcn/ui 集成

### 扩展 shadcn/ui 组件

```tsx
import { Button, type ButtonProps } from '@/components/ui/button'
import { Loader2 } from 'lucide-react'

interface LoadingButtonProps extends ButtonProps {
  loading?: boolean
}

const LoadingButton = ({ loading, disabled, children, ...props }: LoadingButtonProps) => {
  return (
    <Button disabled={disabled || loading} {...props}>
      {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
      {children}
    </Button>
  )
}

export { LoadingButton, type LoadingButtonProps }
```

## 最佳实践

### Props 设计

- 使用 `interface` 定义 Props 类型
- 继承原生 HTML 元素属性（`ComponentProps<'div'>`）
- 提供合理的默认值
- 使用联合类型限制可选值（`'sm' | 'md' | 'lg'`）

### 组件设计

- 使用 `forwardRef` 支持 ref 转发
- 设置 `displayName` 便于调试
- 使用 `cn()` 合并类名，支持自定义样式覆盖
- 使用 `...props` 透传剩余属性

### 文件命名

- 组件文件：`PascalCase.tsx`（如 `Button.tsx`）
- 组件目录：`kebab-case`（如 `date-picker/`）

### 目录结构

```
components/
├── ui/                    # 基础 UI 组件 (shadcn/ui)
├── forms/                 # 表单相关组件
└── layouts/               # 布局组件
```

## 常用 Hooks 模式

```tsx
// 受控组件
const [value, setValue] = useState('')
<Input value={value} onChange={(e) => setValue(e.target.value)} />

// 切换状态
const [open, setOpen] = useState(false)
<Modal open={open} onOpenChange={setOpen} />

// 异步操作
const [loading, setLoading] = useState(false)
const handleSubmit = async () => {
  setLoading(true)
  try { await submitData() } finally { setLoading(false) }
}
```
