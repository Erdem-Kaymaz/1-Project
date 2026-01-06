import requests
import json
import asyncio
import config

HEADERS = {
    'X-Key' : f'Key {config.API_KEY}',
    'X-Secret' : f'Secret {config.SECRET_KEY}',
}

URL = 'https://api-key.fusionbrain.ai/'

async def generate(prompt):
    params = {
        'type': 'GENERATE',
        'numImages': 1,
        'width': 1024,
        'height': 1024,
        'generateParams': {'query': prompt}
    }

    response = requests.get(URL + 'key/api/v1/pipelines', headers=HEADERS)
    pipeline_id = response.json()[0]['id']

    files = {
        'pipeline_id': (None, pipeline_id),
        'params': (None, json.dumps(params), 'application/json')
    }

    response = requests.post(URL + 'key/api/v1/pipeline/run',headers=HEADERS, files=files)
    data = response.json()

    attempts = 0
    while attempts < 40:
        response = requests.get(URL + 'key/api/v1/pipeline/status/' + data['uuid'], headers=HEADERS)
        data = response.json()
        if data['status'] == 'DONE':
            return data['result']['files']
        attempts += 1
        await asyncio.sleep(3)