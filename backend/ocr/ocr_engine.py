"""
ocr_engine.py
-------------
Handles ONLY OCR using Tesseract.
No preprocessing. No parsing.
"""

import pytesseract

def extract_text(processed_image):
    """
    Runs OCR on processed image and returns raw text.
    """

    # OCR configuration
    # OEM 3 = best engine
    # PSM 6 = block of text
    custom_config = r"--oem 3 --psm 6"

    text = pytesseract.image_to_string(
        processed_image,
        config=custom_config
    )

    return text
