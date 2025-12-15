import os
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Hello World</title>
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
    <h1>Hello World from CC</h1>
</body>
</html>
'''

def run_on_port(port):
    app.run(host='0.0.0.0', port=port, threaded=True)

if __name__ == '__main__':
    port_8000 = int(os.environ.get('PORT', 8000))
    port_555 = 555
    
    print(f"Starting server on ports {port_8000} and {port_555}")
    
    t1 = threading.Thread(target=run_on_port, args=(port_8000,))
    t2 = threading.Thread(target=run_on_port, args=(port_555,))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
