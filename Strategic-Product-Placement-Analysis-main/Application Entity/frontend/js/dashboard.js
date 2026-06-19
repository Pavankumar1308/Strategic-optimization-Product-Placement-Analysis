async function loadDashboard() {
  try {
    const summary = await apiRequest("/data/analytics/summary");
    renderChart("chartCategory", summary.map(r => r.category), summary.map(r => r.avg_sales), "Avg Sales Volume");

    const byPosition = await apiRequest("/data/analytics/by-position");
    renderChart("chartPosition", byPosition.map(r => r.position), byPosition.map(r => r.avg_sales), "Avg Sales by Position");

    const byTraffic = await apiRequest("/data/analytics/foot-traffic");
    renderChart("chartFootTraffic", byTraffic.map(r => r.foot_traffic), byTraffic.map(r => r.avg_sales), "Avg Sales by Foot Traffic");
  } catch (e) {
    console.warn("Login required to view dashboard data:", e.message);
  }
}

function renderChart(canvasId, labels, data, label) {
  const ctx = document.getElementById(canvasId);
  new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label,
        data,
        backgroundColor: ["#6c5ce7", "#00cec9", "#fdcb6e", "#e17055"],
      }],
    },
    options: { responsive: true, plugins: { legend: { display: false } } },
  });
}

window.addEventListener("DOMContentLoaded", loadDashboard);
