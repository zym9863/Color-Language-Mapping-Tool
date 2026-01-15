"""
Word2Vec 服务模块
负责加载和管理Word2Vec模型，提供词向量查询功能
"""
import os
from pathlib import Path
from functools import lru_cache

import numpy as np
from gensim.models import KeyedVectors


class Word2VecService:
    """Word2Vec模型服务类"""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_model(self, model_path: str) -> None:
        """
        加载Word2Vec模型
        
        Args:
            model_path: 模型文件路径
        """
        if self._model is None:
            print(f"正在加载Word2Vec模型: {model_path}")
            # 使用text格式加载腾讯词向量
            self._model = KeyedVectors.load_word2vec_format(
                model_path, 
                binary=False,
                no_header=False
            )
            print(f"模型加载完成，词汇量: {len(self._model)}")
    
    @property
    def model(self) -> KeyedVectors:
        """获取模型实例"""
        if self._model is None:
            raise RuntimeError("模型未加载，请先调用 load_model()")
        return self._model
    
    def has_word(self, word: str) -> bool:
        """检查词语是否在词汇表中"""
        return word in self.model.key_to_index
    
    def get_vector(self, word: str) -> np.ndarray | None:
        """
        获取词语的向量表示
        
        Args:
            word: 目标词语
            
        Returns:
            词向量，如果词语不存在则返回None
        """
        if not self.has_word(word):
            return None
        return self.model[word]
    
    def similarity(self, word1: str, word2: str) -> float | None:
        """
        计算两个词语之间的余弦相似度
        
        Args:
            word1: 第一个词语
            word2: 第二个词语
            
        Returns:
            相似度值 (0-1)，如果任一词语不存在则返回None
        """
        if not self.has_word(word1) or not self.has_word(word2):
            return None
        return float(self.model.similarity(word1, word2))
    
    def most_similar(self, word: str, topn: int = 10) -> list[tuple[str, float]]:
        """
        查找与目标词语最相似的词语
        
        Args:
            word: 目标词语
            topn: 返回的词语数量
            
        Returns:
            相似词语列表，每项为 (词语, 相似度) 元组
        """
        if not self.has_word(word):
            return []
        return self.model.most_similar(word, topn=topn)


@lru_cache()
def get_word2vec_service() -> Word2VecService:
    """获取Word2Vec服务单例"""
    return Word2VecService()
