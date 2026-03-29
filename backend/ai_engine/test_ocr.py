import pytesseract
from PIL import Image

# Force correct path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

try:
    img = Image.open("passbook.jpeg")   # make sure name matches EXACTLY
    text = pytesseract.image_to_string(img)

    print("✅ OCR Working!")
    print("Extracted Text:\n", text)

except Exception as e:
    print("❌ Error:", e)