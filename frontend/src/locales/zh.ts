export default {
  app: {
    title: 'Anything Summary',
    subtitle: '一站式智能内容总结工具，支持多模态混合输入',
    guide: '使用指南',
    contact: '联系我们'
  },
  features: {
    text: '文本',
    webpage: '网页',
    document: '文档',
    audio: '音频',
    video: '视频',
    archive: '压缩包'
  },
  input: {
    url: {
      placeholder: '输入网页链接',
      add: '添加链接',
      invalid: '请输入有效的URL地址，例如：https://www.example.com'
    },
    text: {
      placeholder: '输入或粘贴文本内容',
      add: '添加文本'
    },
    delete: '删除',
    file: {
      title: '拖放文件到此处或点击浏览',
      maxSize: '最大文件大小：100MB',
      allowedTypes: '支持的格式',
      button: '选择文件'
    }
  },
  actions: {
    submit: '一键总结',
    copy: '复制',
    download: '下载',
    regenerate: '重新生成'
  },
  status: {
    processing: '正在生成总结...',
    empty: '在左侧输入内容，点击"一键总结"生成摘要'
  },
  contact: {
    title: '联系我们',
    email: '邮箱：support@anythingsummary.com',
    github: 'GitHub：anything-summary',
    wechat: '微信公众号：AnythingSummary',
    feedback: '欢迎反馈问题或建议，帮助我们做得更好！',
    close: '关闭'
  },
  guide: {
    title: '如何使用',
    sections: {
      input: {
        title: '输入方式',
        text: '直接输入或粘贴文本',
        url: '输入网页链接，自动提取内容',
        file: '上传文件（支持多种格式）'
      },
      formats: {
        title: '支持的格式',
        docs: '文档：PDF、Word、TXT',
        images: '图片：JPG、PNG、GIF（支持OCR文字识别）',
        audio: '音频：MP3、WAV（支持语音转文字）',
        video: '视频：MP4、AVI（支持提取音频进行转写）',
        archive: '压缩包：ZIP、RAR、7Z（自动解压并处理内容）'
      },
      process: {
        title: '生成总结',
        step1: '确保至少输入了一种内容（文本、链接或文件）',
        step2: '点击"一键总结"按钮',
        step3: '等待系统处理（处理时间取决于内容长度和类型）'
      },
      results: {
        title: '结果处理',
        description: '获得总结结果后，您可以：',
        copy: '复制：一键复制总结内容到剪贴板',
        download: '下载：将总结内容保存为TXT文件',
        regenerate: '重新生成：如果结果不理想，可以重新生成总结'
      },
      tips: {
        title: '使用建议',
        quality: '输入内容越清晰准确，生成的总结质量越高',
        length: '对于长文本，建议分段输入以获得更好的效果',
        files: '如果上传文件，请确保文件质量良好（如图片清晰、音频清楚等）'
      }
    }
  },
  messages: {
    copySuccess: '复制成功！',
    copyFailed: '复制失败，请手动复制',
    uploadError: '文件上传失败',
    processingError: '处理失败，请重试',
    timeout: '请求超时，请重试'
  },
  uppy: {
    dropPaste: '将文件拖放到这里或%{browse}',
    browse: '浏览',
    uploadComplete: '上传完成',
    uploadFailed: '上传失败',
    dataUploadXFiles: '正在上传 %{smart_count} 个文件',
    xFilesSelected: {
      0: '已选择 %{smart_count} 个文件',
      1: '已选择 %{smart_count} 个文件'
    },
    dropHint: '将文件拖放到此处',
    fileSource: '来源：%{name}',
    myDevice: '我的设备',
    chooseFiles: '选择文件',
    orDragDrop: '或拖放文件',
    filesUploadedOfTotal: {
      0: '已上传 %{complete} / %{smart_count} 个文件',
      1: '已上传 %{complete} / %{smart_count} 个文件'
    },
    maxFileSize: '最大文件大小：%{size}',
    removeFile: '移除文件'
  }
} 