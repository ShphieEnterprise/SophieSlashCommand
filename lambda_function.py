import json
import os

import requests
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey


def lambda_handler(event, context):
    PUBLIC_KEY = os.environ['PUBLIC_KEY']

    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    signature = event['headers']["x-signature-ed25519"]
    timestamp = event['headers']["x-signature-timestamp"]
    body = event['body']

    print('event:', event)
    print('body', body)

    try:
        verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
        body = json.loads(event['body'])

        if body["type"] == 1:
            return {
                'statusCode': 200,
                'body': json.dumps({'type': 1})
            }

        if body["type"] == 2:
            url = "https://discord.com/api/v10/interactions/{}/{}/callback".format(body['id'], body['token'])

            data = {
                "type": 4,
                "data": {
                    "content": "にゃーん"
                }
            }

            r = requests.post(url, json=data)
            print('r:', r.json())
            return
    except (BadSignatureError) as e:
        return {
            'statusCode': 401,
            'body': json.dumps("Bad Signature")
            }

    return {
        'statusCode': 404
    }
