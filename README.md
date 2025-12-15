# Hello World from CC

A simple Python Flask web app for Azure App Service.

## What It Does

Displays "Hello World from CC" when you visit the web page.

## Files

- `network_probe.py` - The Flask application
- `requirements.txt` - Dependencies (flask==3.0.0)

## Deploy to Azure

### Step 1: Create Web App in Azure Portal

1. Go to [portal.azure.com](https://portal.azure.com)
2. Click **Create a resource** → **Web App**
3. Fill in:
   - **Subscription**: Your subscription
   - **Resource Group**: Create new or use existing
   - **Name**: Choose a unique name (e.g., `cc-hello-world`)
   - **Publish**: **Code**
   - **Runtime stack**: **Python 3.11**
   - **Operating System**: **Linux**
   - **Region**: Choose closest to you

### Step 2: Connect to GitHub

4. Click **Deployment** tab
5. Set **Continuous deployment**: **Enable**
6. Sign in to GitHub
7. Select:
   - **Organization**: Chris24cook
   - **Repository**: TM-CF-IngressEndpoint
   - **Branch**: main

### Step 3: Create & Wait

8. Click **Review + create** → **Create**
9. Wait 2-3 minutes for deployment

### Step 4: Access Your App

Your app will be available at:
```
https://<your-app-name>.azurewebsites.net
```

Azure automatically handles:
- **Port 443** (HTTPS) - Public access with SSL
- **Port 80** (HTTP) - Redirects to HTTPS

## Troubleshooting

If you get a 403 error:
1. Go to App Service → **Authentication** → Set to **Disabled**
2. Go to App Service → **Networking** → **Access Restrictions** → Allow all traffic
