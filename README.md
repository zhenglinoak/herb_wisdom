# 本草智典 (Herb Wisdom) — 中医药智能问答系统

本项目是一个基于 **RAG（检索增强生成）** 架构的中医药知识库智能问答系统，采用前后端分离设计。系统能够根据用户提问，从中医药知识库中检索相关信息，并结合大语言模型生成专业、准确的回答。

---

## 项目结构

```
Project1/
├── herb_wisdom_frontend/   # 前端项目（Vue 3 + Vite）
└── herb_wisdom_backend/    # 后端项目（FastAPI + LangChain）
```

---

## 技术栈

### 前端
- **Vue 3** — 渐进式 JavaScript 框架
- **Vue Router 4** — 前端路由管理
- **Vite** — 下一代前端构建工具
- **Element Plus** — UI 组件库
- **Axios** — HTTP 客户端
- **Markdown-it + Highlight.js** — Markdown 渲染与代码高亮
- **@microsoft/fetch-event-source** — SSE 流式请求

### 后端
- **FastAPI** — 现代、高性能 Python Web 框架
- **LangChain / LangChain-Core** — 大模型应用开发框架
- **ChromaDB** — 向量数据库，用于语义检索
- **Ollama** — 本地大语言模型推理服务
- **MySQL** — 关系型数据库，存储用户与对话历史
- **Redis** — 缓存与会话管理
- **Sentence-Transformers / FlagEmbedding** — 文本嵌入模型
- **Rank-BM25 + Jieba** — 中文关键词检索
- **JWT** — 用户身份认证

---

## 核心功能

| 模块 | 功能描述 |
|------|----------|
| **用户系统** | 注册、登录、JWT 身份认证、邮箱验证码 |
| **智能问答** | 基于 RAG 的流式对话，支持多轮历史记忆 |
| **混合检索** | 向量检索（ChromaDB）+ BM25 关键词检索 + RRF 融合 + ReRanker 重排序 |
| **意图识别** | 自动识别用户问题是否与中医药相关，非医药问题直接由大模型回答 |
| **对话管理** | 新建对话、历史记录列表、删除对话、搜索对话 |
| **数据构建** | 支持从 JSON 格式的药材数据集构建向量知识库 |

---

## 前端项目

### 目录结构

```
herb_wisdom_frontend/
├── index.html
├── package.json
├── vite.config.js
└── src/
    ├── main.js              # 应用入口
    ├── App.vue              # 根组件
    ├── router/
    │   └── index.js         # 路由配置（登录/注册/聊天/搜索）
    ├── api/
    │   ├── request.js       # Axios 封装
    │   └── sse.js           # SSE 流式请求封装
    ├── components/
    │   ├── Login.vue        # 登录页
    │   ├── Register.vue     # 注册页
    │   ├── Chat.vue         # 主聊天页（含侧边栏历史记录）
    │   └── Search.vue       # 搜索页
    ├── utils/
    │   └── markdown.js      # Markdown 渲染工具
    ├── styles/
    │   └── variables.css    # CSS 变量
    └── assets/              # 静态资源
```

### 本地运行

```bash
cd herb_wisdom_frontend
npm install
npm run dev
```

默认运行在 `http://localhost:5173`

### 构建生产环境

```bash
npm run build
```

---

## 后端项目

### 目录结构

