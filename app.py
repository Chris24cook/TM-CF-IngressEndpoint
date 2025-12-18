import os
import time
import json
from flask import Flask, Response

app = Flask(__name__)
START_TIME = time.time()

@app.route('/')
def hello():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Endpoint Azure UK South</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body {
            width: 100%;
            height: 100%;
            overflow: hidden;
        }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #0a0a1a;
            color: #fff;
        }
        .wrapper {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .grid-bg {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                linear-gradient(rgba(102,126,234,0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(102,126,234,0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            pointer-events: none;
        }
        .glow-orb {
            position: absolute;
            width: 400px;
            height: 400px;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.3;
            pointer-events: none;
        }
        .orb1 { background: #667eea; top: -100px; left: -100px; }
        .orb2 { background: #764ba2; bottom: -100px; right: -100px; }
        .orb3 { background: #06b6d4; top: 50%; left: 50%; transform: translate(-50%, -50%); }
        .content {
            z-index: 10;
            text-align: center;
        }
        .hex-border {
            position: relative;
            padding: 60px 80px;
            background: rgba(10,10,26,0.9);
            border: 2px solid rgba(102,126,234,0.5);
            clip-path: polygon(10% 0%, 90% 0%, 100% 50%, 90% 100%, 10% 100%, 0% 50%);
        }
        .hex-border::before {
            content: '';
            position: absolute;
            top: -2px; left: -2px; right: -2px; bottom: -2px;
            background: linear-gradient(45deg, #667eea, #764ba2, #06b6d4, #667eea);
            clip-path: polygon(10% 0%, 90% 0%, 100% 50%, 90% 100%, 10% 100%, 0% 50%);
            z-index: -1;
        }
        h1 {
            font-size: 3em;
            font-weight: 300;
            letter-spacing: 8px;
            text-transform: uppercase;
            background: linear-gradient(90deg, #667eea, #764ba2, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            white-space: nowrap;
        }
        .status-line {
            margin-top: 20px;
            font-size: 0.9em;
            color: #10b981;
            letter-spacing: 3px;
        }
        .status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            margin-right: 8px;
        }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="grid-bg"></div>
        <div class="glow-orb orb1"></div>
        <div class="glow-orb orb2"></div>
        <div class="glow-orb orb3"></div>
        <div class="content">
            <div class="hex-border">
                <h1>Endpoint Azure UK South</h1>
                <div class="status-line">
                    <span class="status-dot"></span>ONLINE
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/health')
def health():
    data = {
        'status': 'healthy',
        'uptime_seconds': round(time.time() - START_TIME, 2),
        'region': 'UK South'
    }
    return Response(json.dumps(data), mimetype='application/json')

application = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
