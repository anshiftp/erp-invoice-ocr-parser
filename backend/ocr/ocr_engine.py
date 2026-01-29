import pytesseract

def extract_text(processed_image):

    # OCR configuration
    # OEM 3 = best engine
    # PSM 6 = block of text
    custom_config = r"--oem 3 --psm 6"

    text = pytesseract.image_to_string(
        processed_image,
        config=custom_config
    )

    return text
