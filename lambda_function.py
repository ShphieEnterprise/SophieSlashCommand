import json
import os

from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey


def lambda_handler(event, context):
    print(event)
    PUBLIC_KEY = os.environ['PUBLIC_KEY']

    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    signature = event['headers']["x-signature-ed25519"]
    timestamp = event['headers']["x-signature-timestamp"]
    body = event['body']

    print(body)

    try:
        verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
        body = json.loads(event['body'])
        print('body', body)
        if body["type"] == 1:
            return {
                'statusCode': 200,
                'body': json.dumps({'type': 1})
            }
    except (BadSignatureError) as e:
        return {
            'statusCode': 401,
            'body': json.dumps("Bad Signature")
        }

    return {
        'statusCode': 404
    }
