# 🧾 ERP Invoice OCR Parser

Enterprise Resource Planning (ERP) systems cannot tolerate hallucinated or partially incorrect financial data. A wrong GST number or invoice total is far more damaging than a missing value. 

This project addresses that constraint by prioritizing **correctness over completeness**, **explainability over blind inference**, and **schema safety over heuristic guessing**.

---

## 🚀 Features

- 📸 **Multimodal Extraction:** Supports scanned invoices, receipts, and complex A4 bills.
- 🧠 **Engine-Agnostic Architecture:** Pluggable engines including Rule-Based, Donut (Vision-Language), and Gemini (Multimodal LLM).
- 🧹 **Advanced Preprocessing:** Uses OpenCV to reduce noise and handle uneven lighting/warped scans.
- 🧾 **ERP-Style Structured JSON:** Outputs strictly validated data compatible with systems like SAP, Oracle, and Odoo.
- 🛑 **Null-Safe Extraction:** Defensive parsing that returns `null` for ambiguous values rather than guessing.
- 🌐 **Real-time Testing:** Full Frontend + Backend integration for immediate validation.

---

## 🏗️ System Architecture

```text
Image Upload (Frontend)
        ↓
Backend API (Flask)
        ↓
Document Understanding Engine
(Rule-Based / Donut / Gemini)
        ↓
Validation & Normalization Layer
        ↓
ERP-Compatible Structured JSON
The system is designed to be engine-agnostic, allowing different extraction strategies to be plugged in without changing the API contract.
````

## 📂 Project Structure
````
erp-invoice-ocr-parser/
│
├── backend/
│   ├── app.py                  # API entry point & Flask routing
│   ├── engines/
│   │   ├── donut/               # Vision-language model (Donut)
│   │   └── gemini/              # Multimodal LLM engine (Final Direction)
│   ├── ocr/
│   │   ├── preprocessing.py     # Image cleaning with OpenCV
│   │   ├── ocr_engine.py        # Tesseract OCR extraction
│   │   ├── document_classifier.py# Layout detection
│   │   └── parser.py            # Rule-based logic & arithmetic validation
│   └── uploads/                 # Temporary storage for processed images
│
├── frontend/                    # Vanilla JS, HTML, CSS interface
├── requirements.txt             # Project dependencies
└── README.md
````
## 🧪 Sample ERP Output
````
JSON
{
  "vendor": {
    "name": "Bhagini",
    "gstin": "29ADDPR8125K1Z2",
    "phone": null
  },
  "invoice": {
    "number": "7767",
    "date": "16 May 2024"
  },
  "items": [
    {
      "name": "Mutton Biriyani",
      "unit_price": 400,
      "quantity": 4,
      "total": 1600
    }
  ],
  "amounts": {
    "subtotal": 3000,
    "tax": 150,
    "grand_total": 3150,
    "currency": "INR"
  }
}

````


Design Principle: If a value cannot be validated with confidence, it is returned as null.

## 🧠 Parsing & Validation Philosophy
Invoice OCR is inherently noisy. This system applies defensive extraction techniques:

Rule-Based Validation Logic
Arithmetic Consistency: Item rows are validated using unit_price × quantity ≈ total.

Right → Left Parsing: Numeric fields are prioritized from the total backward to ensure quantity and price alignment.

Noise Removal: Automatic stripping of OCR artifacts like ₹, commas, and stray symbols before conversion.

Explored Approaches
Rule-Based OCR: High explainability but breaks on layout variance.

Donut (Vision-Language): Eliminates OCR dependency but suffers from inconsistent schema reliability.

Gemini (Multimodal LLM): Final direction; robust to unseen layouts with strict schema enforcement.

## 🛠️ Technology Stack
Backend: Python, Flask, Flask-CORS

Image Processing: OpenCV

OCR: Tesseract

AI Models: Donut (HuggingFace), Gemini 2.5 Flash (Google SDK)

Frontend: HTML5, CSS3, JavaScript (Vanilla)

## ▶️ Running Locally
Clone the repository and install dependencies:

Bash
pip install -r requirements.txt
Setup Gemini API Key: Add your API key to backend/engines/gemini/gemini_engine.py.

Run the backend:

Bash
python backend/app.py
Launch the UI: Open frontend/index.html in any modern web browser.

## 📈 Roadmap
[ ] Confidence scoring per extracted field.

[ ] Hybrid routing (deterministic rules + ML).

[ ] Multi-language invoice support.

[ ] Async batch processing for high-volume uploads.
## 🏁 Final Note
This project reflects real-world document intelligence engineering, not textbook OCR. It focuses on practical decision-making and responsible AI use.

The goal is not to extract everything — the goal is to extract only what can be trusted.

## Screenshots


<img width="1919" height="867" alt="Screenshot 2026-02-05 040109" src="https://github.com/user-attachments/assets/2c276fd7-3c01-405f-8b5e-5324714ce90d" />
<img width="1919" height="860" alt="Screenshot 2026-02-05 040037" src="https://github.com/user-attachments/assets/735bfeb2-bc44-49c1-8a3d-439f35ab0e8c" />
<img width="1918" height="861" alt="Screenshot 2026-02-05 035938" src="https://github.com/user-attachments/assets/2304bffa-f5d2-4c28-938a-16be781e1bdd" />
<img width="1916" height="865" alt="Screenshot 2026-02-05 035855" src="https://github.com/user-attachments/assets/32316fe8-2c8e-41c1-a2af-7a7b38b3337a" />
<img width="1919" height="864" alt="Screenshot 2026-02-05 035755" src="https://github.com/user-attachments/assets/9f7992f2-8664-4d62-9fa5-1c19d8356455" />
<img width="1918" height="854" alt="Screenshot 2026-02-05 040133" src="https://github.com/user-attachments/assets/c47d08cd-9af6-4c16-af2b-45a9339a3fa8" />
