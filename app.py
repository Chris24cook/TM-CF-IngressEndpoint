import os
import time
import json
import subprocess
import platform
import re
from flask import Flask, Response

app = Flask(__name__)
START_TIME = time.time()

MONITORED_HOSTS = [
    {'name': 'Google DNS', 'host': '8.8.8.8'},
    {'name': 'Cloudflare DNS', 'host': '1.1.1.1'},
    {'name': 'Microsoft Azure', 'host': '13.107.42.14'},
    {'name': 'AWS', 'host': '52.94.236.248'},
]

def ping_host(host):
    param = '-c' if platform.system().lower() != 'windows' else '-n'
    command = ['ping', param, '1', '-W', '2', host]
    try:
        start = time.time()
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True, timeout=5)
        elapsed = (time.time() - start) * 1000
        match = re.search(r'time[=<](d+.?d*)s*ms', output)
        response_time = float(match.group(1)) if match else round(elapsed, 2)
        return {'status': 'online', 'response_time': round(response_time, 2), 'reachable': True}
    except:
        return {'status': 'offline', 'response_time': None, 'reachable': False}

def get_routes():
    try:
        if platform.system().lower() == 'windows':
            output = subprocess.check_output(['route', 'print'], universal_newlines=True, timeout=10)
        else:
            output = subprocess.check_output(['ip', 'route'], universal_newlines=True, timeout=10)
        return output
    except Exception as e:
        return f'Route info unavailable: {str(e)}'

@app.route('/')
def dashboard():
    region = os.environ.get('REGION', 'UK South')
    results = []
    for h in MONITORED_HOSTS:
        r = ping_host(h['host'])
        r['name'] = h['name']
        r['host'] = h['host']
        results.append(r)
    
    routes = get_routes()
    uptime = round(time.time() - START_TIME, 2)
    
    hosts_html = ''
    for r in results:
        status_class = 'online' if r['reachable'] else 'offline'
        time_display = f"{r['response_time']} ms" if r['reachable'] else 'Unreachable'
        time_class = 'slow' if r['reachable'] and r['response_time'] > 100 else ''
        hosts_html += f'''
        <div class="host-card">
            <div class="host-header">
                <span class="status-dot {status_class}"></span>
                <span class="host-name">{r['name']}</span>
            </div>
            <div class="host-ip">{r['host']}</div>
            <div class="response-time {status_class} {time_class}">{time_display}</div>
        </div>'''
    
    return f'''
<!DOCTYPE html>
<html>
<head>
    <title>Network Dashboard - {region}</title>
    <meta http-equiv="refresh" content="30">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .region-badge {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .region-badge span {{
            background: #667eea;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 1em;
        }}
        .stats-bar {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        .stat {{
            background: rgba(255,255,255,0.1);
            padding: 15px 25px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-value {{ font-size: 1.8em; font-weight: bold; color: #10b981; }}
        .stat-label {{ color: #9ca3af; font-size: 0.9em; }}
        .section {{ margin-bottom: 30px; }}
        .section-title {{
            font-size: 1.3em;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .hosts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }}
        .host-card {{
            background: rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 20px;
            border-left: 4px solid #667eea;
        }}
        .host-header {{ display: flex; align-items: center; margin-bottom: 8px; }}
        .status-dot {{
            width: 12px; height: 12px;
            border-radius: 50%;
            margin-right: 10px;
        }}
        .status-dot.online {{ background: #10b981; box-shadow: 0 0 10px #10b981; }}
        .status-dot.offline {{ background: #ef4444; box-shadow: 0 0 10px #ef4444; }}
        .host-name {{ font-weight: bold; font-size: 1.1em; }}
        .host-ip {{ color: #9ca3af; font-size: 0.9em; margin-bottom: 10px; }}
        .response-time {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }}
        .response-time.online {{ background: rgba(16,185,129,0.2); color: #10b981; }}
        .response-time.offline {{ background: rgba(239,68,68,0.2); color: #ef4444; }}
        .response-time.slow {{ background: rgba(245,158,11,0.2); color: #f59e0b; }}
        .routes-box {{
            background: #0d1117;
            border-radius: 10px;
            padding: 20px;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            color: #10b981;
            overflow-x: auto;
            white-space: pre;
            max-height: 300px;
            overflow-y: auto;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #6b7280;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Network Dashboard</h1>
        <div class="region-badge"><span>CC Endpoint {region}</span></div>
        
        <div class="stats-bar">
            <div class="stat">
                <div class="stat-value">{len([r for r in results if r['reachable']])}/{len(results)}</div>
                <div class="stat-label">Hosts Online</div>
            </div>
            <div class="stat">
                <div class="stat-value">{round(sum(r['response_time'] for r in results if r['reachable']) / max(1, len([r for r in results if r['reachable']])), 1)} ms</div>
                <div class="stat-label">Avg Response</div>
            </div>
            <div class="stat">
                <div class="stat-value">{uptime}s</div>
                <div class="stat-label">Uptime</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Ping Status</div>
            <div class="hosts-grid">{hosts_html}</div>
        </div>
        
        <div class="section">
            <div class="section-title">Route Table</div>
            <div class="routes-box">{routes}</div>
        </div>
        
        <div class="footer">Auto-refreshes every 30 seconds | Last update: {time.strftime('%H:%M:%S')}</div>
    </div>
</body>
</html>
'''

@app.route('/health')
def health():
    data = {
        'status': 'healthy',
        'uptime_seconds': round(time.time() - START_TIME, 2),
        'region': os.environ.get('REGION', 'UK South')
    }
    return Response(json.dumps(data), mimetype='application/json')

@app.route('/api/ping')
def api_ping():
    results = []
    for h in MONITORED_HOSTS:
        r = ping_host(h['host'])
        r['name'] = h['name']
        r['host'] = h['host']
        results.append(r)
    return Response(json.dumps(results), mimetype='application/json')

@app.route('/api/routes')
def api_routes():
    return Response(json.dumps({'routes': get_routes()}), mimetype='application/json')

application = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
