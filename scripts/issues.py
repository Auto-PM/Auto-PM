import os
import requests

query = 'query { issues { nodes { id title } } }'

LINEAR_API_KEY=os.environ.get('LINEAR_API_KEY')
def run_linear_query(query):
    response = requests.post(
        'https://api.linear.app/graphql',
        json={'query': query},
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {LINEAR_API_KEY}',
            }
        )
    return response.json()

x = run_linear_query(query)
print(x)
