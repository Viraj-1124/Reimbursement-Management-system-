import re
import base64
from datetime import date
from pathlib import Path

try:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    from PIL import Image
    import cv2
    import numpy as np
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


def preprocess_image(image_path: str) -> "np.ndarray":
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=30)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def extract_text_from_image(image_path: str) -> str:
    if not TESSERACT_AVAILABLE:
        raise RuntimeError("pytesseract / OpenCV not installed. Run: pip install pytesseract opencv-python pillow")

    processed = preprocess_image(image_path)
    pil_img = Image.fromarray(processed)
    text = pytesseract.image_to_string(pil_img, config="--psm 6")
    return text.strip()


def extract_text_from_base64(image_b64: str) -> str:
    import tempfile, os
    image_data = base64.b64decode(image_b64)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(image_data)
        tmp_path = tmp.name

    try:
        text = extract_text_from_image(tmp_path)
    finally:
        os.remove(tmp_path)

    return text


def parse_amount_from_text(text: str) -> float | None:
    patterns = [
        r"(?:grand\s*total|total\s*due|total\s*amount|amount\s*due|total)[:\s\$]*([0-9,]+\.[0-9]{2})",
        r"\$\s*([0-9,]+\.[0-9]{2})",
        r"([0-9,]+\.[0-9]{2})\s*(?:USD|INR|EUR|GBP)?",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw = match.group(1).replace(",", "")
            try:
                return float(raw)
            except ValueError:
                continue
    return None


def parse_date_from_text(text: str) -> str | None:
    patterns = [
        r"(\d{2})[\/\-\.](\d{2})[\/\-\.](\d{4})",
        r"(\d{4})[\/\-\.](\d{2})[\/\-\.](\d{2})",
        r"(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\,\s]+(\d{4})",
    ]
    month_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "may": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            groups = match.groups()
            try:
                if len(groups) == 3:
                    if groups[1].lower() in month_map:
                        return f"{groups[2]}-{month_map[groups[1].lower()]}-{int(groups[0]):02d}"
                    elif len(groups[0]) == 4:
                        return f"{groups[0]}-{groups[1]}-{groups[2]}"
                    else:
                        return f"{groups[2]}-{groups[1]}-{groups[0]}"
            except Exception:
                continue
    return None


def parse_vendor_from_text(text: str) -> str | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines:
        return lines[0]
    return None


def process_receipt(image_path: str) -> dict:
    raw_text = extract_text_from_image(image_path)

    amount = parse_amount_from_text(raw_text)
    receipt_date = parse_date_from_text(raw_text)
    vendor = parse_vendor_from_text(raw_text)

    found = sum([amount is not None, receipt_date is not None, vendor is not None])
    confidence = round(found / 3, 2)

    return {
        "raw_text": raw_text,
        "amount": amount,
        "date": receipt_date,
        "vendor": vendor,
        "confidence": confidence,
    }


def process_receipt_from_base64(image_b64: str) -> dict:
    import tempfile, os
    image_data = base64.b64decode(image_b64)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(image_data)
        tmp_path = tmp.name

    try:
        result = process_receipt(tmp_path)
    finally:
        os.remove(tmp_path)

    return result