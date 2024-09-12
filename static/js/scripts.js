alert("assd");
document.getElementById("predict-form").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const region = document.getElementById("region").value;
    const month = document.getElementById("month").value;
    const population = document.getElementById("population").value;
    const prev_demand = document.getElementById("prev_demand").value;

    const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ region: parseInt(region), month: parseInt(month), population: parseInt(population), prev_demand: parseInt(prev_demand) })
    });

    const result = await response.json();
    document.getElementById("predicted-value").textContent = result.predicted_demand;
});