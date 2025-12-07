<script setup>
import { ref } from 'vue'

const files = ref([])
const results = ref([])
const loading = ref(false)
const dragover = ref(false)

const API_URL = 'http://localhost:8000'

function handleFiles(event) {
  const newFiles = event.target.files || event.dataTransfer.files
  files.value = [...files.value, ...Array.from(newFiles)]
  dragover.value = false
}

function removeFile(index) {
  files.value.splice(index, 1)
}

function clearAll() {
  files.value = []
  results.value = []
}

async function predict() {
  if (files.value.length === 0) return

  loading.value = true
  results.value = []

  const formData = new FormData()
  files.value.forEach(file => formData.append('files', file))

  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      body: formData
    })
    const data = await response.json()
    results.value = data.results
  } catch (error) {
    console.error('Erreur:', error)
    alert('Erreur lors de la prédiction')
  } finally {
    loading.value = false
  }
}

function getPreviewUrl(file) {
  return URL.createObjectURL(file)
}

function formatConfidence(confidence) {
  return (confidence * 100).toFixed(1)
}
</script>

<template>
  <div class="app">
    <div class="hero">
      <div class="upload-zone">
        <div
          class="dropzone"
          :class="{ dragover, 'has-files': files.length > 0 }"
          @dragover.prevent="dragover = true"
          @dragleave="dragover = false"
          @drop.prevent="handleFiles"
        >
          <input
            type="file"
            accept="image/*"
            multiple
            @change="handleFiles"
            id="file-input"
          />

          <div v-if="files.length === 0" class="dropzone-content">
            <label for="file-input">
              <span class="dropzone-icon">+</span>
              <span>Ajouter des images</span>
            </label>
          </div>

          <div v-else class="files-preview">
            <div class="files-grid">
              <div v-for="(file, index) in files" :key="index" class="file-card">
                <img :src="getPreviewUrl(file)" :alt="file.name" />
                <button class="btn-remove" @click.stop="removeFile(index)">×</button>
              </div>
              <label for="file-input" class="add-more">+</label>
            </div>
          </div>
        </div>

        <div v-if="files.length > 0" class="actions">
          <button class="btn-clear" @click="clearAll">Effacer</button>
          <button class="btn-predict" @click="predict" :disabled="loading">
            {{ loading ? 'Analyse...' : 'Identifier !' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="results.length > 0" class="results">
      <h2>Résultats</h2>
      <div class="results-grid">
        <div v-for="result in results" :key="result.filename" class="result-card">
          <img
            :src="getPreviewUrl(files.find(f => f.name === result.filename))"
            :alt="result.filename"
          />
          <div class="predictions">
            <div
              v-for="(pred, i) in result.predictions"
              :key="pred.name"
              class="prediction"
              :class="{ top: i === 0 }"
            >
              <span class="rank">{{ i + 1 }}</span>
              <span class="name">{{ pred.name }}</span>
              <span class="confidence">{{ formatConfidence(pred.confidence) }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #0a0a0a;
  min-height: 100vh;
  color: #fff;
}

.app {
  min-height: 100vh;
}

.hero {
  height: 100vh;
  background: url('/background.png') center center / cover no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.upload-zone {
  position: absolute;
  left: 8%;
  top: 50%;
  transform: translateY(-50%);
  width: 340px;
}

.dropzone {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  border: 3px solid transparent;
}

.dropzone:hover,
.dropzone.dragover {
  border-color: #feca57;
  box-shadow: 0 0 30px rgba(254, 202, 87, 0.3);
}

.dropzone.has-files {
  padding: 1rem;
}

.dropzone input {
  display: none;
}

.dropzone-content {
  text-align: center;
}

.dropzone-content label {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: #333;
  font-size: 1.1rem;
  font-weight: 500;
}

.dropzone-icon {
  font-size: 4rem;
  font-weight: bold;
  color: #1a1a2e;
}

.files-preview {
  width: 100%;
}

.files-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
}

.file-card {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
}

.file-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.btn-remove {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 20px;
  height: 20px;
  border: none;
  background: rgba(0, 0, 0, 0.7);
  color: #fff;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
  line-height: 1;
}

.btn-remove:hover {
  background: #ff6b6b;
}

.add-more {
  aspect-ratio: 1;
  border-radius: 8px;
  background: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #999;
  cursor: pointer;
  transition: all 0.2s;
}

.add-more:hover {
  background: #ddd;
  color: #666;
}

.actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn-clear {
  flex: 1;
  padding: 0.75rem;
  background: #fff;
  border: 2px solid #ddd;
  color: #666;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-clear:hover {
  border-color: #ff6b6b;
  color: #ff6b6b;
}

.btn-predict {
  flex: 2;
  padding: 0.75rem;
  background: linear-gradient(90deg, #ff6b6b, #feca57);
  border: none;
  border-radius: 8px;
  color: #1a1a2e;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s, opacity 0.2s;
}

.btn-predict:hover:not(:disabled) {
  transform: translateY(-2px);
}

.btn-predict:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.results {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 3rem 2rem;
}

.results h2 {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.result-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  overflow: hidden;
}

.result-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.predictions {
  padding: 1rem;
}

.prediction {
  display: flex;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.prediction:last-child {
  border-bottom: none;
}

.prediction.top {
  font-weight: 600;
}

.prediction.top .name {
  color: #feca57;
}

.rank {
  width: 24px;
  height: 24px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  margin-right: 0.75rem;
}

.prediction.top .rank {
  background: #feca57;
  color: #1a1a2e;
}

.name {
  flex: 1;
}

.confidence {
  color: #888;
  font-size: 0.9rem;
}

.prediction.top .confidence {
  color: #fff;
}
</style>
