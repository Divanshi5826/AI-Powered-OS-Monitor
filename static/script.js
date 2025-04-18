const ctx = document.getElementById("usageChart").getContext("2d");
const aiCtx = document.getElementById("aiChart").getContext("2d");
const networkCtx = document.getElementById("networkChart").getContext("2d");
const chart = new Chart(ctx, {
    type: "line",
    data: {
        labels: [],
        datasets: [
            { label: "CPU Usage", borderColor: "red", data: [], fill: false },
            { label: "Memory Usage", borderColor: "blue", data: [], fill: false },
            { label: "Disk Usage", borderColor: "green", data: [], fill: false }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y: { min: 0, max: 100 }
        }
    }
});
const aiChart = new Chart(aiCtx, {
    type: "line",
    data: {
        labels: [],
        datasets: [
            { label: "Predicted CPU Usage", borderColor: "purple", data: [], fill: false },
            { label: "Predicted Memory Usage", borderColor: "orange", data: [], fill: false },
            { label: "Predicted Disk Usage", borderColor: "teal", data: [], fill: false }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y: { min: 0, max: 100 }
        }
    }
});
const networkChart = new Chart(networkCtx, {
    type: "line",
    data: {
        labels: [],
        datasets: [
            { label: "Upload Speed (Mbps)", borderColor: "blue", data: [], fill: false },
            { label: "Download Speed (Mbps)", borderColor: "green", data: [], fill: false }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y: { min: 0 }
        }
    }
});
function fetchStats() {
    fetch("/stats")
        .then(response => response.json())
        .then(data => {
            document.getElementById("cpu").innerText = data.cpu;
            document.getElementById("memory").innerText = data.memory;
            document.getElementById("disk").innerText = data.disk;
            document.getElementById("upload-speed").innerText = data.upload_speed;
            document.getElementById("download-speed").innerText = data.download_speed;
            const timeLabel = new Date().toLocaleTimeString();
            chart.data.labels.push(timeLabel);
            chart.data.datasets[0].data.push(data.cpu);
            chart.data.datasets[1].data.push(data.memory);
            chart.data.datasets[2].data.push(data.disk);
            networkChart.data.labels.push(timeLabel);
            networkChart.data.datasets[0].data.push(data.upload_speed);
            networkChart.data.datasets[1].data.push(data.download_speed);
            if (chart.data.labels.length > 20) {
                chart.data.labels.shift();
                chart.data.datasets.forEach(dataset => dataset.data.shift());
            }
            if (networkChart.data.labels.length > 20) {
                networkChart.data.labels.shift();
                networkChart.data.datasets.forEach(dataset => dataset.data.shift());
            }
            chart.update();
            networkChart.update();
        })
        .catch(error => console.error("Error fetching stats:", error));
}
function fetchAIStats() {
    fetch("/ai-stats")
        .then(response => response.json())
        .then(data => {
            document.getElementById("ai_cpu").innerText = data.predicted_cpu;
            document.getElementById("ai_memory").innerText = data.predicted_memory;
            document.getElementById("ai_disk").innerText = data.predicted_disk;
            document.getElementById("anomaly-alert").innerText = data.anomaly_alert || "";
            document.getElementById("optimization-suggestion").innerText = data.optimization_suggestion || "";
            document.getElementById("heavy-process").innerText = data.heavy_process_info || "No high usage process detected";
            document.getElementById("energy-score").innerText = `🔋 Energy Score: ${data.energy_efficiency_score}/10`;
            document.getElementById("overload-prediction").innerText = data.overload_prediction;
            const timeLabel = new Date().toLocaleTimeString();
            aiChart.data.labels.push(timeLabel);
            aiChart.data.datasets[0].data.push(data.predicted_cpu);
            aiChart.data.datasets[1].data.push(data.predicted_memory);
            aiChart.data.datasets[2].data.push(data.predicted_disk);
            if (aiChart.data.labels.length > 20) {
                aiChart.data.labels.shift();
                aiChart.data.datasets.forEach(dataset => dataset.data.shift());
            }
            aiChart.update();
        })
        .catch(error => console.error("Error fetching AI stats:", error));
}
setInterval(fetchStats, 2000);
setInterval(fetchAIStats, 2000);
fetchStats();
fetchAIStats();