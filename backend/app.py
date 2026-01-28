"""
app.py
------
Main Flask application.

Responsibilities:
1. Accept image uploads from frontend
2. Run OCR pipeline
3. Return structured data

Business logic is delegated to OCR modules.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from ocr.preprocessing import preprocess_image
from ocr.ocr_engine import extract_text
from ocr.parser import parse_bill_text

# -----------------------
# Flask App Setup
# -----------------------
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------
# Upload Endpoint
# -----------------------
@app.route("/upload", methods=["POST"])
def upload_bill():
    """
    Receives bill image and returns structured OCR output.
    """

    # Validate request
    if "image" not in request.files:
        return jsonify({"error": "Image not provided"}), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save uploaded image
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    # OCR Pipeline
    processed_image = preprocess_image(image_path)
    raw_text = extract_text(processed_image)
    structured_data = parse_bill_text(raw_text)

    return jsonify({
        "raw_text": raw_text,
        "structured_data": structured_data
    })

if __name__ == "__main__":
    app.run(debug=True)
