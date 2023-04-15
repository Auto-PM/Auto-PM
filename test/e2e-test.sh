#!/bin/bash
# A basic "end to end" test.

. venv/bin/activate

make run &
upid=$!

# kill uvicorn on exit
trap "kill $upid" EXIT

sleep 5
# Run the tests	
curl -s http://localhost:8000/.well-known/ai-plugin.json

