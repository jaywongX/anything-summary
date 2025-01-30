<template>
  <div class="page-container">
    <!-- 顶部区域 -->
    <div class="top-section">
      <!-- 左侧标题和描述 -->
      <div class="product-intro">
        <h1>
          <span class="logo">🎯</span> 
          {{ t('app.title') }}
          <span class="subtitle">{{ t('app.subtitle') }}</span>
        </h1>
      </div>

      <!-- 右侧按钮组 -->
      <div class="top-buttons">
        <!-- 语言切换按钮 -->
        <button class="lang-btn" @click="toggleLanguage">
          {{ currentLocale === 'zh' ? 'EN' : '中' }}
        </button>
        <button class="guide-btn" @click="goToGuide">
          <i class="fas fa-question-circle"></i> {{ t('app.guide') }}
        </button>
        <button class="contact-btn" @click="showContactInfo">
          <i class="fas fa-envelope"></i> {{ t('app.contact') }}
        </button>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧输入区域 -->
      <div class="input-section">
        <!-- 功能类型指示器 -->
        <div class="feature-list">
          <span class="feature">📝 {{ t('features.text') }}</span>
          <span class="feature">🔗 {{ t('features.webpage') }}</span>
          <span class="feature">📄 {{ t('features.document') }}</span>
          <span class="feature">🎵 {{ t('features.audio') }}</span>
          <span class="feature">🎬 {{ t('features.video') }}</span>
          <span class="feature">📦 {{ t('features.archive') }}</span>
        </div>
        
        <!-- URL输入区 -->
        <div class="url-inputs">
          <div v-for="(url, index) in urls" :key="'url-'+index" class="url-input-group">
            <div class="input-wrapper">
              <input 
                v-model="urls[index]" 
                type="text" 
                class="form-input"
                :placeholder="t('input.url.placeholder')"
              >
              <button @click="removeUrl(index)" class="remove-btn" v-if="urls.length > 1" :title="t('input.delete')">
                ×
              </button>
            </div>
          </div>
          <button @click="addUrl" class="add-btn">
            <i class="fas fa-plus"></i> {{ t('input.url.add') }}
          </button>
        </div>

        <!-- 文本输入区 -->
        <div class="text-inputs">
          <div v-for="(text, index) in texts" :key="'text-'+index" class="text-input-group">
            <div class="input-wrapper">
              <textarea 
                v-model="texts[index]" 
                class="form-input"
                :placeholder="t('input.text.placeholder')"
                rows="3"
              ></textarea>
              <button @click="removeText(index)" class="remove-btn" v-if="texts.length > 1" :title="t('input.delete')">
                ×
              </button>
            </div>
          </div>
          <button @click="addText" class="add-btn">
            <i class="fas fa-plus"></i> {{ t('input.text.add') }}
          </button>
        </div>

        <!-- 文件上传区域 -->
        <div class="file-upload">
          <div id="uppy"></div>
        </div>

        <button @click="handleSubmit" class="submit-btn" :disabled="!hasInput">
          {{ t('actions.submit') }}
        </button>
      </div>

      <!-- 右侧输出区域 -->
      <div class="output-section">
        <div class="result-container">
          <div v-if="loading" class="loading">
            {{ t('status.processing') }}
          </div>
          <div v-else-if="summary" class="summary-result">
            <p>{{ summary }}</p>
            <div class="action-buttons">
              <button @click="copyToClipboard" class="action-btn">
                <i class="fas fa-copy"></i> {{ t('actions.copy') }}
              </button>
              <button @click="downloadSummary" class="action-btn">
                <i class="fas fa-download"></i> {{ t('actions.download') }}
              </button>
            </div>
          </div>
          <div v-else class="empty-state">
            {{ t('status.empty') }}
          </div>
        </div>
      </div>
    </div>

    <!-- 添加结果显示区域的样式 -->
    <div v-if="summary" class="result-section">
      <h2>处理结果</h2>
      <div class="summary-content">
        <pre>{{ summary }}</pre>
      </div>
    </div>
  </div>

  <!-- 联系方式弹窗 -->
  <div v-if="showContact" class="contact-modal">
    <div class="modal-content">
      <h3>{{ t('contact.title') }}</h3>
      <div class="contact-info">
        <p><i class="fas fa-envelope"></i> {{ t('contact.email') }}</p>
        <p><i class="fab fa-github"></i> {{ t('contact.github') }}</p>
        <p><i class="fab fa-weixin"></i> {{ t('contact.wechat') }}</p>
      </div>
      <div class="contact-footer">
        <p class="feedback-text">{{ t('contact.feedback') }}</p>
        <button class="close-btn" @click="showContact = false">
          {{ t('contact.close') }}
        </button>
      </div>
    </div>
  </div>

  <!-- 复制成功提示 -->
  <div v-if="showCopyTip" class="copy-tip">
    {{ t('messages.copySuccess') }}
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import Uppy from '@uppy/core'
import Dashboard from '@uppy/dashboard'
import '@uppy/core/dist/style.css'
import '@uppy/dashboard/dist/style.css'
import { mockSummaryService } from '../mock/summaryService'
import { config } from '../config.ts'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()

