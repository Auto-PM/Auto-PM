#!/bin/bash

. .ve/bin/activate

uvicorn static-files:app --reload &
upid=$!

# kill uvicorn on exit
trap "kill $upid" EXIT

sleep 1
# Run the tests	
curl -s http://localhost:8000/.well-known/ai-plugin.json

