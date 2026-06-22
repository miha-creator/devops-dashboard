from flask import Flask, jsonify, render_template_string
import docker
import datetime

app = Flask(__name__)
client = docker.from_env()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Dashboard</title>
    <meta http-equiv="refresh" content="10">
    <style>
        body { font-family: monospace; background: #1e1e1e; color: #d4d4d4; padding: 2rem; }
        h1 { color: #569cd6; }
        .container { max-width: 800px; margin: 0 auto; }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th { background: #2d2d2d; padding: 10px; text-align: left; color: #9cdcfe; }
        td { padding: 10px; border-bottom: 1px solid #3a3a3a; }
        .running { color: #4ec9b0; }
        .exited  { color: #f44747; }
        .footer  { margin-top: 2rem; color: #6a6a6a; font-size: 0.8rem; }
    </style>
</head>
<body>
<div class="container">
    <h1>🖥 DevOps Dashboard</h1>
    <p>Updated: {{ updated }}</p>
    <table>
        <tr><th>Container</th><th>Image</th><th>Status</th><th>Ports</th></tr>
        {% for c in containers %}
        <tr>
            <td>{{ c.name }}</td>
            <td>{{ c.image }}</td>
            <td class="{{ c.status }}">{{ c.status }}</td>
            <td>{{ c.ports }}</td>
        </tr>
        {% endfor %}
    </table>
    <div class="footer">Auto-refresh every 10 seconds</div>
</div>
</body>
</html>
"""

def get_containers():
    result = []
    for c in client.containers.list(all=True):
        ports = ", ".join(
            f"{v[0]['HostPort']}" 
            for v in c.ports.values() 
            if v
        ) if c.ports else "—"
        result.append({
            "name": c.name,
            "image": c.image.tags[0] if c.image.tags else "—",
            "status": c.status,
            "ports": ports,
        })
    return result

@app.route("/")
def index():
    return render_template_string(HTML,
        containers=get_containers(),
        updated=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@app.route("/api/containers")
def api_containers():
    return jsonify(get_containers())

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
