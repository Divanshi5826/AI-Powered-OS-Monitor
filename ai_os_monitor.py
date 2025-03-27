from flask import Flask, render_template, jsonify
import psutil
import random
import time
app = Flask(__name__)
previous_net_io = psutil.net_io_counters()
previous_time = time.time()
def get_network_speed():
    global previous_net_io, previous_time
    current_net_io = psutil.net_io_counters()
    current_time = time.time()
    time_diff = current_time - previous_time
    if time_diff == 0:
        return {"upload_speed": 0.0, "download_speed": 0.0}
    upload_speed = (current_net_io.bytes_sent - previous_net_io.bytes_sent) / time_diff / 1024 / 1024
    download_speed = (current_net_io.bytes_recv - previous_net_io.bytes_recv) / time_diff / 1024 / 1024
    previous_net_io = current_net_io
    previous_time = current_time
    return {
        "upload_speed": round(upload_speed, 2),
        "download_speed": round(download_speed, 2)
    }
def get_heavy_processes(threshold=20):
    heavy_process = None
    max_cpu = 0
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
        try:
            pid = proc.info['pid']
            cpu_usage = min(proc.info['cpu_percent'], 100)  # Ensure no process exceeds 100%

            if pid != 0 and cpu_usage > threshold:  # Ignore System Idle Process
                if cpu_usage > max_cpu:
                    max_cpu = cpu_usage
                    heavy_process = proc.info
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue  # Ignore inaccessible processes
    if heavy_process:
        return (f"🚀 {heavy_process['name']} (PID: {heavy_process['pid']}) "
                f"is using high CPU ({max_cpu}%). Consider closing it.")
    return None
@app.route('/stats')
def get_stats():
    network_speeds = get_network_speed()
    return jsonify({
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "upload_speed": network_speeds["upload_speed"],
        "download_speed": network_speeds["download_speed"]
    })
@app.route('/ai-stats')
def get_ai_stats():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    network_speeds = get_network_speed()
    predicted_cpu = round(max(0, min(100, cpu + random.uniform(-3, 3))), 1)
    predicted_memory = round(max(0, min(100, memory + random.uniform(-3, 3))), 1)
    predicted_disk = round(max(0, min(100, disk + random.uniform(-3, 3))), 1)
    anomaly_alert = "⚠ High resource usage detected!" if (cpu > 90 or memory > 90 or disk > 90) else None
    optimization_suggestion = None
    if memory > 80:
        optimization_suggestion = "🛑 Close unused applications to free up memory."
    elif disk > 80:
        optimization_suggestion = "🗑 Consider cleaning unnecessary files to free disk space."
    heavy_process_info = get_heavy_processes()
    energy_score = round(random.uniform(1, 10), 1)
    if cpu > 80 or memory > 80:
        overload_time = round(random.uniform(5, 30), 1)  # Predict overload in next 5-30 minutes
        overload_prediction = f"⚡ System may overload in {overload_time} minutes if usage continues."
    else:
        overload_prediction = "✅ System is running optimally."
    return jsonify({
        "predicted_cpu": predicted_cpu,
        "predicted_memory": predicted_memory,
        "predicted_disk": predicted_disk,
        "anomaly_alert": anomaly_alert,
        "optimization_suggestion": optimization_suggestion,
        "heavy_process_info": heavy_process_info,
        "energy_efficiency_score": energy_score,
        "upload_speed": network_speeds["upload_speed"],
        "download_speed": network_speeds["download_speed"],
        "overload_prediction": overload_prediction
    })
@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)