const currentLocale = computed(() => locale.value)

const toggleLanguage = () => {
  locale.value = locale.value === 'zh' ? 'en' : 'zh'
  localStorage.setItem('locale', locale.value)
}

const uppy = ref(null)
const summary = ref('')
const isProcessing = ref(false)
const urlInput = ref('')
const urls = ref([''])
const texts = ref([''])
const loading = ref(false)
const showCopyTip = ref(false)
const router = useRouter()
const showContact = ref(false)
const uploadedFiles = ref([])

// 计算是否有文件上传
const hasFiles = computed(() => {
  return uppy.value && uppy.value.getFiles().length > 0
})

// 格式化后的摘要内容
const formattedSummary = computed(() => {
  if (!summary.value) return ''
  // 将换行符转换为HTML换行，保持格式
  return summary.value.replace(/\n/g, '<br>')
})

// 修改计算属性，检查是否有任何输入
const hasInput = computed(() => {
  // 检查URL输入
  const hasUrls = urls.value.some(url => {
    const trimmedUrl = url.trim()
    return trimmedUrl !== '' && isValidUrl(trimmedUrl)
  })
  
  // 检查文本输入
  const hasTexts = texts.value.some(text => text.trim() !== '')
  
  // 检查文件上传 - 使用响应式引用
  const hasUploadedFiles = uploadedFiles.value.length > 0
  
  return hasUrls || hasTexts || hasUploadedFiles
})

// 允许的文件类型配置
const allowedFileTypes = {
  // 文档类型
  'application/pdf': '.pdf',
  'application/msword': '.doc',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
  'text/plain': '.txt',
  
  // 图片类型
  'image/jpeg': '.jpg, .jpeg',
  'image/png': '.png',
  'image/gif': '.gif',
  'image/webp': '.webp',
  'image/bmp': '.bmp',
  'image/svg+xml': '.svg',
  
  // 音频类型
  'audio/mpeg': '.mp3',
  'audio/wav': '.wav',
  'audio/ogg': '.ogg',
  'audio/aac': '.aac',
  'audio/m4a': '.m4a',
  'audio/flac': '.flac',
  
  // 视频类型
  'video/mp4': '.mp4',
  'video/webm': '.webm',
  'video/ogg': '.ogv',
  'video/quicktime': '.mov',
  'video/x-msvideo': '.avi',
  'video/x-matroska': '.mkv',
  
  // 压缩包类型
  'application/zip': '.zip',
  'application/x-gzip': '.gz',
  'application/x-tar': '.tar',
  'application/x-rar-compressed': '.rar',
  'application/x-7z-compressed': '.7z'
}

// 复制结果
const copyResult = async () => {
  try {
    await navigator.clipboard.writeText(summary.value)
    alert('已复制到剪贴板')
  } catch (err) {
    console.error('复制失败:', err)
    alert('复制失败，请手动复制')
  }
}

// 分享结果
const shareResult = async () => {
  try {
    if (navigator.share) {
      await navigator.share({
        title: 'AnythingSummary - 内容总结',
        text: summary.value,
        url: window.location.href
      })
    } else {
      // 如果不支持原生分享，创建分享链接
      const shareUrl = `${window.location.origin}/share?summary=${encodeURIComponent(summary.value)}`
      await navigator.clipboard.writeText(shareUrl)
      alert('分享链接已复制到剪贴板')
    }
  } catch (err) {
    console.error('分享失败:', err)
    alert('分享失败，请重试')
  }
}

