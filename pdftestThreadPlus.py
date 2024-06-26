import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def process_page(pdf_path, page_num):
    try:
        pdf_document = fitz.open(pdf_path)
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))
        text = extract_text_from_image(img)
        print(f"Processed page {page_num + 1}/{pdf_document.page_count}")
        return text
    except Exception as e:
        return f"Error processing page {page_num}: {e}"

def extract_text_from_pdf(pdf_path, output_text_path):
    pdf_document = fitz.open(pdf_path)
    num_pages = len(pdf_document)
    extracted_text = ""

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_page, pdf_path, page_num) for page_num in range(num_pages)]
        for future in as_completed(futures):
            extracted_text += future.result() + "\n"

    with open(output_text_path, 'w', encoding='utf-8') as f:
        f.write(extracted_text)

# 함수 호출
extract_text_from_pdf(pdf_path, output_text_path)