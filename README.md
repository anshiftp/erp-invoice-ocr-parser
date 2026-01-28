# 🧾 ERP Invoice OCR Parser

A **rule-based OCR invoice parser** that converts scanned bills and receipts into **structured ERP-style JSON**, supporting restaurant and grocery invoices.

This project focuses on **robust text normalization, document classification, and fault-tolerant item extraction** from noisy OCR output.

---

## 🚀 Features

- 📸 Image upload (bills / receipts)
- 🧠 OCR using **Tesseract**
- 🧹 Image preprocessing with **OpenCV**
- 🧾 Automatic **document type detection**
- 📦 Rule-based parsing into **ERP-style JSON**
- 🧮 Line-item extraction (name, unit price, quantity, total)
- 💰 Subtotal, tax (CGST / SGST), and grand total extraction
- 🛑 Graceful failure (returns `null` instead of incorrect values)
- 🌐 Frontend + Backend integration

---

## 🏗️ Architecture Overview

```text
Image Upload
   ↓
Image Preprocessing (OpenCV)
   ↓
OCR Extraction (Tesseract)
   ↓
Document Classification
   ↓
Rule-Based Parsing
   ↓
Structured ERP JSON Output

```
---

## 📂 Project Structure
```text

erp-invoice-ocr-parser/
│
├── backend/
│   ├── app.py
│   ├── ocr/
│   │   ├── preprocessing.py
│   │   ├── ocr_engine.py
│   │   ├── document_classifier.py
│   │   ├── parser.py
│   │   └── __init__.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── sample_images/
│   ├── restaurant_receipt.jpg
│   ├── grocery_bill.jpg
│   └── fuel_invoice.jpg
│
├── requirements.txt
├── README.md
└── .gitignore
```
---

## 🧪 Sample Output (ERP-Style)

```json
{
  "document_type": "restaurant",
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
      "name": "Mutton biriyani",
      "unit_price": 400,
      "quantity": 4,
      "total": 1600
    },
    {
      "name": "Tandoori Roti",
      "unit_price": 30,
      "quantity": 5,
      "total": 150
    }
  ],
  "amounts": {
    "subtotal": 3000,
    "tax": 150,
    "grand_total": 3150,
    "currency": "INR"
  }
}

```
## 🧠 Parsing Strategy (Important)
OCR output is noisy and inconsistent, so this project uses a defensive, rule-based approach.

Item Extraction Logic
Reads numeric values right → left (total → quantity → unit price)

Removes OCR noise (₹, X, commas, stray symbols)

Extracts item name by removing numeric tokens

Validates rows using:

unit_price × quantity ≈ total
Rejects invalid or ambiguous lines to prevent false positives

This approach ensures ERP-safe structured output even with imperfect OCR data.

## 🛠️ Tech Stack
Python

Flask

Flask-CORS

OpenCV

Tesseract OCR

HTML / CSS / JavaScript

## ▶️ How to Run Locally
1️⃣ Install dependencies

pip install -r requirements.txt

2️⃣ Install Tesseract OCR
Windows

Download from: https://github.com/UB-Mannheim/tesseract/wiki

Add Tesseract to system PATH

3️⃣ Run backend

python backend/app.py

4️⃣ Open frontend

Open frontend/index.html in your browser.

## ⚠️ Limitations
Rule-based (no ML training)

Accuracy depends on OCR quality

Highly complex tabular invoices may require additional heuristics

## 📌 Why Rule-Based?
This project intentionally avoids ML-based parsing to:

Maintain explainability

Avoid training data dependency

Ensure predictable and safe ERP outputs

Handle edge cases deterministically

## 📈 Future Improvements
ML-assisted line-item detection

Confidence scoring for extracted fields

Multi-language OCR support

Export to CSV / Excel

Database persistence

## 🙌 Final Note
This project demonstrates real-world OCR handling, not textbook perfection.
It focuses on robust engineering, defensive parsing, and production-safe outputs — exactly what ERP systems require.

