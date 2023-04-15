#!/bin/bash
set -euo pipefail

curl \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $LINEAR_API_KEY" \
  --data '{ "query": "{ issues { nodes { id title } } }" }' \
  https://api.linear.app/graphql
