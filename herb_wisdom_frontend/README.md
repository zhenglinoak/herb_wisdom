# 本草智典（Herbal Wisdom）前端

基于 **Vue 3 + Vite** 构建的中草药智能问答系统前端应用，提供 AI 对话、知识检索、历史记录搜索等核心功能。

---

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | ^3.5.40 | 前端框架 |
| Vue Router | ^4.6.4 | 路由管理 |
| Vite | ^8.2.0 | 构建工具 |
| Element Plus | ^2.14.4 | UI 组件库 |
| Axios | ^1.19.0 | HTTP 请求 |
| Markdown-it | ^15.0.0 | Markdown 渲染 |
| Highlight.js | ^11.12.0 | 代码高亮 |
| @microsoft/fetch-event-source | ^2.0.1 | SSE 流式请求 |

---

## 项目结构

```
herb_wisdom_frontend/
├── public/                 # 静态资源
│   ├── favicon.svg
│   └── icons.svg
├── src/
│   ├── api/                # API 请求封装
│   │   ├── request.js      # Axios 拦截器与通用请求
│   │   └── sse.js          # SSE（Server-Sent Events）流式请求封装
│   ├── assets/             # 图片/图标资源
│   ├── components/         # 页面组件
│   │   ├── Login.vue       # 登录页（支持账号密码 / 邮箱验证码）
│   │   ├── Register.vue    # 注册页
│   │   ├── Chat.vue        # 核心对话页（AI 聊天、检索文档、历史管理）
│   │   └── Search.vue      # 历史记录搜索页
│   ├── router/
│   │   └── index.js        # 路由配置与导航守卫
│   ├── styles/
│   │   └── variables.css   # 全局 CSS 变量与通用样式
│   ├── utils/
│   │   └── markdown.js     # Markdown 解析器配置
│   ├── App.vue             # 根组件
│   └── main.js             # 应用入口
├── package.json
├── vite.config.js          # Vite 配置（含代理、路径别名、分包）
└── README.md
```

---

## 核心功能

### 1. 用户认证
- **账号密码登录**：支持用户名/邮箱 + 密码登录
- **邮箱验证码登录**：发送邮箱验证码进行快捷登录
- **用户注册**：表单校验，密码二次确认
- **Token 认证**：基于 JWT，登录态保存在 `sessionStorage`
- **路由守卫**：未登录用户自动跳转登录页，已登录用户禁止访问登录/注册页

### 2. AI 智能对话（Chat）
- **流式响应**：基于 SSE 实现 AI 回复的实时打字机效果
- **Markdown 渲染**：AI 回复内容支持 Markdown 语法与代码高亮
- **检索文档面板**：
  - 向量检索（Vector Search）结果展示
  - BM25 检索结果展示
  - 显示药材名称、对应病症、来源及内容摘要
- **对话管理**：
  - 新建对话
  - 切换历史对话
  - 删除对话记录
- **全局搜索**：支持在所有历史对话中搜索关键词，快速定位消息
- **关键词高亮**：当前对话内搜索并高亮匹配内容，自动滚动定位

### 3. 历史记录搜索（Search）
- 按关键词搜索所有历史提问
- 查看某条历史记录下的完整对话上下文

---

## 快速开始

### 环境要求
- Node.js >= 18
- npm 或 pnpm

### 安装依赖

```bash
npm install
```

### 开发运行

```bash
npm run dev
```

默认启动在 http://localhost:5173

### 生产构建

```bash
npm run build
```

### 预览生产包

```bash
npm run preview
```

---

## 配置说明

### 后端接口地址
在 `src/api/request.js` 和 `src/api/sse.js` 中配置：

```js
baseURL: 'http://localhost:8000'
```

### Vite 代理（开发环境）
`vite.config.js` 中已配置代理：

```js
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  },
}
```

### 路径别名
`@` 指向 `src` 目录：

```js
import request from '@/api/request'
```

---

## 路由说明

| 路径 | 组件 | 需要登录 | 说明 |
|------|------|----------|------|
| `/login` | Login.vue | 否 | 登录页 |
| `/register` | Register.vue | 否 | 注册页 |
| `/chat` | Chat.vue | 是 | AI 对话首页（默认页） |
| `/search` | Search.vue | 是 | 历史记录搜索 |
| `/*` | - | - | 重定向至 `/chat` |

---

## 设计风格

项目采用**中式草本风格**设计主题：
- 主色调：草本绿（`#4a7c59`）、茶棕（`#8b6f47`）
- 背景色：宣纸米黄（`#f5f0e8`）
- 字体：优先使用 `"Noto Sans SC"`、`"Microsoft YaHei"`
- 图标：内联 SVG，以叶子、药材为意象

---

## 后端依赖

本项目需配合后端服务使用，后端接口规范：
- 统一返回格式：`{ code: 200, data: ..., msg: ... }`
- 认证 Header：`Authorization: Bearer <token>`
- SSE 接口：`POST /chat/chat?q=...&id=...`
- 历史记录：`/history/getMenu`、`/history/historyContent/:id`、`/history/deleteHistory/:id`
- 用户相关：`/user/login`、`/user/register`、`/user/logout`

---

## 许可证

本项目为私有项目，未经授权请勿用于商业用途。
