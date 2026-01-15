<script setup lang="ts">
import { ref, computed } from 'vue'

// API基础URL
const API_BASE = 'http://localhost:8000'

// 类型定义
interface ColorInfo {
  name: string
  hex: string
  rgb: number[]
  keywords: string[]
  similarity: number
}

interface WordResult {
  word: string
  similarity: number
}

// 状态
const activeTab = ref<'word-to-color' | 'color-to-word'>('word-to-color')
const inputWord = ref('')
const selectedColor = ref('')
const colorResults = ref<ColorInfo[]>([])
const wordResults = ref<WordResult[]>([])
const allColors = ref<ColorInfo[]>([])
const isLoading = ref(false)
const errorMessage = ref('')

// 加载所有颜色
async function loadColors() {
  try {
    const response = await fetch(`${API_BASE}/api/colors`)
    const data = await response.json()
    allColors.value = data.colors
  } catch (error) {
    console.error('加载颜色失败:', error)
  }
}

// 词语转颜色
async function searchWordToColor() {
  if (!inputWord.value.trim()) return
  
  isLoading.value = true
  errorMessage.value = ''
  colorResults.value = []
  
  try {
    const response = await fetch(
      `${API_BASE}/api/word-to-colors?word=${encodeURIComponent(inputWord.value)}&top_n=10`
    )
    const data = await response.json()
    
    if (!data.found) {
      errorMessage.value = data.message
    } else {
      colorResults.value = data.colors
    }
  } catch (error) {
    errorMessage.value = '请求失败，请确保后端服务已启动'
  } finally {
    isLoading.value = false
  }
}

// 颜色转词语
async function searchColorToWord() {
  if (!selectedColor.value) return
  
  isLoading.value = true
  errorMessage.value = ''
  wordResults.value = []
  
  try {
    const response = await fetch(
      `${API_BASE}/api/color-to-words?color=${encodeURIComponent(selectedColor.value)}&top_n=20`
    )
    const data = await response.json()
    
    if (!data.found) {
      errorMessage.value = data.message
    } else {
      wordResults.value = data.words
    }
  } catch (error) {
    errorMessage.value = '请求失败，请确保后端服务已启动'
  } finally {
    isLoading.value = false
  }
}

// 获取当前选中颜色信息
const selectedColorInfo = computed(() => {
  return allColors.value.find(c => c.name === selectedColor.value)
})

// 初始化加载颜色
loadColors()
</script>

<template>
  <div class="app-container">
    <!-- 头部 -->
    <header class="header">
      <h1 class="title">
        <span class="gradient-text">颜色-语言映射工具</span>
      </h1>
      <p class="subtitle">基于 Word2Vec 的语义关联分析</p>
    </header>

    <!-- 标签切换 -->
    <div class="tabs">
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'word-to-color' }"
        @click="activeTab = 'word-to-color'"
      >
        🔤 词语 → 颜色
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'color-to-word' }"
        @click="activeTab = 'color-to-word'"
      >
        🎨 颜色 → 词语
      </button>
    </div>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 词语转颜色 -->
      <div v-if="activeTab === 'word-to-color'" class="panel">
        <div class="input-section">
          <input 
            v-model="inputWord"
            type="text"
            placeholder="输入一个词语，如：海洋、火焰、森林..."
            class="search-input"
            @keyup.enter="searchWordToColor"
          />
          <button class="search-btn" @click="searchWordToColor" :disabled="isLoading">
            {{ isLoading ? '搜索中...' : '🔍 搜索' }}
          </button>
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div v-if="colorResults.length > 0" class="results-section">
          <h3 class="results-title">与「{{ inputWord }}」语义相关的颜色</h3>
          <div class="color-grid">
            <div 
              v-for="color in colorResults" 
              :key="color.name"
              class="color-card"
            >
              <div 
                class="color-preview" 
                :style="{ backgroundColor: color.hex }"
              ></div>
              <div class="color-info">
                <div class="color-name">{{ color.name }}</div>
                <div class="color-hex">{{ color.hex }}</div>
                <div class="similarity-bar">
                  <div 
                    class="similarity-fill" 
                    :style="{ width: (color.similarity * 100) + '%' }"
                  ></div>
                </div>
                <div class="similarity-value">相似度: {{ (color.similarity * 100).toFixed(1) }}%</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 颜色转词语 -->
      <div v-else class="panel">
        <div class="input-section">
          <select v-model="selectedColor" class="color-select">
            <option value="">选择一个颜色...</option>
            <option v-for="color in allColors" :key="color.name" :value="color.name">
              {{ color.name }}
            </option>
          </select>
          <button class="search-btn" @click="searchColorToWord" :disabled="isLoading">
            {{ isLoading ? '搜索中...' : '🔍 搜索' }}
          </button>
        </div>

        <!-- 选中颜色预览 -->
        <div v-if="selectedColorInfo" class="selected-color-preview">
          <div 
            class="big-color-swatch"
            :style="{ backgroundColor: selectedColorInfo.hex }"
          ></div>
          <div class="color-details">
            <h3>{{ selectedColorInfo.name }}</h3>
            <p>HEX: {{ selectedColorInfo.hex }}</p>
            <p>RGB: {{ selectedColorInfo.rgb.join(', ') }}</p>
            <div class="keywords">
              <span 
                v-for="keyword in selectedColorInfo.keywords" 
                :key="keyword"
                class="keyword-tag"
              >
                {{ keyword }}
              </span>
            </div>
          </div>
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div v-if="wordResults.length > 0" class="results-section">
          <h3 class="results-title">与「{{ selectedColor }}」语义相关的词语</h3>
          <div class="word-cloud">
            <span 
              v-for="(item, index) in wordResults" 
              :key="item.word"
              class="word-tag"
              :style="{ 
                fontSize: (1.5 - index * 0.05) + 'rem',
                opacity: 0.5 + item.similarity * 0.5
              }"
            >
              {{ item.word }}
              <span class="word-similarity">{{ (item.similarity * 100).toFixed(0) }}%</span>
            </span>
          </div>
        </div>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <p>Powered by Word2Vec (Tencent AI Lab) | Vue 3 + FastAPI</p>
    </footer>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: #fff;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.header {
  text-align: center;
  padding: 3rem 1rem 2rem;
}

