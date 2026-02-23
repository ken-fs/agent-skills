# AI 画布技术调研报告 (Jimeng vs Oiioii)

本报告详细分析了**即梦 AI (Jimeng)** 和 **Oiioii AI** 两款产品的画布技术实现方案，并提供开源技术选型建议。

## 1. 竞品技术分析对比

| 维度 | 即梦 AI (Jimeng) | Oiioii AI | 海螺 AI (Hailuo Canvas) |
| :--- | :--- | :--- | :--- |
| **核心定位** | **专业图像生成与编辑** <br> (类似 Photoshop + AI) | **故事板与工作流编排** <br> (类似 Miro + Agent) | **多模态对话与视频创作** <br> (Chat + Video Nodes) |
| **渲染技术** | **WebGL + WebAssembly** (高性能) | **SVG + DOM** (tldraw) | **Canvas + DOM Hybrid** (高性能混合) |
| **画布引擎** | 自研引擎 / CanvasKit (Skia) | **tldraw** (React 开源库) | **Custom Canvas** |
| **性能重点** | 像素级渲染、大量高清图处理 | 矢量图形、节点连接、拖拽 | 多媒体卡片(视频/音频)管理 |
| **典型功能** | 局部重绘、外绘、图层混合 | 故事卡片、Agent 协作 | 对话节点、视频生成、节点连线 |
| **复刻难度** | 高 (图形学、Wasm) | 低 (开源 tldraw) | 中 (混合架构交互同步) |

---

## 2. 详细技术拆解

### A. 即梦 AI (Jimeng)
*   **技术栈**: WebGL (Custom/Skia) + WebAssembly + Vue/React
*   **架构特点**:
    *   **高性能渲染**: 为了支持 4K+ 分辨率的 AI 生成图及其实时编辑（蒙版绘制、橡皮擦），它必须使用 GPU 加速的 WebGL 引擎。
    *   **像素操作**: 画布不仅是容器，还充当了图像处理引擎，支持像素级的合成和滤镜。
*   **复刻难度**: ⭐️⭐️⭐️⭐️⭐️ (需要图形学基础)

