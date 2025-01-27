import dashscope
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class AliSummaryService:
    def __init__(self):
        # 直接设置 API key
        dashscope.api_key = settings.ALI_API_KEY
        self.model = 'qwen-max'  # 使用通义千问-max模型
        
    def _generate_prompt(self, content: str) -> str:
        return f"""请对以下内容进行总结，要求：
1. 提取核心要点
2. 保持客观准确
3. 语言简洁清晰
4. 按重要性排序
5. 总结长度控制在300字以内

内容如下：
{content}
"""

    async def summarize(self, content: str) -> str:
        try:
            logger.info("Starting summarization with content length: %d", len(content))
            messages = [{
                'role': 'system',
                'content': '你是一个专业的文本总结助手，善于提取文本的核心内容并进行精炼总结。'
            }, {
                'role': 'user',
                'content': self._generate_prompt(content)
            }]

            logger.info("Calling Ali API with model: %s", self.model)
            response = dashscope.Generation.call(
                model=self.model,
                messages=messages,
                result_format='message',
                max_tokens=800,
                temperature=0.3,
            )
            logger.info("Received response from Ali API with status code: %d", response.status_code)

            if response.status_code == 200:
                result = response.output.choices[0]['message']['content']
                logger.info("Successfully generated summary with length: %d", len(result))
                return result
            else:
                logger.error(f"Ali API error: {response.code} - {response.message}")
                raise Exception(f"调用API失败: {response.message}")

        except Exception as e:
            logger.error(f"Error in summarize: {str(e)}", exc_info=True)
            raise Exception(f"总结失败: {str(e)}")

    async def summarize_url(self, url: str) -> str:
        # 这里可以添加网页内容抓取的逻辑
        try:
            import requests
            from bs4 import BeautifulSoup

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取正文内容
            content = ' '.join([p.text for p in soup.find_all('p')])
            
            return await self.summarize(content)
        except Exception as e:
            logger.error(f"Error in summarize_url: {str(e)}", exc_info=True)
            raise Exception(f"处理URL失败: {str(e)}") 