// 下载结果
const downloadResult = () => {
  const blob = new Blob([summary.value], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'summary.txt'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

onMounted(() => {
  // 初始化 Uppy 实例
  uppy.value = new Uppy({
    restrictions: {
      maxFileSize: 100 * 1024 * 1024,
      maxNumberOfFiles: 5,
      allowedFileTypes: Object.keys(allowedFileTypes)
    },
    locale: {
      strings: locale.value === 'zh' ? t('uppy') : undefined
    }
  })
  .use(Dashboard, {
    target: '#uppy',
    inline: true,
    height: 300,
    width: '100%',
    hideUploadButton: true,
    proudlyDisplayPoweredByUppy: false
  })
  
  // 监听文件添加事件
  uppy.value.on('file-added', (file) => {
    const fileType = file.type
    if (!Object.keys(allowedFileTypes).includes(fileType)) {
      uppy.value.removeFile(file.id)
      alert(`不支持的文件类型！\n支持的格式：${Object.values(allowedFileTypes).join(', ')}`)
    } else {
      // 更新响应式文件列表
      uploadedFiles.value = uppy.value.getFiles()
    }
  })

  // 监听文件移除事件
  uppy.value.on('file-removed', () => {
    // 更新响应式文件列表
    uploadedFiles.value = uppy.value.getFiles()
  })
})

// 监听语言变化，更新 Uppy 的语言设置
watch(locale, (newLocale) => {
  if (uppy.value) {
    uppy.value.setOptions({
      locale: {
        strings: newLocale === 'zh' ? t('uppy') : undefined
      }
    })
  }
})

// 提交处理函数
const handleSubmit = async () => {
  try {
    loading.value = true;
    summary.value = '';  // 清空之前的结果
    
    const formData = new FormData();
    
    // 添加文件
    if (uploadedFiles.value.length > 0) {
      uploadedFiles.value.forEach(file => {
        formData.append('files', file.data);
      });
    }
    
    // 添加文本
    if (texts.value[0]?.trim()) {
      formData.append('text', texts.value[0]);
    }
    
    // 添加URL
    if (urls.value[0]?.trim()) {
      formData.append('url', urls.value[0]);
    }

    // 打印请求信息
    console.log('Sending request to:', `${config.API_BASE_URL}/summary`);
    
    const response = await fetch(`${config.API_BASE_URL}/summary`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }

    const data = await response.json();
    console.log('Submit response:', data);  // 添加日志
    
    if (data.task_id) {
      await pollTaskStatus(data.task_id);
    } else {
      throw new Error('No task ID received');
    }
  } catch (error) {
    console.error('Error:', error)
    alert(t('messages.processingError'))
  } finally {
    loading.value = false;
  }
}

const pollTaskStatus = async (taskId) => {
  try {
    let retries = 0;
    const maxRetries = 180;  // 增加到3分钟
    const interval = 1000;  // 每秒轮询一次
    
    while (retries < maxRetries) {
      const response = await fetch(`${config.API_BASE_URL}/summary/${taskId}`);
      const data = await response.json();
      console.log('Poll response:', data);  // 添加日志
      
      if (data.status === 'completed') {
        if (data.result && data.result.summary) {
          // 处理summary可能是数组的情况
          summary.value = Array.isArray(data.result.summary) 
            ? data.result.summary.join('\n\n')  // 如果是数组，用双换行符连接
            : data.result.summary;
          console.log('Summary length:', summary.value.length);
          break;
        } else {
          console.error('Invalid result format:', data);
          throw new Error('无效的结果格式');
        }
      } else if (data.status === 'error') {
        throw new Error(data.error || '处理失败');
      }
      
      retries++;
      await new Promise(resolve => setTimeout(resolve, interval));
    }
    
    if (retries >= maxRetries) {
      throw new Error('处理超时，请稍后重试');
    }
  } catch (error) {
    console.error('Error polling task status:', error);
    throw error;
  }
};

// URL格式验证函数
const isValidUrl = (url: string) => {
  try {
    new URL(url);
    return true;
  } catch (e) {
    return false;
  }
}

// 修改 addUrl 方法，添加URL验证
const addUrl = () => {
  // 检查最后一个URL是否有效
  const lastUrl = urls.value[urls.value.length - 1]
  if (lastUrl && !isValidUrl(lastUrl)) {
    alert(t('input.url.invalid'))
    return
  }
  urls.value.push('')
}

const removeUrl = (index) => {
  urls.value.splice(index, 1)
}

const addText = () => {
  texts.value.push('')
}

const removeText = (index) => {
  texts.value.splice(index, 1)
}

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(summary.value)
    showCopyTip.value = true
    setTimeout(() => {
      showCopyTip.value = false
    }, 2000)
  } catch (err) {
    console.error('复制失败:', err)
    alert(t('messages.copyFailed'))
  }
}

