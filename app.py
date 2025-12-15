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
    <title>CC Endpoint UK South</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        h1 {
            font-size: 3em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>
    <h1>CC Endpoint UK South</h1>
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
