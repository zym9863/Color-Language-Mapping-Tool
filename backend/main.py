"""
颜色-语言映射工具 API
基于Word2Vec的颜色与语言语义映射服务
"""
import os
from pathlib import Path
from contextlib import asynccontextmanager
from dataclasses import asdict

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from services.word2vec_service import get_word2vec_service
from services.color_mapper import init_color_mapper, get_color_mapper, ColorInfo


# 配置路径
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "model" / "tencent-ailab-embedding-zh-d100-v0.2.0-s.txt"
COLORS_PATH = BASE_DIR / "data" / "colors.json"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时加载模型
    print("正在初始化服务...")
    
    word2vec = get_word2vec_service()
    word2vec.load_model(str(MODEL_PATH))
    
    init_color_mapper(str(COLORS_PATH), word2vec)
    
    print("服务初始化完成！")
    yield
    # 关闭时清理资源
    print("服务关闭")


app = FastAPI(
    title="颜色-语言映射工具 API",
    description="基于Word2Vec的颜色与语言语义映射服务",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def color_info_to_dict(color: ColorInfo) -> dict:
    """将ColorInfo转换为字典"""
    return {
        "name": color.name,
        "hex": color.hex,
        "rgb": color.rgb,
        "keywords": color.keywords,
        "similarity": color.similarity
    }


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "颜色-语言映射工具 API",
        "version": "1.0.0",
        "endpoints": {
            "word_to_colors": "/api/word-to-colors?word=xxx",
            "color_to_words": "/api/color-to-words?color=xxx",
            "colors": "/api/colors"
        }
    }


@app.get("/api/colors")
async def get_colors():
    """
    获取所有支持的颜色
    
    Returns:
        颜色列表
    """
    mapper = get_color_mapper()
    colors = mapper.get_all_colors()
    return {
        "count": len(colors),
        "colors": [color_info_to_dict(c) for c in colors]
    }


@app.get("/api/word-to-colors")
async def word_to_colors(
    word: str = Query(..., description="要查询的词语"),
    top_n: int = Query(10, ge=1, le=30, description="返回的颜色数量")
):
    """
    将词语映射到最相关的颜色
    
    Args:
        word: 输入词语
        top_n: 返回的颜色数量 (1-30)
        
    Returns:
        按相似度排序的颜色列表
    """
    mapper = get_color_mapper()
    word2vec = get_word2vec_service()
    
    # 检查词语是否在词汇表中
    if not word2vec.has_word(word):
        return {
            "word": word,
            "found": False,
            "message": f"词语 '{word}' 不在词汇表中",
            "colors": []
        }
    
    colors = mapper.word_to_colors(word, top_n)
    
    return {
        "word": word,
        "found": True,
        "count": len(colors),
        "colors": [color_info_to_dict(c) for c in colors]
    }


@app.get("/api/color-to-words")
async def color_to_words(
    color: str = Query(..., description="颜色名称"),
    top_n: int = Query(20, ge=1, le=50, description="返回的词语数量")
):
    """
    将颜色映射到最相关的词语
    
    Args:
        color: 颜色名称
        top_n: 返回的词语数量 (1-50)
        
    Returns:
        相关词语列表
    """
    mapper = get_color_mapper()
    
    # 检查颜色是否存在
    all_colors = [c.name for c in mapper.get_all_colors()]
    if color not in all_colors:
        return {
            "color": color,
            "found": False,
            "message": f"颜色 '{color}' 不在颜色库中，支持的颜色: {', '.join(all_colors[:10])}...",
            "words": []
        }
    
    words = mapper.color_to_words(color, top_n)
    
    # 获取颜色信息
    color_info = None
    for c in mapper.get_all_colors():
        if c.name == color:
            color_info = color_info_to_dict(c)
            break
    
    return {
        "color": color,
        "found": True,
        "color_info": color_info,
        "count": len(words),
        "words": words
    }


@app.get("/api/similarity")
async def get_similarity(
    word1: str = Query(..., description="第一个词语"),
    word2: str = Query(..., description="第二个词语")
):
    """
    计算两个词语之间的语义相似度
    
    Args:
        word1: 第一个词语
        word2: 第二个词语
        
    Returns:
        相似度值
    """
    word2vec = get_word2vec_service()
    
    if not word2vec.has_word(word1):
        return {"error": f"词语 '{word1}' 不在词汇表中"}
    
    if not word2vec.has_word(word2):
        return {"error": f"词语 '{word2}' 不在词汇表中"}
    
    similarity = word2vec.similarity(word1, word2)
    
    return {
        "word1": word1,
        "word2": word2,
        "similarity": round(similarity, 4) if similarity else 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
