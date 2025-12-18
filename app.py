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
    <title>CC Endpoint </title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #0a0a1a;
            color: #fff;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            position: relative;
        }
        .grid-bg {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: 
                linear-gradient(rgba(102,126,234,0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(102,126,234,0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: gridMove 20s linear infinite;
        }
        @keyframes gridMove {
            0% { transform: perspective(500px) rotateX(60deg) translateY(0); }
            100% { transform: perspective(500px) rotateX(60deg) translateY(50px); }
        }
        .glow-orb {
            position: absolute;
            width: 400px;
            height: 400px;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.3;
            animation: pulse 4s ease-in-out infinite;
        }
        .orb1 { background: #667eea; top: -100px; left: -100px; }
        .orb2 { background: #764ba2; bottom: -100px; right: -100px; animation-delay: 2s; }
        .orb3 { background: #06b6d4; top: 50%; left: 50%; transform: translate(-50%, -50%); }
        @keyframes pulse {
            0%, 100% { opacity: 0.2; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(1.1); }
        }
        .particles {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            overflow: hidden;
        }
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: #667eea;
            border-radius: 50%;
            box-shadow: 0 0 10px #667eea;
            animation: float 15s infinite linear;
        }
        @keyframes float {
            0% { transform: translateY(100vh) translateX(0); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-100vh) translateX(100px); opacity: 0; }
        }
        .content {
            position: relative;
            z-index: 10;
            text-align: center;
        }
        .hex-border {
            position: relative;
            padding: 60px 80px;
            background: rgba(10,10,26,0.8);
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
            animation: borderGlow 3s linear infinite;
        }
        @keyframes borderGlow {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }
        h1 {
            font-size: 3em;
            font-weight: 300;
            letter-spacing: 8px;
            text-transform: uppercase;
            background: linear-gradient(90deg, #667eea, #764ba2, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: none;
            animation: textGlow 2s ease-in-out infinite alternate;
        }
        @keyframes textGlow {
            from { filter: drop-shadow(0 0 20px rgba(102,126,234,0.5)); }
            to { filter: drop-shadow(0 0 40px rgba(102,126,234,0.8)); }
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
            animation: blink 1s infinite;
        }
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        .scan-line {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
            animation: scan 3s linear infinite;
        }
        @keyframes scan {
            0% { top: 0; opacity: 1; }
            100% { top: 100%; opacity: 0; }
        }
    </style>
</head>
<body>
    <div class="grid-bg"></div>
    <div class="glow-orb orb1"></div>
    <div class="glow-orb orb2"></div>
    <div class="glow-orb orb3"></div>
    <div class="particles">
        <div class="particle" style="left:10%;animation-delay:0s"></div>
        <div class="particle" style="left:20%;animation-delay:2s"></div>
        <div class="particle" style="left:30%;animation-delay:4s"></div>
        <div class="particle" style="left:50%;animation-delay:1s"></div>
        <div class="particle" style="left:70%;animation-delay:3s"></div>
        <div class="particle" style="left:80%;animation-delay:5s"></div>
        <div class="particle" style="left:90%;animation-delay:2.5s"></div>
    </div>
    <div class="scan-line"></div>
    <div class="content">
        <div class="hex-border">
            <h1>CC Endpoint </h1>
            <div class="status-line">
                <span class="status-dot"></span>ONLINE
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
        'region': ''
    }
    return Response(json.dumps(data), mimetype='application/json')

application = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
