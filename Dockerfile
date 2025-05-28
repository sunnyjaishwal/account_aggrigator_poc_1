# Use an official Ubuntu base image
FROM ubuntu:20.04

# Set timezone environment variables to prevent interactive prompt
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
    echo "Asia/Kolkata" > /etc/timezone && \
    apt-get update && apt-get install -y tzdata

# Install required packages including Firefox and dev dependencies
RUN apt-get update && apt-get install -y \
    x11vnc \
    xvfb \
    wget \
    git \
    gnupg \
    firefox \
    python3 \
    python3-pip \
    mitmproxy \
    ca-certificates \
    && apt-get clean

# Clone and setup noVNC + websockify manually
RUN git clone https://github.com/novnc/noVNC.git /opt/novnc && \
    git clone https://github.com/novnc/websockify /opt/novnc/utils/websockify && \
    ln -s /opt/novnc/utils/novnc_proxy /usr/local/bin/novnc_proxy

# Set up Firefox policies to disable prompts and allow proxy
COPY scripts/policies.json /usr/lib/firefox/distribution/policies.json

# Install FastAPI, Uvicorn, and mitmproxy Python bindings
RUN pip3 install fastapi uvicorn mitmproxy

# Install project-specific Python dependencies
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app/
WORKDIR /app/

# Make entrypoint scripts executable
RUN chmod +x /app/scripts/entrypoint.sh
RUN chmod +x /app/scripts/browser_session.sh

# Expose required ports
EXPOSE 5900 6080 8000 8080

# Set entrypoint
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