const downloadTxt = () => {
  const blob = new Blob([summary.value], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'summary.txt'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const regenerate = () => {
  // Implement the regenerate logic here
  console.log('Regenerate clicked')
}

const goToGuide = () => {
  router.push('/guide')
}

// 显示联系信息
const showContactInfo = () => {
  showContact.value = true
}
</script>

<style scoped>
.page-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.top-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  margin-bottom: 1rem;
}

.product-intro {
  display: flex;
  align-items: center;
}

h1 {
  font-size: 1.5rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.subtitle {
  font-size: 1rem;
  color: #666;
  margin-left: 1rem;
  font-weight: normal;
}

.top-buttons {
  display: flex;
  gap: 1rem;
}

.guide-btn, .contact-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.feature-list {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background: #f5f5f5;
  border-radius: 4px;
  justify-content: center;
}

.feature {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  flex: 1;
}

.input-section, .output-section {
  background: #fff;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.input-wrapper {
  position: relative;
  width: 100%;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.form-input {
  flex: 1;
  min-width: 0;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  border-color: #2196F3;
  outline: none;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

.remove-btn {
  margin-left: 8px;
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  color: #757575;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 20px;
  font-weight: 300;
  padding: 0;
  line-height: 1;
  user-select: none;
}

.remove-btn:hover {
  background: #e0e0e0;
  color: #424242;
  border-color: #bdbdbd;
  transform: scale(1.05);
}

.remove-btn:active {
  transform: scale(0.95);
}

.add-btn {
  width: 100%;
  padding: 0.75rem;
  background: #f5f5f5;
  border: 1px dashed #ccc;
  border-radius: 4px;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  transition: all 0.3s ease;
}

.add-btn:hover {
  background: #e0e0e0;
  border-color: #999;
  color: #333;
}

.add-btn i {
  font-size: 0.9rem;
}

.url-inputs, .text-inputs {
  margin-bottom: 1.5rem;
  width: 100%;
}

.url-input-group, .text-input-group {
  width: 100%;
}

textarea.form-input {
  resize: vertical;
  min-height: 80px;
  margin-right: 0;
}

.submit-btn {
  width: 100%;
  padding: 0.75rem;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 1rem;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.result-container {
  height: 100%;
  overflow-y: auto;
}

.empty-state {
  color: #666;
  text-align: center;
  padding: 2rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .top-section {
    flex-direction: column;
    gap: 1rem;
  }
}

.result-section {
  margin-top: 2rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 8px;
}

.summary-content {
  max-height: 500px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: monospace;
  background: white;
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid #ddd;
}

pre {
  margin: 0;
  white-space: pre-wrap;
}

/* 联系方式弹窗样式 */
.contact-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.contact-info {
  margin: 1.5rem 0;
}

.contact-info p {
  margin: 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.contact-info a {
  color: #2196F3;
  text-decoration: none;
}

.contact-info a:hover {
  text-decoration: underline;
}

.contact-footer {
  margin-top: 1.5rem;
  text-align: center;
}

.feedback-text {
  color: #666;
  font-style: italic;
  margin-bottom: 1rem;
}

.close-btn {
  padding: 0.5rem 2rem;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #1976D2;
}

.copy-tip {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 添加语言切换按钮样式 */
.lang-btn {
  padding: 0.5rem 1rem;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.lang-btn:hover {
  background: #f5f5f5;
  border-color: #ccc;
}
</style> 