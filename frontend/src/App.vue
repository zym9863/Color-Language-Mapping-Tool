<script setup lang="ts">
import { ref, computed } from 'vue'

// API Base URL
const API_BASE = 'http://localhost:8000'

// Types
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

// State
const activeTab = ref<'word-to-color' | 'color-to-word'>('word-to-color')
const inputWord = ref('')
const selectedColor = ref('')
const colorResults = ref<ColorInfo[]>([])
const wordResults = ref<WordResult[]>([])
const allColors = ref<ColorInfo[]>([])
const isLoading = ref(false)
const errorMessage = ref('')

// Load colors on mount
async function loadColors() {
  try {
    const response = await fetch(`${API_BASE}/api/colors`)
    const data = await response.json()
    allColors.value = data.colors
  } catch (error) {
    console.error('Failed to load colors:', error)
  }
}

// Word -> Color
async function searchWordToColor() {
  if (!inputWord.value.trim()) return
  
  isLoading.value = true
  errorMessage.value = ''
  colorResults.value = []
  
  try {
    const response = await fetch(
      `${API_BASE}/api/word-to-colors?word=${encodeURIComponent(inputWord.value)}&top_n=12`
    )
    const data = await response.json()
    
    if (!data.found) {
      errorMessage.value = data.message
    } else {
      colorResults.value = data.colors
    }
  } catch (error) {
    errorMessage.value = 'CONNECTION_ERROR: Backend offline.'
  } finally {
    isLoading.value = false
  }
}

// Color -> Word
async function searchColorToWord() {
  if (!selectedColor.value) return
  
  isLoading.value = true
  errorMessage.value = ''
  wordResults.value = []
  
  try {
    const response = await fetch(
      `${API_BASE}/api/color-to-words?color=${encodeURIComponent(selectedColor.value)}&top_n=30`
    )
    const data = await response.json()
    
    if (!data.found) {
      errorMessage.value = data.message
    } else {
      wordResults.value = data.words
    }
  } catch (error) {
    errorMessage.value = 'CONNECTION_ERROR: Backend offline.'
  } finally {
    isLoading.value = false
  }
}

const selectedColorInfo = computed(() => {
  return allColors.value.find(c => c.name === selectedColor.value)
})

loadColors()
</script>

