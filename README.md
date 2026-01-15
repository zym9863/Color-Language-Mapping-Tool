# 🎨 颜色-语言映射工具

[中文](README.md) | [English](README-EN.md)

基于 Word2Vec 的颜色与语言语义映射工具，实现词语与颜色之间的双向关联分析。

## ✨ 功能特性

- **🔤 词语 → 颜色**: 输入任意词语，查找语义最相关的颜色
- **🎨 颜色 → 词语**: 选择颜色，发现与之语义关联的词语
- **📊 相似度计算**: 基于词向量的余弦相似度算法
- **🌈 30种颜色库**: 包含常见中文颜色及其语义关键词

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| **后端** | FastAPI + Python 3.12 |
| **前端** | Vue 3 + TypeScript + Vite |
| **词向量** | Tencent AI Lab 中文词向量 (200万词, 100维) |
| **包管理** | uv (后端) + pnpm (前端) |

## 📦 项目结构

```
Color Language Mapping Tool/
├── backend/                    # 后端服务
│   ├── main.py                 # FastAPI 入口
│   ├── services/               # 核心服务
│   │   ├── word2vec_service.py # Word2Vec 模型服务
│   │   └── color_mapper.py     # 颜色映射逻辑
│   ├── data/
│   │   └── colors.json         # 颜色数据库
│   └── model/                  # 词向量模型
└── frontend/                   # Vue 前端
    └── src/
        └── App.vue             # 主界面
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/zym9863/Color-Language-Mapping-Tool.git
cd Color-Language-Mapping-Tool
```

### 2. 安装依赖

```bash
# 安装后端依赖
cd backend
uv sync

# 安装前端依赖
cd ../frontend
pnpm install
```

### 3. 下载词向量模型

将 [腾讯AI Lab词向量](https://ai.tencent.com/ailab/nlp/zh/embedding.html) 下载并放置到 `backend/model/` 目录。

### 4. 启动服务

```bash
# 启动后端 (首次加载模型约30秒)
cd backend
uv run uvicorn main:app --reload --port 8000

# 新终端启动前端
cd frontend
pnpm dev
```

### 5. 访问应用

- 🌐 前端界面: http://localhost:5173
- 📚 API文档: http://localhost:8000/docs

## 📡 API 接口

| 端点 | 说明 | 示例 |
|------|------|------|
| `GET /api/word-to-colors` | 词语转颜色 | `?word=海洋&top_n=10` |
| `GET /api/color-to-words` | 颜色转词语 | `?color=蓝色&top_n=20` |
| `GET /api/colors` | 获取所有颜色 | - |
| `GET /api/similarity` | 计算相似度 | `?word1=海洋&word2=蓝色` |

## 🎯 使用示例

### 词语 → 颜色

输入 "海洋" 会返回：蓝色、深蓝色、青色、天蓝色等语义相关的颜色。

### 颜色 → 词语

选择 "红色" 会返回：热情、火焰、爱情、危险等相关词语。

## 📄 License

MIT License
