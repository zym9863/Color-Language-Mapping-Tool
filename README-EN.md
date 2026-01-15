# 🎨 Color-Language Mapping Tool

[中文](README.md) | [English](README-EN.md)

A Semantic Color-Language Mapping Tool based on Word2Vec, enabling bidirectional association analysis between words and colors.

## ✨ Features

- **🔤 Word → Color**: Input any word to find the most semantically relevant colors.
- **🎨 Color → Word**: Select a color to discover semantically associated words.
- **📊 Similarity Calculation**: Cosine similarity algorithm based on word embeddings.
- **🌈 30-Color Palette**: Includes common Chinese colors and their semantic keywords.

## 🛠️ Tech Stack

| Level | Technology |
|-------|------------|
| **Backend** | FastAPI + Python 3.12 |
| **Frontend** | Vue 3 + TypeScript + Vite |
| **Word Embeddings** | Tencent AI Lab Chinese Embedding (2M words, 100d) |
| **Package Manager** | uv (Backend) + pnpm (Frontend) |

## 📦 Project Structure

```
Color Language Mapping Tool/
├── backend/                    # Backend Service
│   ├── main.py                 # FastAPI Entry
│   ├── services/               # Core Services
│   │   ├── word2vec_service.py # Word2Vec Service
│   │   └── color_mapper.py     # Color Mapping Logic
│   ├── data/
│   │   └── colors.json         # Color Database
│   └── model/                  # Word Embedding Model
└── frontend/                   # Vue Frontend
    └── src/
        └── App.vue             # Main Interface
```

## 🚀 Quick Start

### 1. Clone the Project

```bash
git clone https://github.com/zym9863/Color-Language-Mapping-Tool.git
cd Color-Language-Mapping-Tool
```

### 2. Install Dependencies

```bash
# Install Backend Dependencies
cd backend
uv sync

# Install Frontend Dependencies
cd ../frontend
pnpm install
```

### 3. Download Word Embedding Model

Download [Tencent AI Lab Embedding](https://ai.tencent.com/ailab/nlp/zh/embedding.html) and place it in the `backend/model/` directory.

### 4. Start Services

```bash
# Start Backend (First time loading takes ~30s)
cd backend
uv run uvicorn main:app --reload --port 8000

# Start Frontend in a new terminal
cd frontend
pnpm dev
```

### 5. Access Application

- 🌐 Frontend: http://localhost:5173
- 📚 API Docs: http://localhost:8000/docs

## 📡 API Endpoints

| Endpoint | Description | Example |
|----------|-------------|---------|
| `GET /api/word-to-colors` | Word to Colors | `?word=ocean&top_n=10` |
| `GET /api/color-to-words` | Color to Words | `?color=blue&top_n=20` |
| `GET /api/colors` | Get All Colors | - |
| `GET /api/similarity` | Calculate Similarity | `?word1=ocean&word2=blue` |

## 🎯 Usage Examples

### Word → Color

Input "Ocean" returns: Blue, Dark Blue, Cyan, Sky Blue, and other semantically related colors.

### Color → Word

Select "Red" returns: Passion, Fire, Love, Danger, and other related words.

## 📄 License

MIT License
