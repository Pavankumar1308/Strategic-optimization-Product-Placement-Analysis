async function predictSales() {
  const payload = {
    "Product Category": document.getElementById("p-category").value,
    "Product Position": document.getElementById("p-position").value,
    "Promotion": document.getElementById("p-promotion").value,
    "Foot Traffic": document.getElementById("p-foot-traffic").value,
    "Consumer Demographics": document.getElementById("p-demographic").value,
    "Seasonal": document.getElementById("p-seasonal").value,
    "Price": parseFloat(document.getElementById("p-price").value || 0),
    "Competitor's Price": parseFloat(document.getElementById("p-competitor-price").value || 0),
  };

  try {
    const data = await apiRequest("/predict/sales", "POST", payload);
    document.getElementById("prediction-result").innerText =
      `Predicted Sales Volume: ${data.predicted_sales_volume}`;
  } catch (e) {
    document.getElementById("prediction-result").innerText = `Error: ${e.message}`;
  }
}