<template>
  <div class="void-interface">
    <div class="noise-decoration"></div>
    
    <header class="cyber-header">
      <div class="logo-area">
        <h1 class="glitch-title u-display" data-text="CHROMA_MAP">CHROMA_MAP</h1>
        <div class="subtitle u-mono">>> SEMANTIC_COLOR_BRIDGE_V1.0</div>
      </div>
      <div class="status-indicator">
        <span class="status-dot"></span>
        <span class="u-mono">SYSTEM_ONLINE</span>
      </div>
    </header>

    <main class="cyber-main">
      <!-- Mode Switcher -->
      <div class="mode-selector">
        <button 
          class="mode-btn u-mono" 
          :class="{ active: activeTab === 'word-to-color' }"
          @click="activeTab = 'word-to-color'"
        >
          [A] INPUT_WORD
        </button>
        <button 
          class="mode-btn u-mono" 
          :class="{ active: activeTab === 'color-to-word' }"
          @click="activeTab = 'color-to-word'"
        >
          [B] SELECT_COLOR
        </button>
      </div>

      <!-- Word to Color View -->
      <section v-if="activeTab === 'word-to-color'" class="view-panel">
        <div class="search-matrix">
          <div class="input-wrapper">
            <span class="prompt u-mono">></span>
            <input 
              v-model="inputWord"
              type="text"
              placeholder="ENTER_KEYWORD..."
              class="cyber-input u-display"
              @keyup.enter="searchWordToColor"
            />
            <button class="cyber-action-btn u-mono" @click="searchWordToColor" :disabled="isLoading">
              {{ isLoading ? 'PROCESSING...' : 'EXECUTE' }}
            </button>
          </div>
        </div>

        <div v-if="errorMessage" class="error-terminal u-mono">
          <span class="error-prefix">ERROR:</span> {{ errorMessage }}
        </div>

        <div v-if="colorResults.length > 0" class="results-grid">
          <div class="grid-header u-mono">
            RESULTS_FOUND: {{ colorResults.length }} // KEYWORD: "{{ inputWord }}"
          </div>
          <div class="cards-container">
            <div 
              v-for="color in colorResults" 
              :key="color.name"
              class="color-unit"
              :style="{ '--unit-color': color.hex }"
            >
              <div class="color-swatch"></div>
              <div class="unit-data">
                <div class="unit-header">
                  <span class="unit-name u-display">{{ color.name }}</span>
                  <span class="unit-hex u-mono">{{ color.hex }}</span>
                </div>
                <div class="scan-bar-container">
                  <div class="scan-bar" :style="{ width: (color.similarity * 100) + '%' }"></div>
                </div>
                <div class="unit-metrics u-mono">
                  <span>MATCH_RATE</span>
                  <span class="highlight">{{ (color.similarity * 100).toFixed(1) }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Color to Word View -->
      <section v-else class="view-panel">
        <div class="search-matrix">
           <div class="input-wrapper select-wrapper">
            <span class="prompt u-mono">></span>
            <select v-model="selectedColor" class="cyber-select u-mono">
              <option value="">SELECT_CHROMATIC_VALUE...</option>
              <option v-for="color in allColors" :key="color.name" :value="color.name">
                {{ color.name }}
              </option>
            </select>
            <button class="cyber-action-btn u-mono" @click="searchColorToWord" :disabled="isLoading">
              {{ isLoading ? 'PROCESSING...' : 'ANALYZE' }}
            </button>
          </div>
        </div>

        <div v-if="selectedColorInfo" class="color-analysis-panel">
           <div class="analysis-preview" :style="{ backgroundColor: selectedColorInfo.hex }">
             <div class="preview-overlay u-mono">
               <div>R:{{ selectedColorInfo.rgb[0] }}</div>
               <div>G:{{ selectedColorInfo.rgb[1] }}</div>
               <div>B:{{ selectedColorInfo.rgb[2] }}</div>
             </div>
           </div>
           <div class="analysis-data">
             <h2 class="u-display">{{ selectedColorInfo.name }}</h2>
             <div class="tags-cloud">
               <span v-for="tag in selectedColorInfo.keywords" :key="tag" class="tag u-mono">#{{ tag }}</span>
             </div>
           </div>
        </div>

        <div v-if="errorMessage" class="error-terminal u-mono">
          <span class="error-prefix">ERROR:</span> {{ errorMessage }}
        </div>

        <div v-if="wordResults.length > 0" class="word-stream">
          <div class="grid-header u-mono">
             ASSOCIATED_CONCEPTS_DETECTED //
          </div>
          <div class="stream-container">
            <span 
              v-for="(item, index) in wordResults" 
              :key="item.word"
              class="data-token u-mono"
              :style="{ 
                '--opacity': 0.4 + item.similarity * 0.6,
                '--scale': 0.9 + item.similarity * 0.3
              }"
            >
              <span class="token-text">{{ item.word }}</span>
              <span class="token-value">_{{ (item.similarity * 100).toFixed(0) }}</span>
            </span>
          </div>
        </div>
      </section>
    </main>

    <footer class="cyber-footer u-mono">
      <div class="footer-line">VOID_SYSTEMS // TENCENT_AI_LAB_EMBEDDINGS</div>
    </footer>
  </div>
</template>

<style scoped>
/* Layout Structure */
.void-interface {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-sm);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Header */
.cyber-header {
  padding: var(--space-lg) 0 var(--space-md);
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  border-bottom: 1px solid var(--c-border);
  margin-bottom: var(--space-md);
}

.glitch-title {
  font-size: 3.5rem;
  line-height: 1;
  background: linear-gradient(to right, #fff, #999);
  -webkit-background-clip: text;
  color: transparent;
  position: relative;
}

.subtitle {
  color: var(--c-accent-cyan);
  margin-top: var(--space-xs);
  font-size: 0.9rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: var(--c-text-muted);
}

.status-dot {
  width: 8px;
  height: 8px;
  background-color: var(--c-accent-lime);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--c-accent-lime);
  animation: pulse 2s infinite;
}

/* Mode Selector */
.mode-selector {
  display: flex;
  gap: var(--space-sm);
  margin-bottom: var(--space-lg);
}

.mode-btn {
  background: transparent;
  border: 1px solid var(--c-border);
  color: var(--c-text-muted);
  padding: 1rem 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  flex: 1;
  text-align: center;
  font-size: 0.9rem;
  position: relative;
  overflow: hidden;
}

.mode-btn:hover {
  border-color: var(--c-text-main);
  color: var(--c-text-main);
}

.mode-btn.active {
  background: var(--c-surface-hover);
  border-color: var(--c-accent-cyan);
  color: var(--c-accent-cyan);
  box-shadow: inset 0 0 15px rgba(0, 243, 255, 0.1);
}

.mode-btn.active::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 4px; height: 100%;
  background: var(--c-accent-cyan);
}

/* Search Matrix */
.search-matrix {
  margin-bottom: var(--space-lg);
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  padding: 0.5rem;
  transition: border-color 0.3s ease;
}

.input-wrapper:focus-within {
  border-color: var(--c-accent-magenta);
  box-shadow: var(--glow-magenta);
}

.prompt {
  color: var(--c-text-muted);
  font-size: 1.5rem;
  padding-left: 1rem;
}

