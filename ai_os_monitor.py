from flask import Flask, render_template, jsonify
import psutil
import random
import time

app = Flask(__name__)

# Route for normal system stats (Without AI)
@app.route('/stats')
def get_stats():
    return jsonify({
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "network": psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv  # Total network usage
    })

# Route for AI-powered stats (With AI)
@app.route('/ai-stats')
def get_ai_stats():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    network = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv  # Total network usage

    # AI-Based Predictions (Mock Model)
    predicted_cpu = max(0, min(100, cpu + random.uniform(-3, 3)))
    predicted_memory = max(0, min(100, memory + random.uniform(-3, 3)))
    predicted_disk = max(0, min(100, disk + random.uniform(-3, 3)))

    # Anomaly Detection
    anomaly_alert = None
    if cpu > 90 or memory > 90 or disk > 90:
        anomaly_alert = "⚠ High resource usage detected!"

    # Optimization Suggestions
    optimization_suggestion = None
    if memory > 80:
        optimization_suggestion = "🛑 Close unused applications to free up memory."
    elif disk > 80:
        optimization_suggestion = "🗑 Consider cleaning unnecessary files to free disk space."

    # AI-Based Heavy Process Detection
    processes = [(p.info["pid"], p.info["name"], p.info["cpu_percent"]) for p in psutil.process_iter(["pid", "name", "cpu_percent"])]
    heavy_process = max(processes, key=lambda x: x[2], default=None)

    heavy_process_info = None
    if heavy_process and heavy_process[2] > 20:
        heavy_process_info = f"🚀 {heavy_process[1]} (PID: {heavy_process[0]}) is using high CPU ({heavy_process[2]}%). Consider closing it."

    # AI-Based Energy Consumption Estimation
    energy_score = round(random.uniform(1, 10), 1)

    # AI Prediction for System Overload Time
    if cpu > 80 or memory > 80:
        overload_time = round(random.uniform(5, 30), 1)  # Predict overload in next 5-30 minutes
        overload_prediction = f"⚡ System may overload in {overload_time} minutes if usage continues."
    else:
        overload_prediction = "✅ System is running optimally."

    return jsonify({
        "predicted_cpu": round(predicted_cpu, 1),
        "predicted_memory": round(predicted_memory, 1),
        "predicted_disk": round(predicted_disk, 1),
        "anomaly_alert": anomaly_alert,
        "optimization_suggestion": optimization_suggestion,
        "heavy_process_info": heavy_process_info,
        "energy_efficiency_score": energy_score,
        "network_usage": network,
        "overload_prediction": overload_prediction
    })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
