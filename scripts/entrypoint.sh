#!/bin/bash

# Clean any old X sessions
pkill Xvfb
pkill firefox
pkill x11vnc
pkill fluxbox

# Start virtual display
Xvfb :1 -screen 0 1280x720x24 &
export DISPLAY=:1
sleep 2

# Start a lightweight window manager
fluxbox &
sleep 1

# Start x11vnc server on display :1
x11vnc -display :1 -nopw -forever -bg

# Start noVNC server on port 6080 via websockify
echo "Starting noVNC server..."
/opt/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 6080 --web /opt/novnc &

# Setup mitmproxy CA certificate
echo "Generating mitmproxy CA certificate..."
mkdir -p /root/.mitmproxy

# Trigger cert generation
timeout 5 mitmdump --set block_global=false || true

# Install mitmproxy cert to system
if [ -f /root/.mitmproxy/mitmproxy-ca-cert.pem ]; then
    cp /root/.mitmproxy/mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/mitmproxy-ca-cert.crt
    update-ca-certificates
    echo "MITMProxy CA installed."
else
    echo "MITMProxy CA not found. Something went wrong!"
fi

# Start mitmproxy
echo "Starting mitmproxy..."
mitmdump -s /app/scripts/mitmproxy_script.py --listen-port 8080 --set block_global=false &

# Start FastAPI server
echo "Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8000