.cyber-input, .cyber-select {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--c-text-main);
  font-size: 1.5rem;
  padding: 1rem;
  outline: none;
  text-transform: uppercase;
  width: 100%;
}

.cyber-select {
  cursor: pointer;
  font-size: 1.2rem;
}

.cyber-select option {
  background: var(--c-surface);
  color: var(--c-text-main);
}

.cyber-action-btn {
  background: var(--c-text-main);
  color: var(--c-void);
  border: none;
  padding: 1rem 2rem;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.1s;
}

.cyber-action-btn:hover:not(:disabled) {
  background: var(--c-accent-cyan);
  transform: translateX(-2px) translateY(-2px);
  box-shadow: 4px 4px 0 rgba(255, 255, 255, 0.2);
}

.cyber-action-btn:disabled {
  background: var(--c-text-muted);
  cursor: not-allowed;
}

/* Color Cards Layout */
.grid-header {
  border-bottom: 1px solid var(--c-border);
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
  color: var(--c-text-muted);
  font-size: 0.8rem;
  letter-spacing: 1px;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.5rem;
}

.color-unit {
  border: 1px solid var(--c-border);
  background: var(--c-surface);
  transition: all 0.3s ease;
  position: relative;
}

.color-unit:hover {
  border-color: var(--unit-color);
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.5);
}

.color-swatch {
  height: 120px;
  background-color: var(--unit-color);
  border-bottom: 1px solid var(--c-border);
  position: relative;
}

.color-unit:hover .color-swatch::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.2) 45%, transparent 50%);
  background-size: 200% 200%;
  animation: shine 1s;
}

.unit-data {
  padding: 1rem;
}

.unit-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 1rem;
}

.unit-name {
  font-size: 1rem;
  letter-spacing: -0.02em;
}

.unit-hex {
  font-size: 0.7rem;
  color: var(--c-text-muted);
}

.scan-bar-container {
  height: 2px;
  background: #222;
  margin-bottom: 0.5rem;
  width: 100%;
}

.scan-bar {
  height: 100%;
  background: var(--c-accent-cyan);
  box-shadow: 0 0 8px var(--c-accent-cyan);
}

.unit-metrics {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: var(--c-text-muted);
}

.unit-metrics .highlight {
  color: var(--c-text-main);
  font-weight: bold;
}

/* Color Analysis Panel */
.color-analysis-panel {
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
  border: 1px solid var(--c-border);
  padding: 1.5rem;
  background: linear-gradient(90deg, rgba(255,255,255,0.02) 0%, transparent 100%);
}

.analysis-preview {
  height: 150px;
  width: 100%;
  border: 1px solid var(--c-border);
  position: relative;
}

.preview-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0,0,0,0.7);
  padding: 4px;
  font-size: 0.7rem;
  display: flex;
  justify-content: space-around;
  backdrop-filter: blur(4px);
}

.analysis-data h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: var(--c-text-main);
}

.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  border: 1px solid var(--c-border);
  padding: 4px 8px;
  font-size: 0.8rem;
  color: var(--c-text-muted);
  transition: color 0.2s;
}

.tag:hover {
  border-color: var(--c-accent-magenta);
  color: var(--c-accent-magenta);
}

/* Word Stream */
.stream-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.data-token {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  padding: 0.5rem 1rem;
  opacity: var(--opacity);
  transform: scale(var(--scale));
  transition: all 0.3s ease;
  cursor: crosshair;
}

.data-token:hover {
  border-color: var(--c-accent-lime);
  color: var(--c-accent-lime);
  opacity: 1 !important;
  transform: scale(1.1);
  box-shadow: 0 0 15px rgba(204, 255, 0, 0.2);
  z-index: 10;
}

.token-value {
  font-size: 0.7em;
  color: var(--c-text-muted);
}

/* Error */
.error-terminal {
  border-left: 2px solid #ff003c;
  background: rgba(255, 0, 60, 0.1);
  padding: 1rem;
  margin-top: 1rem;
  color: #ff003c;
}

/* Footer */
.cyber-footer {
  margin-top: auto;
  padding: 2rem 0;
  text-align: center;
  border-top: 1px solid var(--c-border);
  color: var(--c-text-muted);
  font-size: 0.7rem;
}

/* Responsive */
@media (max-width: 768px) {
  .cyber-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .glitch-title {
    font-size: 2rem;
  }

  .color-analysis-panel {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .analysis-preview {
    margin: 0 auto;
    width: 100px;
    height: 100px;
  }
  
  .tags-cloud {
    justify-content: center;
  }
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(204, 255, 0, 0.4); }
  70% { box-shadow: 0 0 0 6px rgba(204, 255, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(204, 255, 0, 0); }
}

@keyframes shine {
  0% { transform: translateX(-100%) translateY(-100%); }
  100% { transform: translateX(100%) translateY(100%); }
}
</style>
