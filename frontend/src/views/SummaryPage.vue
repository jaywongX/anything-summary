<template>
  <div class="page-container">
    <!-- 顶部区域 -->
    <div class="top-section">
      <!-- 产品描述 -->
      <div class="product-intro">
        <h1>
          <span class="logo">🎯</span> 
          Anything Summary
        </h1>
        <p class="intro-text">
          一站式智能内容总结工具
          <span class="feature-list">
            <span class="feature">📝 文本</span>
            <span class="feature">🔗 网页</span>
            <span class="feature">📄 文档</span>
            <span class="feature">🎵 音频</span>
            <span class="feature">🎬 视频</span>
            <span class="feature">📦 压缩包</span>
          </span>
        </p>
      </div>

      <!-- 右侧按钮组 -->
      <div class="top-buttons">
        <button class="guide-btn" @click="goToGuide">
          <i class="fas fa-question-circle"></i> 使用指南
        </button>
        <button class="contact-btn" @click="showContactInfo">
          <i class="fas fa-envelope"></i> 联系我们
        </button>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧输入区域 -->
      <div class="input-section">
        <h2>输入区域</h2>
        
        <!-- URL输入区 -->
        <div class="url-inputs">
          <h3>网页链接 ({{ urls.length }}个)</h3>
          <div v-for="(url, index) in urls" :key="'url-'+index" class="url-input-group">
            <input 
              v-model="urls[index]" 
              type="text" 
              class="form-input"
              placeholder="请输入网页链接"
            >
            <button @click="removeUrl(index)" class="remove-btn" v-if="urls.length > 1">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <button @click="addUrl" class="add-btn">
            <i class="fas fa-plus"></i> 添加链接
          </button>
        </div>

        <!-- 文本输入区 -->
        <div class="text-inputs">
          <h3>文本内容 ({{ texts.length }}个)</h3>
          <div v-for="(text, index) in texts" :key="'text-'+index" class="text-input-group">
            <textarea 
              v-model="texts[index]" 
              class="form-input"
              placeholder="请输入文本内容"
              rows="4"
            ></textarea>
            <button @click="removeText(index)" class="remove-btn" v-if="texts.length > 1">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <button @click="addText" class="add-btn">
            <i class="fas fa-plus"></i> 添加文本
          </button>
        </div>

        <!-- 文件上传区域 -->
        <div class="file-upload">
          <h3>文件上传</h3>
          <div id="uppy"></div>
          <p class="file-hint">
            支持的文件类型：<br>
            文档：PDF、Word、TXT<br>
            图片：JPG、PNG、GIF、WEBP、BMP、SVG<br>
            音频：MP3、WAV、OGG、AAC、M4A、FLAC<br>
            视频：MP4、WEBM、OGV、MOV、AVI、MKV<br>
            (单个文件最大100MB)
          </p>
        </div>

        <button @click="handleSubmit" class="submit-btn" :disabled="!hasInput">
          开始总结
        </button>
      </div>

      <!-- 右侧输出区域 -->
      <div class="output-section">
        <h2>总结结果</h2>
        <div class="result-container">
          <div v-if="loading" class="loading">
            正在生成总结...
          </div>
          <div v-else-if="summary" class="summary-result">
            <p>{{ summary }}</p>
            <div class="action-buttons">
              <button @click="copyToClipboard" class="action-btn">
                <i class="fas fa-copy"></i> 复制
              </button>
              <button @click="downloadTxt" class="action-btn">
                <i class="fas fa-download"></i> 下载
              </button>
              <button @click="regenerate" class="action-btn">
                <i class="fas fa-sync"></i> 重新生成
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 联系方式弹窗 -->
  <div v-if="showContact" class="contact-modal">
    <div class="modal-content">
      <h3>联系我们</h3>
      <div class="contact-info">
        <p><i class="fas fa-envelope"></i> 邮箱：support@anythingsummary.com</p>
        <p><i class="fab fa-github"></i> GitHub：<a href="https://github.com/yourusername/anything-summary" target="_blank">anything-summary</a></p>
        <p><i class="fab fa-weixin"></i> 微信公众号：AnythingSummary</p>
      </div>
      <div class="contact-footer">
        <p class="feedback-text">欢迎反馈问题或建议，帮助我们做得更好！</p>
        <button class="close-btn" @click="showContact = false">关闭</button>
      </div>
    </div>
  </div>

  <!-- 复制成功提示 -->
  <div v-if="showCopyTip" class="copy-tip">
    复制成功！
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Uppy from '@uppy/core'
import Dashboard from '@uppy/dashboard'
import '@uppy/core/dist/style.css'
import '@uppy/dashboard/dist/style.css'
import { mockSummaryService } from '../mock/summaryService'
import { config } from '../config'
import { useRouter } from 'vue-router'

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
  // 初始化Uppy上传组件
  uppy.value = new Uppy({
    restrictions: {
      maxFileSize: 100 * 1024 * 1024,
      maxNumberOfFiles: 5,
      allowedFileTypes: Object.keys(allowedFileTypes)
    }
  })
  .use(Dashboard, {
    target: '#uppy',
    inline: true,
    height: 250,
    width: '100%',
    hideUploadButton: true,
    proudlyDisplayPoweredByUppy: false,
    locale: {
      strings: {
        dropPasteFiles: '拖拽文件到这里，或者 %{browse}',
        browse: '选择文件',
        uploadComplete: '上传完成',
        uploadFailed: '上传失败',
        dataUploadXFiles: '已选择 %{smart_count} 个文件',
        dropPaste: '拖拽文件到这里，或者 %{browse}'
      }
    }
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

// 提交处理函数
const handleSubmit = async () => {
  try {
    // 验证是否有内容需要处理
    if (!hasInput.value) {
      alert('请至少输入一项需要总结的内容（文本、URL或文件）');
      return;
    }

    loading.value = true;
    const formData = new FormData();
    
    // 添加文件
    if (uploadedFiles.value.length > 0) {
      uploadedFiles.value.forEach(file => {
        formData.append('files', file.data);  // 注意这里改为 'files'
      });
    }
    
    // 添加URL
    const validUrls = urls.value.filter(url => url.trim() && isValidUrl(url.trim()));
    if (validUrls.length > 0) {
      formData.append('urls', validUrls.join(','));
    }
    
    // 添加文本
    const validTexts = texts.value.filter(text => text.trim());
    if (validTexts.length > 0) {
      formData.append('texts', validTexts.join('\n\n'));
    }

    console.log('Sending request with content:');
    console.log('- Files:', uploadedFiles.value.length);
    console.log('- URLs:', validUrls.length);
    console.log('- Texts:', validTexts.length);

    const response = await fetch(`${config.apiBaseUrl}/summary`, {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    console.log('Response data:', data);

    if (data.success) {
      pollTaskStatus(data.task_id);
    } else {
      throw new Error(data.error || '处理失败');
    }
  } catch (error) {
    console.error('处理失败:', error);
    alert(error.message || '处理失败，请重试');
  }
};

// 添加轮询任务状态的函数
const pollTaskStatus = async (taskId) => {
  try {
    const response = await fetch(`${config.apiBaseUrl}/summary/${taskId}`)
    const data = await response.json()
    
    if (data.status === 'completed') {
      summary.value = data.result.summary
      loading.value = false
    } else if (data.status === 'processing') {
      // 继续轮询
      setTimeout(() => pollTaskStatus(taskId), 1000)
    } else if (data.status === 'error') {
      loading.value = false
      throw new Error(data.error || '处理失败')
    } else {
      loading.value = false
      throw new Error('未知状态：' + data.status)
    }
  } catch (error) {
    loading.value = false
    console.error('轮询任务状态失败:', error)
    alert(error.message || '处理失败，请重试')
  }
}

// URL格式验证函数
const isValidUrl = (url) => {
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
    alert('请输入有效的URL地址，例如: https://www.example.com')
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
    alert('复制失败，请手动复制')
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
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  padding: 1rem;
  gap: 2rem;
}

.top-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}

.product-intro {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  font-size: 2rem;
}

.product-intro h1 {
  font-size: 1.8rem;
  color: #2196F3;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.intro-text {
  font-size: 1rem;
  color: #555;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.feature-list {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.feature {
  font-size: 0.9rem;
  padding: 0.25rem 0.75rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.top-buttons {
  display: flex;
  gap: 1rem;
}

.guide-btn, .contact-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 20px;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  background: white;
}

.guide-btn {
  color: #2196F3;
  border: 1px solid #2196F3;
}

.contact-btn {
  color: #4CAF50;
  border: 1px solid #4CAF50;
}

.guide-btn:hover, .contact-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.guide-btn:hover {
  background: #2196F3;
  color: white;
}

.contact-btn:hover {
  background: #4CAF50;
  color: white;
}

.main-content {
  display: flex;
  gap: 2rem;
}

.input-section, .output-section {
  flex: 1;
  padding: 1.5rem;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 1.5rem;
  color: #333;
  font-size: 1.5rem;
}

.url-inputs, .text-inputs {
  margin-bottom: 1.5rem;
}

.url-input-group, .text-input-group {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.form-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.add-btn, .remove-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-btn {
  background: #4CAF50;
  color: white;
  width: 100%;
  margin-top: 0.5rem;
}

.add-btn:hover {
  background: #45a049;
}

.remove-btn {
  background: #ff5252;
  color: white;
  padding: 0.75rem;
}

.remove-btn:hover {
  background: #ff3939;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.submit-btn:hover {
  background: #1976D2;
}

.result-container {
  min-height: 300px;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 1rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.summary-result {
  white-space: pre-wrap;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  justify-content: flex-end;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.action-btn:nth-child(1) {
  background: #4CAF50;
  color: white;
}

.action-btn:nth-child(2) {
  background: #2196F3;
  color: white;
}

.action-btn:nth-child(3) {
  background: #FF9800;
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
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

h3 {
  margin: 1rem 0;
  color: #666;
  font-size: 1.1rem;
}

.file-upload {
  margin: 1.5rem 0;
  padding: 1rem;
  border: 1px dashed #ddd;
  border-radius: 4px;
}

.file-hint {
  margin-top: 0.5rem;
  color: #666;
  font-size: 0.9rem;
  text-align: left;
  line-height: 1.5;
  padding: 0.5rem;
  background: #f5f5f5;
  border-radius: 4px;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.product-intro h1 {
  font-size: 2.5rem;
  color: #2196F3;
  margin-bottom: 1rem;
  font-weight: bold;
}

.intro-text {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.intro-sub {
  font-size: 1.1rem;
  color: #666;
  font-style: italic;
}

.feature {
  display: inline-block;
  margin: 0.25rem;
  padding: 0.5rem 1rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.feature:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.file-hint::after {
  content: "压缩包：ZIP、GZ、TAR、RAR、7Z";
  display: block;
  margin-top: 0.5rem;
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

/* 响应式调整 */
@media (max-width: 768px) {
  .top-section {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .feature-list {
    justify-content: center;
  }

  .top-buttons {
    width: 100%;
    justify-content: center;
  }
}
</style> 