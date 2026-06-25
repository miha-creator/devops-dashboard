from flask import Flask, jsonify, render_template_string
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import datetime
import os

app = Flask(__name__)

REQUEST_COUNT = Counter('dashboard_requests_total', 'Total requests to dashboard')

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Dashboard</title>
    <meta http-equiv="refresh" content="10">
    <style>
        body { font-family: monospace; background: #1e1e1e; color: #d4d4d4; padding: 2rem; }
        h1 { color: #569cd6; }
        .container { max-width: 900px; margin: 0 auto; }
        .badge { padding: 4px 10px; border-radius: 4px; background: #2d2d2d; }
        .links a { color: #569cd6; margin-right: 1rem; }
        .footer { margin-top: 2rem; color: #6a6a6a; font-size: 0.8rem; }
        .info { background: #2d2d2d; padding: 1rem; border-radius: 4px; margin-top: 1rem; }
        .info p { margin: 0.3rem 0; }
    </style>
</head>
<body>
<div class="container">
    <h1>🖥 DevOps Dashboard</h1>
    <p>Updated: {{ updated }}</p>
    <div class="links">
        <a href="/metrics">📊 Prometheus Metrics</a>
        <a href="/api/info">🔌 API</a>
        <a href="/health">❤️ Health</a>
    </div>
    <div class="info">
        <p>🚀 <b>Running in Kubernetes</b></p>
        <p>📦 Pod: {{ pod_name }}</p>
        <p>🌐 Namespace: {{ namespace }}</p>
        <p>🔢 Version: {{ version }}</p>
    </div>
    <div class="footer">Auto-refresh every 10 seconds</div>
</div>
</body>
</html>
"""

@app.route("/")
def index():
    REQUEST_COUNT.inc()
    return render_template_string(HTML,
        updated=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        pod_name=os.environ.get("POD_NAME", "unknown"),
        namespace=os.environ.get("POD_NAMESPACE", "default"),
        version=os.environ.get("APP_VERSION", "1.0.0"),
    )

@app.route("/api/info")
def api_info():
    return jsonify({
        "pod": os.environ.get("POD_NAME", "unknown"),
        "namespace": os.environ.get("POD_NAMESPACE", "default"),
        "version": os.environ.get("APP_VERSION", "1.0.0"),
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
