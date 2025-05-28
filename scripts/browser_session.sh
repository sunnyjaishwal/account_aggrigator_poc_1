#!/bin/bash

# Ensure URL is passed
URL=$1

# Start a virtual display
Xvfb :1 -screen 0 1280x720x24 &

# Wait a moment
sleep 2

# Start VNC server
x11vnc -display :1 -nopw -forever -bg

# Set Firefox to use MITMProxy at localhost:8080
# Use a temporary Firefox profile with proxy settings
PROFILE_DIR=$(mktemp -d)

# Configure proxy settings using user.js
cat <<EOF > $PROFILE_DIR/user.js
user_pref("network.proxy.type", 1);
user_pref("network.proxy.http", "localhost");
user_pref("network.proxy.http_port", 8080);
user_pref("network.proxy.ssl", "localhost");
user_pref("network.proxy.ssl_port", 8080);
user_pref("network.proxy.no_proxies_on", "");
user_pref("security.enterprise_roots.enabled", true);  // trust local MITM certs
EOF

# Launch Firefox with the profile
#DISPLAY=:1 firefox --no-remote --profile "$PROFILE_DIR" --width=1280 --height=720 "$URL"
DISPLAY=:1 firefox --kiosk "$URL" --no-remote --profile "$PROFILE_DIR" &

