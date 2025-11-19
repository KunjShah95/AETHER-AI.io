from fastapi import FastAPI
from fastapi.responses import HTMLResponse
try:
    from .analytics import AnalyticsManager
except ImportError:
    from analytics import AnalyticsManager
import uvicorn
import threading

app = FastAPI()
analytics = AnalyticsManager()

@app.get("/", response_class=HTMLResponse)
def read_root():
    stats = analytics.get_stats()
    html_content = """
    <html>
        <head>
            <title>Aether AI Dashboard</title>
            <style>
                body { font-family: 'Segoe UI', sans-serif; background: #0d1117; color: #c9d1d9; padding: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .card { background: #161b22; padding: 25px; margin-bottom: 20px; border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
                h1 { color: #58a6ff; margin-bottom: 30px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
                h2 { color: #7ee787; margin-top: 0; }
                ul { list-style: none; padding: 0; }
                li { padding: 10px 0; border-bottom: 1px solid #21262d; display: flex; justify-content: space-between; }
                li:last-child { border-bottom: none; }
                .count { background: #238636; color: white; padding: 2px 10px; border-radius: 12px; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Aether AI Analytics Dashboard</h1>
                <div class="card">
                    <h2>📊 Command Usage Stats</h2>
                    <ul>
    """
    if not stats:
        html_content += "<li>No data available yet.</li>"
    else:
        for cmd, count in stats.items():
            html_content += f"<li><span>{cmd}</span> <span class='count'>{count}</span></li>"
    
    html_content += """
                    </ul>
                </div>
                <div class="card">
                    <h2>ℹ️ System Info</h2>
                    <p>Status: <strong>Online</strong></p>
                    <p>Version: <strong>3.0</strong></p>
                </div>
            </div>
        </body>
    </html>
    """
    return html_content

def start_dashboard(port=8000):
    """Start the dashboard in a separate thread"""
    def run():
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
    
    t = threading.Thread(target=run, daemon=True)
    t.start()
    print(f"📊 Dashboard started at http://localhost:{port}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
