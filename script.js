// frontend/script.js
document.getElementById('controlForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const runButton = document.querySelector('button[type="submit"]');
    const originalButtonText = runButton.textContent;
    runButton.disabled = true;
    runButton.textContent = 'Processing...';
    
    try {
        const city = document.getElementById('citySelect').value;
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;
        const model = document.getElementById('modelSelect').value;
        const k = parseInt(document.getElementById('kValue').value);

        if (!city || !startDate || !endDate || isNaN(k)) {
            throw new Error('Please fill all fields with valid values');
        }

        // Call Forecast API
        const forecastRes = await fetch('http://localhost:5000/api/forecast', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                city, 
                start_date: startDate, 
                end_date: endDate, 
                model, 
                params: { lookback: 24 } 
            })
        });
        
        if (!forecastRes.ok) {
            const errorData = await forecastRes.json();
            throw new Error(errorData.error || 'Forecast API failed');
        }
        
        const forecastData = await forecastRes.json();
        Plotly.newPlot('forecastPlot', forecastData.plotly_data, forecastData.layout);

        // 🔹 Display summary bullet list
        if (forecastData.summary && Array.isArray(forecastData.summary)) {
            const summaryHtml = forecastData.summary.map(item => `<li>${item}</li>`).join("");
            document.getElementById('predictionList').innerHTML = `
                <h5>Next 2–3 Days Forecast (Hourly)</h5>
                <ul>${summaryHtml}</ul>
            `;
        } else {
            document.getElementById('predictionList').innerHTML = "<p>No summary available.</p>";
        }

        // Call Cluster API
        const clusterRes = await fetch('http://localhost:5000/api/cluster', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ city, start_date: startDate, end_date: endDate, k })
        });
        
        if (!clusterRes.ok) {
            const errorData = await clusterRes.json();
            throw new Error(errorData.error || 'Cluster API failed');
        }
        
        const clusterData = await clusterRes.json();
        Plotly.newPlot('clusterPlot', clusterData.plotly_data, clusterData.layout);
        
    } catch (error) {
        alert(`Error: ${error.message}`);
        console.error(error);
    } finally {
        runButton.disabled = false;
        runButton.textContent = originalButtonText;
    }
});

// Set default dates to today and tomorrow
window.addEventListener('DOMContentLoaded', () => {
    const today = new Date().toISOString().split('T')[0];
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const tomorrowStr = tomorrow.toISOString().split('T')[0];
    
    document.getElementById('startDate').value = today;
    document.getElementById('endDate').value = tomorrowStr;
});
