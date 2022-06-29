import requests
import json
import os
from auth import getAuth
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

groupId = os.getenv('groupId')
channelID = os.getenv('channelID')
code_collab = os.getenv('code_collab')
portal_posse = os.getenv('portal_posse')

ENDPOINT = 'https://graph.microsoft.com/v1.0'


def get_pretty_json_string(value_dict):
    return json.dumps(value_dict, indent=4, sort_keys=True, ensure_ascii=False)


def postChat(chat_ID, message):
    funcResult = getAuth()
    chat = f"/chats/{chat_ID}/messages"
    url = ENDPOINT+chat

    payload = json.dumps({
      "body": {
        "content": f"{message}"
      }
    })

    headers = {
                'Accept': 'application/json',
               'Authorization': 'Bearer '+funcResult['access_token'],
               'Content-Type': 'application/json'
                }

    res = requests.post(url, headers=headers, data=payload)
    print(res.text)


def getChat(chat_ID, top):
    funcResult = getAuth()
    url = ENDPOINT + f'/chats/{chat_ID}/messages?$top={top}'

    headers = {
                'Accept': 'application/json',
               'Authorization': 'Bearer '+funcResult['access_token'],
               'Content-Type': 'application/json'
                }

    result = requests.get(url, headers=headers).json()
    # result = json.loads(result.text)
    return result



# postChat(code_collab, html)

res = getChat(portal_posse, 3)
sxJSON = get_pretty_json_string(res)
print(sxJSON)
#
# for data in res['value']:
#     print(data['from']['user']['displayName'])
#     print(data['body']['content'])
#     print(data['lastModifiedDateTime'])

