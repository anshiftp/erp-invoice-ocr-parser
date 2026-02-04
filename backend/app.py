from flask import Flask, request, jsonify
from flask_cors import CORS
import os
# This imports the function from the OTHER file
from engines.gemini.gemini_engine import run_gemini 

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_bill():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files["image"]
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    print("DEBUG: Sending to Gemini...")

    # Run the engine
    structured_data = run_gemini(image_path)

    return jsonify({
        "engine": "gemini-1.5-flash",
        "structured_data": structured_data,
        "raw_donut_output": structured_data 
    })

if __name__ == "__main__":
    app.run(debug=True)