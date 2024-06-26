import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# Tesseract OCR 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# TESSDATA_PREFIX 환경 변수 설정
tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'

# PDF 파일 경로
pdf_path = '1999 철도통계연보(37회).pdf'
# 출력 텍스트 파일 경로
output_text_path = '1999 철도통계연보(37회).txt'

def extract_text_from_image(image):
    return pytesseract.image_to_string(image, lang='kor', config=tessdata_dir_config)

def extract_text_from_pdf(pdf_path, output_text_path):
    # PDF 열기
    pdf_document = fitz.open(pdf_path)
    extracted_text = ""

    # 각 페이지 순회
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        # 페이지를 이미지로 변환
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))

        # 이미지에서 텍스트 추출
        text = extract_text_from_image(img)
        extracted_text += text + "\n"

    # 추출된 텍스트를 파일에 저장
    with open(output_text_path, 'w', encoding='utf-8') as f:
        f.write(extracted_text)

# 함수 호출
extract_text_from_pdf(pdf_path, output_text_path)