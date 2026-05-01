#!/bin/bash
cd "$(dirname "$0")"

# Start API in background
cd api
source ../venv/bin/activate 2>/dev/null || true
uvicorn main:app --host 0.0.0.0 --port 9000 &
API_PID=$!

echo "Mobile-Morpher API started on port 9000"
echo "PID: $API_PID"

# Keep running
wait $API_PID