```
herb_wisdom_backend/
├── main.py                  # FastAPI 应用入口
├── requirements.txt         # Python 依赖
├── Dockerfile               # Docker 构建文件
├── .env                     # 环境变量配置
├── .env.docker              # Docker 环境变量配置
│
├── ai/                      # AI 模型加载模块
│   ├── LoadChatModel.py
│   ├── LoadEmbeddingModel.py
│   ├── LoadReRankerModel.py
│   ├── LoadIntentRecognitionModel.py
│   └── LoadChromaCon.py
│
├── chat/                    # 聊天业务模块
│   ├── controller/          # API 路由控制器
│   ├── service/             # 业务逻辑层
│   ├── dao/                 # 数据访问层
│   ├── entity/              # 数据实体
│   └── util/                # 工具类（检索、RRF、ReRanker、意图识别等）
│
├── user/                    # 用户业务模块
│   ├── controller/
│   ├── service/
│   ├── dao/
│   ├── entity/
│   └── util/
│
├── common/                  # 公共模块
│   ├── JWTUtil.py           # JWT 生成
│   ├── JWTDecode.py         # JWT 校验
│   ├── MySQLUtil.py         # MySQL 连接池
│   ├── RedisUtil.py         # Redis 连接
│   └── ResponseUtil.py      # 统一响应封装
│
├── data/                    # 数据与向量库
│   ├── BuildDatabase.py     # 构建向量数据库脚本
│   ├── CreateHistoryChoma.py
│   ├── herbal_medicine_data/# 药材知识库（ChromaDB）
│   └── chat_memory_db/      # 聊天记忆向量库（ChromaDB）
│
└── media/avatars/           # 用户头像存储
```

### 本地运行

1. **安装依赖**

```bash
cd herb_wisdom_backend
pip install -r requirements.txt
```

2. **配置环境变量**

复制 `.env` 并根据实际情况修改：

```bash
cp .env .env.local
# 编辑 .env.local，配置 MySQL、Redis、Ollama、模型路径等
```

3. **启动服务**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API 文档地址：`http://localhost:8000/docs`

### 构建向量数据库

```bash
cd herb_wisdom_backend
data/BuildDatabase.py
```

确保 `RAG_DATA_DIR` 指向包含药材 JSON 文件的目录。

### Docker 部署

```bash
cd herb_wisdom_backend
docker build -t herb-wisdom-backend .
docker run -d -p 8001:8001 --env-file .env.docker herb-wisdom-backend
```

---

## RAG 检索流程

1. **意图识别** — 判断用户问题是否与中医药相关
2. **向量检索** — 通过 ChromaDB 进行语义相似度检索（Top-K=10）
3. **BM25 检索** — 通过关键词匹配补充检索
4. **RRF 融合** — 使用 Reciprocal Rank Fusion 合并两种检索结果
5. **ReRanker 重排序** — 使用 BGE-Reranker 对融合结果精排
6. **大模型生成** — 将检索到的上下文注入 Prompt，由 LLM 生成最终回答
7. **历史记忆** — 向量检索历史记忆 + MySQL 近期对话记录，支持多轮上下文

---

## API 概览

| 路由前缀 | 说明 |
|----------|------|
| `/user` | 用户注册、登录、信息获取 |
| `/chat` | 流式对话、保存对话 |
| `/history` | 历史记录查询、删除 |
| `/media` | 静态文件（头像等） |

---

## 环境变量说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `MYSQL_HOST` / `PORT` / `USER` / `PASSWORD` / `DATABASE` | MySQL 连接配置 | `localhost`, `3306`, `root` |
| `REDIS_HOST` / `PORT` / `DB` | Redis 连接配置 | `localhost`, `6379` |
| `SECRET_KEY` / `ALGORITHM` / `ACCESS_TOKEN_EXPIRE` | JWT 配置 | `HS256`, `36000` |
| `SEND_EMAIL` / `SEND_PASSWORD` | 邮箱验证码发送配置 | — |
| `OLLAMA_BASE_URL` / `OLLAMA_MODEL` | Ollama 服务地址与模型 | `http://localhost:11434`, `qwen2.5:7b` |
| `EMBEDDING_MODEL_PATH` / `EMBEDDING_DEVICE` | 嵌入模型路径与设备 | `cuda` / `cpu` |
| `RERANKER_MODEL_PATH` / `RERANKER_DEVICE` | 重排序模型路径与设备 | `cuda` / `cpu` |
| `CHROMA_PERSIST_DIR` / `CHROMA_COLLECTION_NAME` | ChromaDB 持久化路径与集合名 | — |
| `CHAT_MEMORY_DB_PATH` | 聊天记忆向量库路径 | — |
| `RAG_DATA_DIR` | 药材 JSON 数据源目录 | — |
| `CORS_ORIGINS` | 允许的跨域前端地址 | `http://localhost:5173` |

---

## 开源协议

本项目仅供学习与研究使用。
