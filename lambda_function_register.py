import os

import requests


def lambda_handler(event, context):
    url = f"https://discord.com/api/v8/applications/{os.environ['APPLICATION_ID']}/commands"

    # The json structure should be a list of command dictionaries
    json = [
        {
            "name": "neko",
            "description": "Mazu ha kokokara",
            "type": 1  # Type 1 indicates a CHAT_INPUT (slash command)
        },
        {
            "name": "inu",
            "description": "Tsugi ha wanchan",
            "type": 1  # Type 1 indicates a CHAT_INPUT (slash command)
        }
    ]

    headers = {
        "Authorization": f"Bot {os.environ['TOKEN']}"
    }

    # Loop through each command in the json list and post it
    for command in json:
        r = requests.post(url, headers=headers, json=command)
        print(r.json())

