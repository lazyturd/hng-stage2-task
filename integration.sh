#!/bin/bash
# integration.sh

echo "Waiting for stack to be ready..."
sleep 10

echo "Submitting job..."
RESPONSE=$(curl -s -X POST http://localhost:3000/submit)
JOB_ID=$(echo $RESPONSE | jq -r .job_id)

if [ -z "$JOB_ID" ] || [ "$JOB_ID" == "null" ]; then
  echo "Failed to create job"
  exit 1
fi

echo "Job $JOB_ID created. Polling..."

# Timeout loop requirement
TIMEOUT=60
START_TIME=$(date +%s)

while true; do
  CURRENT_TIME=$(date +%s)
  ELAPSED=$((CURRENT_TIME - START_TIME))

  if [ $ELAPSED -gt $TIMEOUT ]; then
    echo "Integration timeout exceeded!"
    exit 1
  fi

  STATUS=$(curl -s http://localhost:3000/status/$JOB_ID | jq -r .status)
  if [ "$STATUS" == "completed" ]; then
    echo "Job successfully completed!"
    exit 0
  fi
  
  sleep 2
done