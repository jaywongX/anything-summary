<template>
  <div class="guide-container">
    <h1>{{ t('guide.title') }}</h1>
    
    <div class="guide-section">
      <h2>{{ t('guide.sections.input.title') }}</h2>
      <div class="guide-item">
        <ul>
          <li>{{ t('guide.sections.input.text') }}</li>
          <li>{{ t('guide.sections.input.url') }}</li>
          <li>{{ t('guide.sections.input.file') }}</li>
        </ul>
      </div>
      
      <h2>{{ t('guide.sections.formats.title') }}</h2>
      <div class="guide-item">
        <ul>
          <li>{{ t('guide.sections.formats.docs') }}</li>
          <li>{{ t('guide.sections.formats.images') }}</li>
          <li>{{ t('guide.sections.formats.audio') }}</li>
          <li>{{ t('guide.sections.formats.video') }}</li>
          <li>{{ t('guide.sections.formats.archive') }}</li>
        </ul>
      </div>
    </div>

    <div class="guide-section">
      <h2>{{ t('guide.sections.process.title') }}</h2>
      <ul>
        <li>{{ t('guide.sections.process.step1') }}</li>
        <li>{{ t('guide.sections.process.step2') }}</li>
        <li>{{ t('guide.sections.process.step3') }}</li>
      </ul>
    </div>

    <div class="guide-section">
      <h2>{{ t('guide.sections.results.title') }}</h2>
      <p>{{ t('guide.sections.results.description') }}</p>
      <ul>
        <li>{{ t('guide.sections.results.copy') }}</li>
        <li>{{ t('guide.sections.results.download') }}</li>
        <li>{{ t('guide.sections.results.regenerate') }}</li>
      </ul>
    </div>

    <div class="guide-section">
      <h2>{{ t('guide.sections.tips.title') }}</h2>
      <ul>
        <li>{{ t('guide.sections.tips.quality') }}</li>
        <li>{{ t('guide.sections.tips.length') }}</li>
        <li>{{ t('guide.sections.tips.files') }}</li>
      </ul>
    </div>

    <button class="back-btn" @click="router.push('/')">
      <i class="fas fa-arrow-left"></i> {{ t('app.title') }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const { t } = useI18n()
</script>

<style scoped>
.guide-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  color: #333;
}

h1 {
  text-align: center;
  color: #2196F3;
  margin-bottom: 2rem;
}

.guide-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #1976D2;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e0e0e0;
}

.guide-item {
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 4px;
}

h3 {
  color: #4CAF50;
  margin-bottom: 0.5rem;
}

ul {
  padding-left: 1.5rem;
  margin: 0.5rem 0;
}

li {
  margin: 0.5rem 0;
  line-height: 1.6;
}

.back-btn {
  display: block;
  margin: 2rem auto;
  padding: 0.75rem 2rem;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: #1976D2;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
</style> 