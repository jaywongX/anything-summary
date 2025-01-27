<template>
  <div class="guide-container">
    <h1>如何使用 AnythingSummary</h1>
    
    <div class="guide-section">
      <h2>1. 输入内容</h2>
      <p>您可以通过以下三种方式输入需要总结的内容（支持同时使用多种方式）：</p>
      
      <div class="guide-item">
        <h3>📝 文本输入</h3>
        <ul>
          <li>直接在文本框中输入或粘贴文字</li>
          <li>点击"添加文本"可以增加多个文本输入框</li>
          <li>每个文本框右侧的删除按钮可以移除不需要的输入框</li>
        </ul>
      </div>
      
      <div class="guide-item">
        <h3>🔗 网页链接</h3>
        <ul>
          <li>输入需要总结的网页URL</li>
          <li>支持添加多个网页链接</li>
          <li>系统会自动提取网页中的主要内容</li>
        </ul>
      </div>
      
      <div class="guide-item">
        <h3>📁 文件上传</h3>
        <ul>
          <li>支持多种文件格式：
            <ul>
              <li>文档：PDF、Word、TXT</li>
              <li>图片：JPG、PNG、GIF等（支持OCR文字识别）</li>
              <li>音频：MP3、WAV等（支持语音转文字）</li>
              <li>视频：MP4、AVI等（支持提取音频进行转写）</li>
              <li>压缩包：ZIP、GZ、TAR、RAR、7Z（自动解压并处理内容）</li>
            </ul>
          </li>
          <li>单个文件最大支持100MB</li>
          <li>可以同时上传多个文件（最多5个）</li>
        </ul>
      </div>
    </div>

    <div class="guide-section">
      <h2>2. 生成总结</h2>
      <ul>
        <li>确保至少输入了一种内容（文本、链接或文件）</li>
        <li>点击"开始总结"按钮</li>
        <li>等待系统处理（处理时间取决于内容长度和类型）</li>
      </ul>
    </div>

    <div class="guide-section">
      <h2>3. 结果处理</h2>
      <p>获得总结结果后，您可以：</p>
      <ul>
        <li>复制：一键复制总结内容到剪贴板</li>
        <li>下载：将总结内容保存为TXT文件</li>
        <li>重新生成：如果结果不理想，可以重新生成总结</li>
      </ul>
    </div>

    <div class="guide-section">
      <h2>使用建议</h2>
      <ul>
        <li>输入内容越清晰准确，生成的总结质量越高</li>
        <li>对于长文本，建议分段输入以获得更好的效果</li>
        <li>如果上传文件，请确保文件质量良好（如图片清晰、音频清楚等）</li>
      </ul>
    </div>

    <button class="back-btn" @click="goBack">返回主页</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.push('/')
}
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