// 模拟延迟
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 模拟文件类型对应的摘要结果
const mockSummaryByType = {
  text: "这是文本内容的摘要：主要讨论了...",
  url: "网页内容摘要：该页面主要介绍...",
  pdf: "PDF文档摘要：这份文档详细说明了...",
  image: "图片内容识别：图片中包含...",
  audio: "音频内容转写：讨论了关于...",
  video: "视频内容概述：视频主要展示了..."
};

// 模拟摘要服务
export const mockSummaryService = async (formData) => {
  // 模拟处理延迟 1-2 秒
  await delay(1000 + Math.random() * 1000);

  let summaryParts = [];

  // 处理文本内容
  const text = formData.get('text');
  if (text) {
    summaryParts.push(mockSummaryByType.text);
  }

  // 处理URL
  const url = formData.get('url');
  if (url) {
    summaryParts.push(`${mockSummaryByType.url}\n链接：${url}`);
  }

  // 处理文件
  const files = formData.getAll('files');
  files.forEach(file => {
    if (file.type.includes('pdf')) {
      summaryParts.push(mockSummaryByType.pdf);
    } else if (file.type.includes('image')) {
      summaryParts.push(mockSummaryByType.image);
    } else if (file.type.includes('audio')) {
      summaryParts.push(mockSummaryByType.audio);
    } else if (file.type.includes('video')) {
      summaryParts.push(mockSummaryByType.video);
    }
  });

  // 模拟成功或失败
  if (Math.random() > 0.1) { // 90% 成功率
    return {
      success: true,
      summary: summaryParts.join('\n\n')
    };
  } else {
    throw new Error('模拟服务器错误');
  }
}; 