### B. Oiioii AI
*   **技术栈**: React + Vite + **tldraw** (开源)
*   **架构特点**:
    *   **直接使用开源库**: 经分析，Oiioii 直接使用了开源的 [tldraw](https://tldraw.dev/) 库作为画布底层。
    *   **SVG 渲染**: 它不处理复杂的像素操作，而是将图片、文字、视频作为“卡片”或“节点”在无限画布上排列。
    *   **侧重业务**: 它的核心不在画板本身，而在左侧的 Chat 面板与右侧画板的联动（即：Chat 生成脚本 -> 脚本转变为画板上的卡片 -> 卡片调用 AI 生成视频）。
*   **复刻难度**: ⭐️⭐️ (技术栈成熟，主要工作量在业务逻辑)

### C. 海螺 AI (Hailuo Canvas)
*   **技术栈**: Next.js + React + Ant Design + **Canvas (Main Rendering)**
*   **架构特点**:
    *   **Chat-First (对话驱动)**: 画布本质是对话产物的容器。HTML 源码显示其数据结构包含 `messageList` 和 `sectionDetailList`，证明画布是"Chat Section"的延伸。
    *   **自定义数据模型**: // 根据页面源码分析
        *   节点数据结构使用 `xStart`, `yStart`, `width`, `height` 绝对定位。
        *   核心对象是 `agentFile` (包含 `url`, `noWatermarkUrl`, `aiWatermarkUrl`)，证明它是专门为 **AI 生成资源** 设计的容器，而非通用绘图对象。
    *   **视频流媒体优先**: 节点大量包含视频属性 (`duration`, `playWidth`)，侧重于多媒体编排。
    *   **渲染技术**: 
        *   **Canvas 核心**: 用户反馈确认核心绘图区使用 `<canvas>` 元素，这通常用于高性能的无限画布缩放、平移和连接线绘制（类似 Miro 或 Figma 的底层实现）。
        *   **HTML/DOM 覆盖**: 视频播放器和复杂的富文本编辑（Chat Bubbles）很可能通过 HTML Overlay 覆盖在 Canvas 之上，形成 "Hybrid" 架构，以兼顾性能（Canvas 处理大量节点位置）和功能（DOM 处理视频控件）。
        *   UI 基础层使用 Ant Design。
*   **复刻难度**: ⭐️⭐️⭐️ (混合架构增加了坐标同步和事件穿透的复杂度)

## 4. 可行性分析：使用 tldraw 复刻海螺 AI

用户提问：*“如果使用 tldraw 可以实现海螺的效果不？有什么风险？”*

### 结论
**可以实现 MVP (最小可行性产品)，但难以达到海螺的生产级性能上限。**

### ✅ tldraw 的优势 (Why Yes)
1.  **开发速度极快**: tldraw 开箱即用了无限画布、缩放平移、选择工具、撤销重做等基础功能。用 React 开发自定义 Shape (如视频卡片) 非常简单。
2.  **React 生态亲和**: 海螺本身也是 React + Next.js，tldraw 完美契合及生态，可以直接复用现有的 Video Player 组件。
3.  **内置性能优化**: tldraw 内置了 **Viewport Culling (视口剔除)**，屏幕外的节点会自动隐藏 (`display: none`)，这在一定程度上缓解了 DOM 过多的卡顿问题。

### ⚠️ 核心风险 (Risks)

#### 1. 视频节点的 "DOM 爆炸" 问题
*   **海螺的方案**: **Canvas (绘图) + Hybrid DOM**。Canvas 绘制成千上万个矩形是非常廉价的，只有用户交互时才加载重型 DOM。
*   **tldraw 的方案**: **纯 DOM/SVG**。每个视频节点本质上都是一个 `div` 或 `foreignObject`。
*   **风险点**: 当画布上有 100+ 个视频卡片时，即使 tldraw 做了剔除，浏览器的 **内存占用 (Memory Footprint)** 和 **图层合成 (Compositing)** 压力依然巨大。浏览器对同时存在的 `<video>` 或 `<iframe>` 数量有限制，过多会导致页面崩溃或视频黑屏。

#### 2. 混合渲染层级 (Z-Index / Layering)
*   海螺的 "连线" 和 "背景" 是 Canvas 绘制的，性能极佳。
*   tldraw 的连线是 SVG DOM。在节点极其密集（例如数百个 AI 对话节点）时，SVG 的重排重绘 (Reflow/Repaint) 开销远大于 Canvas。

### 🚀 建议路线
*   **阶段一 (验证期)**: **直接用 tldraw**。如果你的目标是管理 < 50 个视频片段的 Storyboard，tldraw 是完美的，开发成本仅需 2-3 天。
*   **阶段二 (产品期)**: **魔改 tldraw 或自研 Canvas**。如果用户会创建包含 500+ 节点的超大项目，你需要“逃离” tldraw 的默认渲染机制，重写 renderer 层，将静态节点“降级”为 Canvas 绘制，仅对激活节点使用 DOM 渲染。这相当于把 tldraw 改造成了海螺的架构。

---

## 5. 深度分析：React + tldraw + WebGL 混合架构

用户提问：*“如果使用 React + Vite + tldraw + WebGL 的方式，有什么问题？后续要拓展或者会遇到什么问题？性能上有什么问题？”*

这是一个非常典型但**充满陷阱**的 "Hybrid Architecture" (混合架构)。

### A. 核心问题 (Current Problems)

1.  **"三明治" 层级问题 (The Sandwich Problem)**
    *   **现象**: WebGL (Canvas) 和 tldraw (DOM/SVG) 是两个独立的渲染层。
    *   **痛点**: 你无法轻易地让一个 WebGL 物体 "穿插" 在两个 tldraw 节点中间。
        *   ❌ 能够做到: WebGL 层全在最底下 (背景) 或全在最顶上 (遮罩)。
        *   ❌ **难以做到**: [ tldraw 节点 A ] -> [ WebGL 视频 ] -> [ tldraw 节点 B ]。
    *   **后果**: 你的应用层级会被强制分为 "背景层" 和 "UI 层"，限制了创意的自由度（例如无法用 tldraw 的画笔在 WebGL 视频上方做标注，除非画笔也是 WebGL 的）。

2.  **坐标系同步延迟 (Sync Jitter)**
    *   **现象**: tldraw 有自己的摄像机 (Camera) 逻辑（平移/缩放），WebGL 也有自己的 Viewport 变换矩阵。
    *   **痛点**: 当用户快速拖拽画布时，React 的渲染循环 (DOM更新) 和 WebGL 的渲染循环 (requestAnimationFrame) 可能不同步。
    *   **后果**: 会出现 **"果冻效应" (Rubber-banding)** — DOM 元素看起来比 WebGL 背景 "慢半拍" 或 "快半拍"，极度影响专业感。

3.  **事件穿透 (Event Drilling)**
    *   **现象**: 如果 WebGL 层在上面，它会挡住 tldraw 的鼠标事件；如果 tldraw 在上面，你没法操作 WebGL 里的物体。
    *   **痛点**: 你需要写一套复杂的 "事件转发系统" (Event Bus)，判断用户点击的位置到底是有 WebGL 物体还是 tldraw 空白处，然后手动分发事件。

### B. 后续拓展问题 (Future Expansion Risks)

1.  **导出与截图 (Export/Screenshot)**
    *   **问题**: 浏览器无法直接把 `<canvas>` (WebGL) 和 `<div>` (DOM) 一起截图。
    *   **卡点**: tldraw 自带的 `exportAsImage` 只能导出一张 SVG/PNG，**它会丢失你 WebGL 层的所有内容**。
    *   **解决成本**: 你必须手动用 `canvas.toDataURL()` 抓取 WebGL 画面，然后用 SVG `<image>` 标签强行塞回 tldraw 的导出流中，非常容易出 Bug（如分辨率对不齐）。

2.  **文字渲染 (Text Rendering)**
    *   **问题**: WebGL 渲染高质量文字（支持中文、换行、光标编辑）是图形学噩梦 (SDF Font)。
    *   **卡点**: 如果你想让 WebGL 里的物体带文字，你通常只能退回到 DOM 渲染文字。这又回到了 "三明治层级" 问题。

### C. 性能问题 (Performance)

1.  **双重渲染循环 (Double Loop Overhead)**
    *   React/tldraw 在跑主线程 diff 算法。
    *   WebGL (Pixi/Three) 在跑 requestAnimationFrame。
    *   **后果**: 笔记本电脑风扇狂转。即使画面静止，WebGL 为了响应可能的 shader 变化也常保持重绘，电池消耗大。

2.  **上下文切换与内存**
    *   浏览器同时维护复杂的 DOM 树 (tldraw) 和大显存占用的 WebGL Context。在移动端或低性能 PC 上，很容易触发进程崩溃。

### 🚀 架构建议

*   **如果你的核心体验是 "画板/笔记" (如 Miro)**: 坚持 **tldraw (SVG/DOM)**。不要引入 WebGL，除非作为纯静态背景。视频用 `<div>` 解决。
*   **如果你的核心体验是 "视频/图像处理" (如即梦)**: 放弃 tldraw 的渲染层。使用 **Pixi.js / Fabric.js (Canvas 2D)** 甚至原生 WebGL 重写渲染器。只复用 tldraw 的 *数据结构* (Store)，重写 *视图层* (View)。
*   **折中方案 (海螺模式)**:
    *   底层: Canvas 画连线、网格、背景。
    *   中层: DOM (React) 渲染视频卡片、文字、对话框。
    *   顶层: 另一个 Canvas 画临时的笔迹或选框。
    *   *不要使用全功能的 WebGL 3D 引擎混搭，除非你有专业图形学团队。*

---

## 6. 总结与建议

根据你的需求，需要在以下两条路线中选择：

### 路线一：做“图像编辑工具” (对标即梦)
如果你需要实现：局部重绘、图像扩充、像素级擦除。
*   **推荐引擎**: **LeaferJS** (高性能) 或 **Konva.js** (成熟稳定)。
*   **后端支持**: ComfyUI (处理复杂的 Inpainting/Outpainting 工作流)。
*   **架构**: 前端负责交互和选区坐标计算，后端负责图像生成。

### 路线二：做“工作流/故事板” (对标 Oiioii)
如果你需要实现：无限白板、节点连接、多图排列、AI 编排。
*   **推荐引擎**: **tldraw** (首选)。
    *   **优势**: 它是 React 生态中最好的无限画布库，自带完善的拖拽、连线、缩放逻辑。Oiioii 就是用它做的。
    *   **扩展性**: tldraw 提供了基于“形状 (Shape)”的扩展机制，你可以很容易地定义一个“AI 生成卡片”组件放入画布中。
*   **替代方案**: **React Flow** (如果更侧重流程图而非自由绘图)。

---

## 4. 推荐实现路线 (Roadmap)

### 复刻 Oiioii (最快落地 MVP 方案)

1.  **初始化项目**: 使用 `Vite + React`。
2.  **集成画布**: 安装 `tldraw` 库。
    ```bash
    npm install tldraw
    ```
3.  **自定义图形**: 利用 tldraw 的 Custom Shapes API，开发：
    *   `StoryBlock`: 显示脚本、分镜图的卡片组件。
    *   `AgentNode`: 代表不同 AI 角色（如导演、编剧）的节点。
4.  **AI 接入**:
    *   左侧 Sidebar 做 Chat 界面。
    *   调用 LLM 生成 JSON 格式的故事脚本。
    *   解析 JSON，调用 `editor.createShape(...)` 自动在画布上生成对应的卡片。

### 复刻即梦 (高性能专业方案)

1.  **前端**: React + **LeaferJS** (比 Fabric/Konva 更快，适合未来扩展)。
2.  **核心交互**:
    *   实现“画布漫游” (Zoom/Pan)。
    *   实现“图片上传”与“图层管理”。
    *   开发“蒙版画笔” (用于 Inpainting)。
3.  **后端**: 部署 **ComfyUI**。
    *   搭建 `Image-to-Image (Inpainting)` 工作流。
    *   通过 WebSocket 与前端通信，实时回传生成进度。

---

## 5. 即梦深度技术揭秘 (架构、难点与亮点)

### 技术架构图 (Technical Architecture)

即梦的实现并非单一技术，而是端到端的复杂系统：

```mermaid
graph TD
    User[用户操作] -->|交互事件| LynxUI[UI 层 (Lynx/React)]
    User -->|绘制/漫游| CanvasEngine[图形引擎 (C++ Wasm / WebGL)]
    
    subgraph Frontend [前端核心]
        LynxUI -- 双线程通信 --> CanvasEngine
        CanvasEngine -->|GPU 加速| Render[WebGL 渲染器]
        CanvasEngine -->|状态同步| Store[图层状态树]
    end
    
    subgraph AI_Backend [AI 服务层]
        CanvasEngine -->|上传遮罩/Prompt| Orchestrator[工作流编排]
        Orchestrator -->|Inpainting| SDModel[Seedance/SD 模型]
        Orchestrator -->|图像分析| Vision[CV 分析服务]
    end
    
    AI_Backend -->|生成结果| CanvasEngine
```

### 核心难点 (Implementation Challenges)

1.  **超大分辨率渲染与内存管理**:
    *   **问题**: AI 生成的图片通常是高偏分辨率（如 4K），且画布上可能堆积数十张图。传统 Canvas 2D 会导致内存暴涨甚至浏览器崩溃 (OOM)。
    *   **解决**: 必须使用 **分块渲染 (Tiled Rendering)** 和 **LOD (Level of Detail)** 技术。只渲染视口内的图片分块；缩小时渲染低清缩略图，放大时才加载高清纹理。WebAssembly 在此用于高效管理内存块。

2.  **坐标系转换与混合渲染**:
    *   **问题**: 既要支持矢量的 UI 控件（选框、手柄），又要支持位图的像素操作（画笔涂抹遮罩）。
    *   **解决**: 实现复杂的场景图 (Scene Graph)，将矢量层（SVG/Canvas Overlay）与位图层（WebGL Texture）的坐标系精确对齐。

3.  **实时交互与 AI 延迟**:
    *   **问题**: AI 生成需要时间（5-10秒），用户不能干等。
    *   **解决**: 乐观更新 (Optimistic UI)。用户涂抹遮罩后，前端立即生成“占位流光效果”，或者先返回低清预览图，后台高清图生成完毕后再无感替换。

### 产品亮点 (Product Highlights)

1.  **"所想即所得" 的工作流**:
    *   它不是简单的“画板”，而是将 **Prompt -> 生成 -> 修改 -> 扩展** 这一整套 AI 创作逻辑内化到了工具中。相比于 ComfyUI 的硬核节点，即梦将其封装为符合直觉的图形操作。

2.  **局部重绘 (Inpainting) 的交互体验**:
    *   它的“涂抹 -> 描述 -> 生成”流程非常顺滑。特别是**画笔的边缘羽化**和**自动遮罩**（利用 CV 算法自动吸附物体边缘），极大地降低了用户抠图的门槛。

3.  **无限外绘 (Outpainting)**:
    *   能够无缝地向外扩展图片。这需要在前端动态计算扩展区域的坐标，并将原图边缘与新生成的区域进行一种“不可见”的融合处理 (Seamless Blending)。

---

**总结建议**：
*   **追求效果酷炫、功能强大 (图像处理)** -> 选 **LeaferJS** 路线 (即梦模式)。
6. 终极架构方案 (The "Better" Way)

如果现在从零开始，使用最新的技术栈，可以实现一个比即梦和 Oiioii 更强大、更面向未来的**混合架构 (Hybrid Architecture)**。

### 核心理念：Hybrid Rendering + Local AI

*   **UI/画布层**: 使用 **tldraw** (SVG/React)。因为它解决了最麻烦的“无限画布交互”、“手势系统”、“DOM 覆盖”问题。不需要重造轮子。
*   **高性能渲染层**: 在 tldraw 中嵌入 **WebGL/WebGPU Overlay**。不要用 SVG 渲染大图，而是写一个自定义的 `WebImageNode`，底层用 WebGL/WebGPU 渲染纹理。这样既有 React 的开发效率，又有原生级的图像性能。
*   **端侧 AI (Edge AI)**: 利用 **WebGPU** 在浏览器运行小模型。
    *   **Segment Anything (SAM2)**: 实时运行在浏览器里。用户鼠标悬停时，利用 WebGPU 算力直接推理出物体遮罩 (Mask)，**0 延迟**，无需请求服务器。即梦目前还是依赖服务器 CV 算法，有延迟。

### 推荐架构栈 (Next-Gen Stack)

| 模块 | 推荐技术 | 理由 |
| :--- | :--- | :--- |
| **App Shell** | React + Vite | 行业标准。 |
| **Canvas** | **tldraw (SDK)** | 最好的交互体验，支持自定义 Shape。 |
| **Image Engine** | **PixiJS** / **wgpu** | 在 tldraw 的 Custom Shape 中嵌入 WebGL Context，处理滤镜和像素操作。 |
| **Client AI** | **Transformers.js (WebGPU)** | 在浏览器直接运行 SAM2 (分割)、Depth Anything (深度图)。 |
| **Server AI** | **ComfyUI** | 只处理繁重的 Generative AI (Flux, SD3)。 |

### 方案优势
1.  **开发快**: tldraw 解决了 90% 的画布交互问题。
2.  **性能高**: WebGL 处理图片，SVG 处理 UI，各取所长。
3.  **体验绝杀**: 端侧 AI 带来的“实时自动抠图/选区”，是目前 Web 端竞品很少具备的杀手级体验。

---

## 7. 渲染技术深度对比：SVG vs WebGL/WebGPU

用户常问：*“为什么不能直接用 `<img>` 或 `<image>` (SVG) 标签显示所有图片？为什么即梦这种产品非要上 WebGL？”*

下表从**性能**和**体验（体感）**两个维度进行对比：

| 维度 | SVG / DOM (如 Oiioii, tldraw 默认) | WebGL / WebGPU (如即梦, Figma) |
| :--- | :--- | :--- |
| **处理 100 张 4K 图片** | **卡顿/崩溃**。浏览器要为每张图创建 DOM 节点和图层合成，内存占用极高，滚动时掉帧明显。 | **丝滑**。GPU 将图片作为纹理 (Texture) 处理，只渲染屏幕可见区域 (Culling)。即使 1000 张图也能跑满 60FPS。 |
| **放大/缩小 (Zoom)** | **有虚焦感**。浏览器重绘 DOM 需要时间，快速缩放时可能会看到图片闪烁或模糊后变清晰。 | **无缝缩放**。GPU 可以在纹理级别做线性插值，缩放过程极其平滑，像原生 App。 |
| **像素级滤镜** | **如幻灯片般慢**。只能用 CSS `filter`，如果要是实时调色、亮度遮罩、边缘羽化，CPU 会满载，页面发烫。 | **即时响应 (Real-time)**。Shader (着色器) 并行计算每个像素，调色、抠图、流动特效都是毫秒级响应。 |
| **开发难度** | **低 (Low)**。像写 HTML 一样写 `<image>`，可以直接用 React 控制属性。 | **极高 (Very High)**。需要写 Shader 代码，管理内存、纹理垃圾回收、坐标系矩阵变换。 |
| **适用场景** | 白板、流程图、轻量级拼图 (Miro, FigJam)。 | 专业设计工具、游戏、重度图像编辑 (Figma, Photoshop Web)。 |

**体感差异总结**：
*   用 **SVG** 就像在操作 **PPT**，图片多了会慢，主要是“排版”。
*   用 **WebGL** 就像在玩 **3A 游戏**，无论图片多大、特效多复杂，操作都是跟手的，主要是“创作”。
