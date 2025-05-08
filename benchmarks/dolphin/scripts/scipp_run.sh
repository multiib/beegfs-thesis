#!/bin/bash

# Configuration
REMOTE_USER="benjabor"
REMOTE_HOST="mpg-2014-18"
REMOTE_BIN="/opt/DIS/bin"
LOCAL_BIN="/opt/DIS/bin"

# Step 1: Start scipp server on remote
echo "[INFO] Starting scipp server on remote..."
ssh "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_BIN && nohup ./scipp -rn 4 -server > server.log 2>&1 &"
echo "[INFO] Remote server started."

# Step 2: Start scipp client locally
echo "[INFO] Starting scipp client locally..."
cd "$LOCAL_BIN"
sudo ./scipp -rn 8 -client
