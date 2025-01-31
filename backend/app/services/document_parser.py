from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import docx
import fitz  # PyMuPDF
import io
import os
import logging
from typing import Optional
import PyPDF2
import sys

logger = logging.getLogger(__name__)

class DocumentParser:
    def __init__(self):
        self._check_dependencies()
        
    def _check_dependencies(self):
        """检查必要的依赖是否已安装"""
        try:
            # 检查 tesseract
            if sys.platform.startswith('win'):
                if not os.environ.get('TESSERACT_CMD'):
                    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                    if os.path.exists(tesseract_path):
                        pytesseract.pytesseract.tesseract_cmd = tesseract_path
                    else:
                        logger.warning("Tesseract not found in default location")
            
            # 测试 tesseract 是否可用
            try:
                pytesseract.get_tesseract_version()
                logger.info("Tesseract is available")
            except Exception as e:
                logger.error(f"Tesseract is not properly installed: {str(e)}")
            
            # 检查中文语言包
            if sys.platform.startswith('win'):
                tessdata_path = os.path.join(os.path.dirname(pytesseract.pytesseract.tesseract_cmd), 'tessdata')
            else:
                tessdata_path = '/usr/share/tesseract-ocr/4.00/tessdata'
            
            if not os.path.exists(os.path.join(tessdata_path, 'chi_sim.traineddata')):
                logger.warning("Chinese language pack not found")
            
            # 检查 poppler
            try:
                from pdf2image.exceptions import PDFPageCountError
                logger.info("pdf2image (poppler) is available")
            except ImportError as e:
                logger.error(f"pdf2image or poppler is not properly installed: {str(e)}")
            
            # 检查 PyCryptodome
            try:
                from Crypto.Cipher import AES
                logger.info("PyCryptodome is available")
            except ImportError:
                logger.error("PyCryptodome is not properly installed")
                
        except Exception as e:
            logger.error(f"Error checking dependencies: {str(e)}")

    def parse_file(self, file_path: str) -> Optional[str]:
        """解析文件内容"""
        try:
            file_extension = file_path.lower().split('.')[-1]
            
            if file_extension == 'pdf':
                return self._parse_pdf(file_path)
            elif file_extension in ['doc', 'docx']:
                return self._parse_docx(file_path)
            elif file_extension == 'txt':
                return self._parse_txt(file_path)
            elif file_extension in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
                return self.parse_image(file_path)
            else:
                logger.warning(f"Unsupported file type: {file_extension}")
                return None
        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {str(e)}", exc_info=True)
            return None

    def _parse_pdf(self, file_path: str) -> Optional[str]:
        """解析PDF文件"""
        try:
            # 首先尝试使用 PyMuPDF
            doc = fitz.open(file_path)
            text_content = []
            
            # 获取页数
            num_pages = len(doc)
            logger.info(f"PDF has {num_pages} pages")
            
            # 提取所有页面的文本
            for page_num in range(num_pages):
                try:
                    page = doc[page_num]
                    text = page.get_text("text")
                    if text.strip():
                        text_content.append(text.strip())
                        logger.debug(f"Extracted text from page {page_num + 1}")
                    else:
                        logger.warning(f"No text found in page {page_num + 1}")
                except Exception as e:
                    logger.error(f"Error extracting text from page {page_num + 1}: {str(e)}")
                    continue

            doc.close()
            
            if text_content:
                full_text = '\n\n'.join(text_content)  # 使用双换行分隔页面
                logger.info(f"Successfully extracted {len(full_text)} characters using PyMuPDF")
                return full_text
            else:
                logger.info("No text extracted using PyMuPDF, trying OCR")
                return self._ocr_pdf(file_path)

        except Exception as e:
            logger.error(f"Error parsing PDF with PyMuPDF: {str(e)}", exc_info=True)
            logger.info("PyMuPDF failed, trying OCR")
            return self._ocr_pdf(file_path)

    def _parse_docx(self, file_path: str) -> Optional[str]:
        """解析DOCX文件"""
        try:
            doc = docx.Document(file_path)
            text_content = []
            
            # 提取所有段落
            for para in doc.paragraphs:
                if para.text.strip():
                    text_content.append(para.text)
            
            # 提取所有表格中的文本
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if cell.text.strip():
                            text_content.append(cell.text)
            
            full_text = '\n'.join(text_content)
            logger.info(f"Successfully extracted {len(full_text)} characters from DOCX")
            return full_text
        except Exception as e:
            logger.error(f"Error parsing DOCX file: {str(e)}", exc_info=True)
            return None

    def _parse_txt(self, file_path: str) -> Optional[str]:
        """解析TXT文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                logger.info(f"Successfully read {len(content)} characters from TXT")
                return content
        except UnicodeDecodeError:
            try:
                # 如果UTF-8解码失败，尝试使用GBK编码
                with open(file_path, 'r', encoding='gbk') as file:
                    content = file.read()
                    logger.info(f"Successfully read {len(content)} characters from TXT using GBK encoding")
                    return content
            except Exception as e:
                logger.error(f"Error parsing TXT file with GBK encoding: {str(e)}", exc_info=True)
                return None
        except Exception as e:
            logger.error(f"Error parsing TXT file: {str(e)}", exc_info=True)
            return None

    def parse_image(self, file_path: str) -> str:
        """解析图片文件"""
        try:
            image = Image.open(file_path)
            # 使用中文和英文语言包
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            return text
        except Exception as e:
            logger.error(f"Error parsing image: {str(e)}", exc_info=True)
            raise 

    def _ocr_pdf(self, file_path: str) -> Optional[str]:
        """使用OCR处理PDF文件"""
        try:
            # 将PDF转换为图片
            logger.info("Converting PDF to images...")
            images = convert_from_path(
                file_path,
                dpi=300,  # 提高DPI以获得更好的文本识别效果
                fmt='jpeg',
                thread_count=os.cpu_count() or 1  # 使用多线程加速
            )
            logger.info(f"Converted {len(images)} pages to images")
            
            # 对每个页面进行OCR
            text_content = []
            for i, image in enumerate(images):
                try:
                    # 预处理图像以提高OCR质量
                    image = Image.fromarray(self._preprocess_image(image))
                    
                    # 使用中文和英文语言包
                    text = pytesseract.image_to_string(
                        image,
                        lang='chi_sim+eng',
                        config='--psm 1 --oem 1'  # 使用更准确的OCR模式
                    )
                    
                    if text.strip():
                        text_content.append(text.strip())
                        logger.debug(f"OCR extracted text from page {i + 1}")
                    else:
                        logger.warning(f"OCR found no text in page {i + 1}")
                except Exception as e:
                    logger.error(f"Error performing OCR on page {i + 1}: {str(e)}")
                    continue
            
            if not text_content:
                logger.error("No text could be extracted from PDF using either method")
                return None
            
            full_text = '\n\n'.join(text_content)  # 使用双换行分隔页面
            logger.info(f"Successfully extracted {len(full_text)} characters from PDF using OCR")
            return full_text
        except Exception as e:
            logger.error(f"Error performing OCR on PDF: {str(e)}", exc_info=True)
            return None

    def _preprocess_image(self, image):
        """预处理图像以提高OCR质量"""
        import numpy as np
        from PIL import ImageEnhance
        
        # 转换为numpy数组
        img_array = np.array(image)
        
        # 转换为PIL图像进行增强
        img = Image.fromarray(img_array)
        
        # 增加对比度
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        
        # 增加锐度
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)
        
        return np.array(img) 