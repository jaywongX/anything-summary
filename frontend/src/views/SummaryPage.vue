<template>
  <div class="summary-container">
    <h1 class="title">AnythingSummary</h1>
    <div class="subtitle">支持文本、文档、图片、音视频、网页等内容的智能总结</div>
    
    <!-- 输入区域容器 -->
    <div class="input-section">
      <!-- 链接输入区域 -->
      <div class="url-input-container">
        <div class="section-title">
          <i class="fas fa-link"></i>
          <span>网页链接</span>
        </div>
        <input 
          type="url" 
          v-model="urlInput"
          placeholder="请输入需要总结的网页链接"
          class="url-input"
        />
      </div>
      
      <!-- 富文本编辑器区域 -->
      <div class="editor-container">
        <div class="section-title">
          <i class="fas fa-edit"></i>
          <span>文本输入</span>
        </div>
        <div id="editor"></div>
      </div>

      <!-- 文件上传区域 -->
      <div class="uploader-container">
        <div class="section-title">
          <i class="fas fa-file-upload"></i>
          <span>文件上传</span>
        </div>
        <div id="uppy"></div>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="action-buttons">
      <button 
        class="submit-btn" 
        @click="handleSubmit" 
        :disabled="isProcessing || (!hasContent && !hasFiles && !urlInput.trim())"
      >
        <i class="fas fa-magic" v-if="!isProcessing"></i>
        <i class="fas fa-spinner fa-spin" v-else></i>
        {{ isProcessing ? '正在总结...' : '开始总结' }}
      </button>
    </div>

    <!-- 结果展示区域 -->
    <div class="result-container" v-if="summaryResult">
      <div class="result-header">
        <h2>总结结果</h2>
        <div class="result-actions">
          <button class="action-btn" @click="copyResult" title="复制内容">
            <i class="fas fa-copy"></i>
          </button>
          <button class="action-btn" @click="shareResult" title="分享链接">
            <i class="fas fa-share-alt"></i>
          </button>
          <button class="action-btn" @click="downloadResult" title="下载文件">
            <i class="fas fa-download"></i>
          </button>
        </div>
      </div>
      <div class="summary-content" v-html="formattedSummary"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Quill from 'quill'
import Uppy from '@uppy/core'
import Dashboard from '@uppy/dashboard'
import '@uppy/core/dist/style.css'
import '@uppy/dashboard/dist/style.css'
import 'quill/dist/quill.snow.css'
import { mockSummaryService } from '../mock/summaryService'
import { config } from '../config'

const quill = ref(null)
const uppy = ref(null)
const summaryResult = ref('')
const isProcessing = ref(false)
const urlInput = ref('')

// 计算是否有内容输入
const hasContent = computed(() => {
  return quill.value && quill.value.getText().trim().length > 0
})

// 计算是否有文件上传
const hasFiles = computed(() => {
  return uppy.value && uppy.value.getFiles().length > 0
})

// 格式化后的摘要内容
const formattedSummary = computed(() => {
  if (!summaryResult.value) return ''
  // 将换行符转换为HTML换行，保持格式
  return summaryResult.value.replace(/\n/g, '<br>')
})

// 允许的文件类型
const allowedFileTypes = {
  documents: [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain'
  ]
}

// 复制结果
const copyResult = async () => {
  try {
    await navigator.clipboard.writeText(summaryResult.value)
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
        text: summaryResult.value,
        url: window.location.href
      })
    } else {
      // 如果不支持原生分享，创建分享链接
      const shareUrl = `${window.location.origin}/share?summary=${encodeURIComponent(summaryResult.value)}`
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
  const blob = new Blob([summaryResult.value], { type: 'text/plain' })
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
  // 初始化Quill编辑器
  quill.value = new Quill('#editor', {
    theme: 'snow',
    placeholder: '请输入需要总结的文本...',
    modules: {
      toolbar: [
        ['bold', 'italic', 'underline'],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        ['clean']
      ]
    }
  })

  // 初始化Uppy上传组件
  uppy.value = new Uppy({
    restrictions: {
      maxFileSize: 100 * 1024 * 1024, // 最大100MB
      maxNumberOfFiles: 5,
      allowedFileTypes: allowedFileTypes.documents
    }
  })
    .use(Dashboard, {
      target: '#uppy',
      inline: true,
      height: 300,
      width: '100%',
      note: '支持格式：PDF、Word、TXT文档，单个文件最大100MB',
      proudlyDisplayPoweredByUppy: false,
    })
    
  uppy.value.on('file-added', (file) => {
    const fileType = file.type
    const isValidType = allowedFileTypes.documents.includes(fileType)
    
    if (!isValidType) {
      uppy.value.removeFile(file.id)
      alert('不支持的文件格式！仅支持PDF、Word、TXT文档')
    }
  })
})

// 提交处理函数
const handleSubmit = async () => {
  try {
    isProcessing.value = true
    
    // 获取编辑器内容
    const textContent = quill.value.root.innerHTML
    
    // 获取上传的文件
    const files = uppy.value.getFiles()
    
    // 创建FormData对象
    const formData = new FormData()
    
    // 添加文本内容
    if (textContent.trim()) {
      formData.append('text', textContent)
    }
    
    // 添加URL
    if (urlInput.value.trim()) {
      formData.append('url', urlInput.value.trim())
    }
    
    // 添加文件到FormData
    files.forEach(file => {
      formData.append('files', file.data)
    })

    let data;
    if (config.useMockService) {
      data = await mockSummaryService(formData);
    } else {
      const response = await fetch(`${config.apiBaseUrl}/summary`, {
        method: 'POST',
        body: formData
      });
      data = await response.json();
    }

    summaryResult.value = data.summary;
    
  } catch (error) {
    console.error('处理失败:', error)
    alert('处理失败，请重试')
  } finally {
    isProcessing.value = false
  }
}
</script>

<style scoped>
.summary-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 10px;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
}

.input-section {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 30px;
}

.section-title {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  color: #2c3e50;
  font-weight: bold;
}

.section-title i {
  margin-right: 8px;
}

.url-input-container {
  margin-bottom: 20px;
}

.url-input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  transition: border-color 0.3s;
}

.url-input:focus {
  border-color: #4CAF50;
  outline: none;
}

.editor-container {
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

#editor {
  min-height: 200px;
}

.uploader-container {
  margin-bottom: 20px;
}

.action-buttons {
  text-align: center;
  margin: 30px 0;
}

.submit-btn {
  padding: 12px 30px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.submit-btn:hover:not(:disabled) {
  background-color: #45a049;
}

.submit-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.result-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-top: 30px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.result-header h2 {
  margin: 0;
  color: #2c3e50;
}

.result-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  padding: 8px;
  background: none;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn:hover {
  background-color: #f5f5f5;
  border-color: #999;
}

.summary-content {
  white-space: pre-wrap;
  line-height: 1.6;
  color: #2c3e50;
}

/* 添加响应式设计 */
@media (max-width: 768px) {
  .summary-container {
    padding: 10px;
  }
  
  .submit-btn {
    width: 100%;
    justify-content: center;
  }
  
  .result-header {
    flex-direction: column;
    gap: 10px;
  }
  
  .result-actions {
    width: 100%;
    justify-content: space-around;
  }
}
</style> 