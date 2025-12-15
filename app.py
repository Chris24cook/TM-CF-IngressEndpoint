import os
import time
import socket
import platform
import subprocess
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
START_TIME = time.time()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return socket.gethostbyname(socket.gethostname())

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "service": "Azure Network Probe Agent",
        "version": "1.0.0",
        "hostname": socket.gethostname(),
        "local_ip": get_local_ip(),
        "platform": platform.system(),
        "python_version": platform.python_version(),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "uptime_seconds": time.time() - START_TIME})

@app.route('/ping')
def ping():
    return jsonify({"message": "pong", "server_time": datetime.utcnow().isoformat() + "Z", "timestamp_ms": int(time.time() * 1000)})

@app.route('/debug/headers')
def debug_headers():
    headers = dict(request.headers)
    return jsonify({
        "client_ip": request.remote_addr,
        "x_forwarded_for": request.headers.get('X-Forwarded-For'),
        "x_forwarded_host": request.headers.get('X-Forwarded-Host'),
        "x_azure_clientip": request.headers.get('X-Azure-ClientIP'),
        "x_azure_socketip": request.headers.get('X-Azure-SocketIP'),
        "x_arr_ssl": request.headers.get('X-ARR-SSL'),
        "x_site_deployment_id": request.headers.get('X-Site-Deployment-Id'),
        "all_headers": headers
    })

@app.route('/debug/env')
def debug_env():
    safe_vars = ['WEBSITE_SITE_NAME', 'WEBSITE_INSTANCE_ID', 'WEBSITE_HOSTNAME', 'WEBSITE_RESOURCE_GROUP', 'WEBSITE_OWNER_NAME', 'REGION_NAME', 'WEBSITE_SKU', 'HOME', 'PATH']
    env_info = {var: os.environ.get(var) for var in safe_vars if os.environ.get(var)}
    return jsonify({"azure_environment": env_info, "is_azure": 'WEBSITE_SITE_NAME' in os.environ})

@app.route('/dns/<hostname>')
def dns_lookup(hostname):
    try:
        ip_addresses = socket.gethostbyname_ex(hostname)
        return jsonify({"hostname": hostname, "canonical_name": ip_addresses[0], "aliases": ip_addresses[1], "addresses": ip_addresses[2], "success": True})
    except socket.gaierror as e:
        return jsonify({"hostname": hostname, "error": str(e), "success": False}), 404

@app.route('/tcp-test/<host>/<int:port>')
def tcp_test(host, port):
    timeout = float(request.args.get('timeout', 3))
    start = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        latency = (time.time() - start) * 1000
        sock.close()
        return jsonify({"host": host, "port": port, "open": result == 0, "latency_ms": round(latency, 2), "success": True})
    except Exception as e:
        return jsonify({"host": host, "port": port, "error": str(e), "success": False})

@app.route('/simulate-load/<float:duration>')
def simulate_load(duration):
    if duration > 30:
        return jsonify({"error": "Max duration is 30 seconds"}), 400
    time.sleep(duration)
    return jsonify({"slept_for_seconds": duration, "message": "Load simulation complete"})

@app.route('/debug/memory')
def memory_info():
    try:
        import resource
        usage = resource.getrusage(resource.RUSAGE_SELF)
        return jsonify({"max_rss_mb": usage.ru_maxrss / 1024, "user_time_seconds": usage.ru_utime, "system_time_seconds": usage.ru_stime})
    except:
        return jsonify({"error": "Memory info not available on this platform"})

@app.route('/debug/interfaces')
def network_interfaces():
    try:
        result = subprocess.run(['ip', 'addr'], capture_output=True, text=True, timeout=5)
        return jsonify({"interfaces": result.stdout, "success": True})
    except Exception as e:
        return jsonify({"error": str(e), "success": False})

@app.route('/traceroute/<target>')
def traceroute(target):
    try:
        result = subprocess.run(['traceroute', '-m', '15', '-w', '1', target], capture_output=True, text=True, timeout=30)
        lines = result.stdout.strip().split('
')
        return jsonify({"target": target, "hops": lines, "success": True})
    except FileNotFoundError:
        return jsonify({"error": "traceroute not installed", "success": False})
    except Exception as e:
        return jsonify({"target": target, "error": str(e), "success": False})

@app.route('/echo', methods=['GET', 'POST', 'PUT', 'DELETE'])
def echo():
    return jsonify({"method": request.method, "path": request.path, "query_params": dict(request.args), "headers": dict(request.headers), "body": request.get_data(as_text=True), "remote_addr": request.remote_addr, "timestamp": datetime.utcnow().isoformat() + "Z"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
