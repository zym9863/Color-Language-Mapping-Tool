"""
颜色映射服务模块
实现词语与颜色之间的语义映射
"""
import json
from pathlib import Path
from dataclasses import dataclass, field

import numpy as np

from .word2vec_service import Word2VecService, get_word2vec_service


@dataclass
class ColorInfo:
    """颜色信息数据类"""
    name: str
    hex: str
    rgb: list[int]
    keywords: list[str] = field(default_factory=list)
    similarity: float = 0.0


class ColorMapper:
    """颜色映射服务类"""
    
    def __init__(self, colors_path: str, word2vec_service: Word2VecService):
        """
        初始化颜色映射器
        
        Args:
            colors_path: 颜色数据文件路径
            word2vec_service: Word2Vec服务实例
        """
        self.word2vec = word2vec_service
        self.colors: dict[str, dict] = {}
        self._load_colors(colors_path)
    
    def _load_colors(self, path: str) -> None:
        """加载颜色数据"""
        with open(path, 'r', encoding='utf-8') as f:
            self.colors = json.load(f)
        print(f"已加载 {len(self.colors)} 种颜色")
    
    def get_all_colors(self) -> list[ColorInfo]:
        """获取所有颜色信息"""
        return [
            ColorInfo(
                name=name,
                hex=info['hex'],
                rgb=info['rgb'],
                keywords=info.get('keywords', [])
            )
            for name, info in self.colors.items()
        ]
    
    def word_to_colors(self, word: str, top_n: int = 10) -> list[ColorInfo]:
        """
        将词语映射到最相关的颜色
        
        算法逻辑:
        1. 计算输入词与每个颜色名称的直接相似度
        2. 计算输入词与每个颜色关键词的相似度，取最高值
        3. 综合两者得到最终相似度
        
        Args:
            word: 输入词语
            top_n: 返回的颜色数量
            
        Returns:
            按相似度排序的颜色列表
        """
        if not self.word2vec.has_word(word):
            return []
        
        results = []
        word_vector = self.word2vec.get_vector(word)
        
        for color_name, color_info in self.colors.items():
            # 计算与颜色名称的相似度
            name_similarity = 0.0
            if self.word2vec.has_word(color_name):
                sim = self.word2vec.similarity(word, color_name)
                if sim is not None:
                    name_similarity = sim
            
            # 计算与颜色关键词的相似度
            keyword_similarity = 0.0
            keywords = color_info.get('keywords', [])
            for keyword in keywords:
                if self.word2vec.has_word(keyword):
                    sim = self.word2vec.similarity(word, keyword)
                    if sim is not None:
                        keyword_similarity = max(keyword_similarity, sim)
            
            # 综合相似度: 颜色名称权重0.4 + 关键词权重0.6
            final_similarity = name_similarity * 0.4 + keyword_similarity * 0.6
            
            if final_similarity > 0:
                results.append(ColorInfo(
                    name=color_name,
                    hex=color_info['hex'],
                    rgb=color_info['rgb'],
                    keywords=keywords,
                    similarity=round(final_similarity, 4)
                ))
        
        # 按相似度降序排序
        results.sort(key=lambda x: x.similarity, reverse=True)
        return results[:top_n]
    
    def color_to_words(self, color_name: str, top_n: int = 20) -> list[dict]:
        """
        将颜色映射到最相关的词语
        
        Args:
            color_name: 颜色名称
            top_n: 返回的词语数量
            
        Returns:
            相关词语列表，包含词语和相似度
        """
        if color_name not in self.colors:
            return []
        
        if not self.word2vec.has_word(color_name):
            # 如果颜色名不在词汇表中，使用关键词
            keywords = self.colors[color_name].get('keywords', [])
            all_similar = []
            for keyword in keywords:
                if self.word2vec.has_word(keyword):
                    similar = self.word2vec.most_similar(keyword, topn=top_n)
                    all_similar.extend(similar)
            
            # 去重并排序
            word_dict = {}
            for word, sim in all_similar:
                if word not in word_dict or sim > word_dict[word]:
                    word_dict[word] = sim
            
            results = [{'word': w, 'similarity': round(s, 4)} 
                      for w, s in sorted(word_dict.items(), 
                                        key=lambda x: x[1], 
                                        reverse=True)[:top_n]]
            return results
        
        # 直接使用颜色名查找相似词
        similar_words = self.word2vec.most_similar(color_name, topn=top_n)
        return [{'word': word, 'similarity': round(sim, 4)} 
                for word, sim in similar_words]


_color_mapper: ColorMapper | None = None


def get_color_mapper() -> ColorMapper:
    """获取颜色映射器单例"""
    global _color_mapper
    if _color_mapper is None:
        raise RuntimeError("颜色映射器未初始化")
    return _color_mapper


def init_color_mapper(colors_path: str, word2vec_service: Word2VecService) -> ColorMapper:
    """初始化颜色映射器"""
    global _color_mapper
    _color_mapper = ColorMapper(colors_path, word2vec_service)
    return _color_mapper
