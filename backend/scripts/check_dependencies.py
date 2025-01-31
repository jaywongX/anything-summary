#!/usr/bin/env python3
import sys
import os
import subprocess

def check_system_dependencies():
    """检查系统依赖"""
    print("Checking system dependencies...")
    
    # 检查 Python 版本
    print(f"Python version: {sys.version}")
    
    # 检查 Tesseract
    try:
        if sys.platform.startswith('win'):
            tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            if not os.path.exists(tesseract_cmd):
                print("ERROR: Tesseract not found. Please install from: https://github.com/UB-Mannheim/tesseract/wiki")
            else:
                print(f"Tesseract found at: {tesseract_cmd}")
        else:
            result = subprocess.run(['which', 'tesseract'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Tesseract found at: {result.stdout.strip()}")
            else:
                print("ERROR: Tesseract not found. Please install using: sudo apt-get install tesseract-ocr")
    except Exception as e:
        print(f"Error checking Tesseract: {str(e)}")
    
    # 检查 Poppler
    try:
        if sys.platform.startswith('win'):
            # Windows 上检查 poppler
            if 'POPPLER_PATH' not in os.environ:
                print("WARNING: POPPLER_PATH environment variable not set")
        else:
            result = subprocess.run(['which', 'pdftoppm'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Poppler found at: {result.stdout.strip()}")
            else:
                print("ERROR: Poppler not found. Please install using: sudo apt-get install poppler-utils")
    except Exception as e:
        print(f"Error checking Poppler: {str(e)}")

if __name__ == '__main__':
    check_system_dependencies() 