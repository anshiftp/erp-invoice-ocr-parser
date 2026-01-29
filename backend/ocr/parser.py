
# Converts raw OCR text into structured, ERP-style invoice data.

import re
from typing import List, Dict
from ocr.document_classifier import detect_document_type

# MAIN ENTRY POINT

def parse_bill_text(text: str) -> Dict:
    lines = normalize_lines(text)
    joined_text = " ".join(lines)

    doc_type = detect_document_type(joined_text)

    vendor = extract_vendor(lines)
    invoice = extract_invoice(lines)

    # Pass doc_type but don't strictly enforce it inside the function
    items = extract_items(lines, doc_type)
    print("FINAL ITEMS:", items)

    amounts = extract_amounts(lines)

    return {
        "document_type": doc_type,
        "vendor": vendor,
        "invoice": invoice,
        "items": items,
        "amounts": amounts,
    }

# NORMALIZATION

def normalize_lines(text: str) -> List[str]:
    lines = []
    for line in text.split("\n"):
        line = line.strip()
        if len(line) < 3:
            continue
        # Allow basic punctuation and currency symbols
        line = re.sub(r"[^\w₹€$.,:/\- ]+", "", line)
        lines.append(line)
    return lines


# VENDOR EXTRACTION

def extract_vendor(lines: List[str]) -> Dict:
    name = None
    gstin = None
    phone = None

    for i, line in enumerate(lines[:12]):
        # GSTIN regex
        gst_match = re.search(r"\b\d{2}[A-Z]{5}\d{4}[A-Z]\wZ\w\b", line)
        if gst_match:
            gstin = gst_match.group()

        # Phone regex
        phone_match = re.search(r"\b\d{10}\b", line)
        if phone_match:
            phone = phone_match.group()

        # Vendor name heuristics
        if not name:
            if (
                i < 3
                and not re.search(r"\d", line)
                and len(line) > 5
                and not any(k in line.lower() for k in ["gst", "invoice", "sale receipt", "date"])
            ):
                name = line

    return {
        "name": name,
        "gstin": gstin,
        "phone": phone,
    }


# INVOICE + DATE

def extract_invoice(lines: List[str]) -> Dict:
    invoice_no = None
    date = None

    for line in lines:
        inv_match = re.search(
            r"(invoice|bill)\s*(no|number)?\s*[:\-]?\s*([A-Z0-9\-]+)",
            line,
            re.IGNORECASE,
        )
        if inv_match and not invoice_no:
            invoice_no = inv_match.group(3)

        date_match = re.search(
            r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{1,2}\s+[A-Za-z]{3,}\s+\d{4}\b",
            line,
        )
        if date_match and not date:
            date = date_match.group()

    return {
        "number": invoice_no,
        "date": date,
    }


# ITEM EXTRACTION (FIXED)

def extract_items(lines: List[str], doc_type: str) -> List[Dict]:
    """
    Robust OCR-safe item extractor.
    """
    items = []


    for line in lines:
        original = line.lower()

        # ❌ Skip non-item lines early
        if any(k in original for k in [
            "subtotal", "total", "cgst", "sgst", "tax",
            "cash", "amount", "invoice", "date", "gst", "table"
        ]):
            continue

        clean = (
            line.replace("₹", "")
                .replace("X", " ")
                .replace("x", " ")
                .replace(",", "")  # Handle commas in prices (e.g., 1,600)
        )

        # Extract ALL numbers from the line
        numbers = re.findall(r"\d+", clean)

        # Need at least price, qty, total
        if len(numbers) < 3:
            continue

        try:
            total = float(numbers[-1])
            quantity = float(numbers[-2])
            unit_price = float(numbers[-3])
        except ValueError:
            continue

        # Extract name by removing numbers
        name = re.sub(r"\d+", "", clean).strip()

        # Reject garbage names
        if len(name) < 3:
            continue

        # Logical validation (VERY important)
        if abs((unit_price * quantity) - total) > 1.0:
            continue

        items.append({
            "name": name,
            "unit_price": int(unit_price) if unit_price.is_integer() else unit_price,
            "quantity": int(quantity) if quantity.is_integer() else quantity,
            "total": int(total) if total.is_integer() else total,
        })

    return items


# AMOUNTS

def extract_amounts(lines: List[str]) -> Dict:
    subtotal = None
    total = None
    tax = 0

    # Subtotal
    for line in lines:
        if "sub" in line.lower():
            m = re.search(r"₹?\s*(\d{2,7})", line)
            if m:
                subtotal = int(m.group(1))

    # CGST / SGST
    for line in lines:
        if "cgst" in line.lower() or "sgst" in line.lower():
            m = re.search(r"₹?\s*(\d+)", line)
            if m:
                tax += int(m.group(1))

    # Final total (bottom-most)
    for line in reversed(lines):
        if any(k in line.lower() for k in ["total", "cash", "amount payable"]):
            m = re.search(r"₹?\s*(\d{2,7})", line)
            if m:
                total = int(m.group(1))
                break

    # Fallback tax
    if tax == 0 and subtotal and total:
        tax = total - subtotal

    return {
        "subtotal": subtotal,
        "tax": tax if tax else None,
        "grand_total": total,
        "currency": "INR",
    }