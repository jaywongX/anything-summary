from bs4 import BeautifulSoup
import requests
import PyPDF2
import docx
import io
import logging

logger = logging.getLogger(__name__)

class ParserService:
    @staticmethod
    def parse_url(url):
        """解析网页内容"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # 移除脚本和样式
            for script in soup(["script", "style"]):
                script.decompose()
            # 获取文本
            text = soup.get_text()
            # 清理文本
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            return text
        except Exception as e:
            return f"解析URL失败: {str(e)}"

    @staticmethod
    def parse_pdf(file_bytes):
        """解析PDF文件内容"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"解析PDF失败: {str(e)}"

    @staticmethod
    def parse_docx(file_bytes):
        """解析Word文件内容"""
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except Exception as e:
            return f"解析Word文件失败: {str(e)}"

    @staticmethod
    def parse_txt(file_bytes):
        """解析TXT文件内容"""
        try:
            logger.info("Attempting to parse TXT file")
            try:
                text = file_bytes.decode('utf-8')
                logger.info("Successfully decoded TXT file with UTF-8")
                return text
            except UnicodeDecodeError:
                logger.info("UTF-8 decode failed, trying GBK")
                try:
                    text = file_bytes.decode('gbk')
                    logger.info("Successfully decoded TXT file with GBK")
                    return text
                except Exception as e:
                    logger.error(f"GBK decode failed: {str(e)}")
                    return f"解析TXT文件失败: {str(e)}"
        except Exception as e:
            logger.error(f"Error parsing TXT file: {str(e)}")
            return f"解析TXT文件失败: {str(e)}" 