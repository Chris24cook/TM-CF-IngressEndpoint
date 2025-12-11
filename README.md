# Azure Network Probe

A Python Flask utility for network diagnostics in Azure App Service Linux containers.

## Features

- **Health Check**: Azure-compatible health endpoint
- **Latency Testing**: Simple ping/pong endpoint
- **Header Inspection**: View Azure proxy headers (X-Forwarded-For, X-Azure-ClientIP, etc.)
- **DNS Lookup**: Resolve any hostname
- **TCP Port Testing**: Test connectivity to any host:port
- **Traceroute**: Trace network routes (if available)
- **Load Simulation**: Test timeout configurations
- **Environment Info**: View safe Azure environment variables

## Quick Deploy

1. Download both files (network_probe.py and requirements.txt)
2. Run the Azure CLI commands:

```bash
az login
az group create --name NetProbeRG --location eastus
az appservice plan create --name NetProbePlan --resource-group NetProbeRG --sku B1 --is-linux
az webapp up --sku F1 --name YOUR-UNIQUE-NAME --resource-group NetProbeRG --runtime "PYTHON:3.11"
```

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Status & system info |
| `/health` | Health check for Azure |
| `/ping` | Simple latency test |
| `/debug/headers` | View all request headers |
| `/debug/env` | Azure environment variables |
| `/debug/interfaces` | Network interfaces |
| `/dns/<hostname>` | DNS lookup |
| `/tcp-test/<host>/<port>` | TCP connectivity test |
| `/traceroute/<target>` | Trace network route |
| `/simulate-load/<seconds>` | Load simulation (max 30s) |
| `/echo` | Echo request details |

## License

MIT
