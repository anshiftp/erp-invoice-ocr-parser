"""
preprocessing.py
----------------
Handles ONLY image preprocessing.

Purpose:
Improve OCR accuracy by enhancing image quality.
"""

import cv2

def preprocess_image(image_path):
    """
    Reads image and prepares it for OCR.
    """

    # Load image
    image = cv2.imread(image_path)

    # Safety check
    if image is None:
        raise ValueError("Failed to load image")

    # Resize to improve small text recognition
    image = cv2.resize(
        image, None, fx=1.5, fy=1.5,
        interpolation=cv2.INTER_CUBIC
    )

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Reduce noise
    gray = cv2.medianBlur(gray, 3)

    # Adaptive thresholding (handles uneven lighting)
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresh
