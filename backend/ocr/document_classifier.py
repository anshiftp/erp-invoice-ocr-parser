
# Detects document type based on OCR content.

def detect_document_type(text):
 
    text = text.lower()

    if "petrol" in text or "fuel" in text or "diesel" in text:
        return "fuel_receipt"

    if "gst" in text or "invoice no" in text:
        return "tax_invoice"

    if "food" in text or "hotel" in text or "restaurant" in text:
        return "restaurant"

    return "receipt"