.title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
}

.gradient-text {
  background: linear-gradient(120deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: #a0aec0;
  margin-top: 0.5rem;
  font-size: 1.1rem;
}

.tabs {
  display: flex;
  justify-content: center;
  gap: 1rem;
  padding: 0 1rem;
  margin-bottom: 2rem;
}

.tab-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  padding: 0.8rem 1.5rem;
  border-radius: 2rem;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.tab-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.tab-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.main-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.panel {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-radius: 1.5rem;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.input-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.search-input, .color-select {
  flex: 1;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  padding: 1rem 1.5rem;
  border-radius: 1rem;
  font-size: 1rem;
  outline: none;
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-input:focus, .color-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
}

.color-select option {
  background: #1a1a2e;
  color: #fff;
}

.search-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: #fff;
  padding: 1rem 2rem;
  border-radius: 1rem;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.search-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.results-section {
  margin-top: 1.5rem;
}

.results-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #e2e8f0;
}

.color-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.color-card {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 1rem;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.color-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.color-preview {
  height: 80px;
  transition: height 0.3s ease;
}

.color-card:hover .color-preview {
  height: 100px;
}

.color-info {
  padding: 1rem;
}

.color-name {
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.color-hex {
  color: #a0aec0;
  font-size: 0.9rem;
  font-family: monospace;
  margin-bottom: 0.5rem;
}

.similarity-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.similarity-fill {
  height: 100%;
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
  border-radius: 2px;
  transition: width 0.5s ease;
}

.similarity-value {
  font-size: 0.85rem;
  color: #a0aec0;
}

.selected-color-preview {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 1rem;
}

.big-color-swatch {
  width: 120px;
  height: 120px;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.color-details h3 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
}

.color-details p {
  margin: 0.25rem 0;
  color: #a0aec0;
  font-family: monospace;
}

.keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.keyword-tag {
  background: rgba(102, 126, 234, 0.3);
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.85rem;
}

.word-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.word-tag {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  cursor: default;
}

.word-tag:hover {
  transform: scale(1.1);
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.5), rgba(118, 75, 162, 0.5));
}

.word-similarity {
  font-size: 0.7em;
  color: #a0aec0;
}

.footer {
  text-align: center;
  padding: 2rem;
  color: #64748b;
  font-size: 0.9rem;
  margin-top: 2rem;
}

@media (max-width: 640px) {
  .title {
    font-size: 1.8rem;
  }
  
  .tabs {
    flex-direction: column;
  }
  
  .input-section {
    flex-direction: column;
  }
  
  .selected-color-preview {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .color-grid {
    grid-template-columns: 1fr;
  }
}
</style>
