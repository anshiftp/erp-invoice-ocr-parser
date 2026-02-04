    async function uploadBill() {
    const fileInput = document.getElementById("billImage");
    const previewImage = document.getElementById("previewImage");
    const billDetails = document.getElementById("bill-details");

    if (!fileInput.files.length) {
        alert("Please select an image first.");
        return;
    }

    const file = fileInput.files[0];

    // Image preview
    const reader = new FileReader();
    reader.onload = () => {
        previewImage.src = reader.result;
    };
    reader.readAsDataURL(file);

    // 🔥 Send image to Flask backend
    const formData = new FormData();
    formData.append("image", file);

    try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        //renderBillDetails(data);

           // ✅ SHOW RAW OCR TEXT and STRUCTURED DATA
       const items = data.structured_data?.items || [];

billDetails.innerHTML = `
  <h4>Raw OCR Output</h4>
  <pre>${JSON.stringify(data.raw_donut_output, null, 2)}</pre>

  <h4>Structured Output</h4>

  <p><strong>Vendor Name:</strong> 
    ${data.structured_data?.vendor?.name || "Not found"}
  </p>

  <p><strong>GSTIN:</strong> 
    ${data.structured_data?.vendor?.gstin || "Not found"}
  </p>

  <p><strong>Invoice Number:</strong> 
    ${data.structured_data?.invoice?.number || "Not found"}
  </p>

  <p><strong>Date:</strong> 
    ${data.structured_data?.invoice?.date || "Not found"}
  </p>

  ${
    items.length > 0
      ? `
        <h4>Items</h4>
        <table>
          <tr>
            <th>Item</th>
            <th>Unit Price</th>
            <th>Qty</th>
            <th>Total</th>
          </tr>
          ${items
            .map(
              item => `
                <tr>
                  <td>${item.name}</td>
                  <td>₹${item.unit_price}</td>
                  <td>${item.quantity}</td>
                  <td>₹${item.total}</td>
                </tr>
              `
            )
            .join("")}
        </table>
      `
      : "<p><strong>Items:</strong> Not found</p>"
  }

  <p><strong>Subtotal:</strong> 
    ₹${data.structured_data?.amounts?.subtotal || "Not found"}
  </p>

  <p><strong>Tax:</strong> 
    ₹${data.structured_data?.amounts?.tax || "Not found"}
  </p>

  <p><strong>Total:</strong> 
    ₹${data.structured_data?.amounts?.grand_total || "Not found"}
  </p>
`;


  } catch (error) {
    console.error("FRONTEND ERROR:", error);
    alert(error.message);
}

}