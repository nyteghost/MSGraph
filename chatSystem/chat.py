import time
import requests
import json
import os
from auth import getAuth
from dotenv import load_dotenv
import pandas as pd
import imgkit
import numpy as np
from PIL import Image
import base64

load_dotenv()

groupId = os.getenv('groupId')
channelID = os.getenv('channelID')
code_collab = os.getenv('code_collab')
portal_posse = os.getenv('portal_posse')
mainDataChat = os.getenv('mainDataChat')

ENDPOINT = 'https://graph.microsoft.com/v1.0'
BETA = 'https://graph.microsoft.com/beta'


def get_pretty_json_string(value_dict):
    return json.dumps(value_dict, indent=4, sort_keys=True, ensure_ascii=False)


def df2img(csv_file, name_file):
    df = csv_file
    df = df.style.set_table_styles([dict(selector='th', props=[('text-align', 'center'),('background-color', '#40466e'), ('color', 'white')])])
    df.set_properties(**{'text-align': 'center'}).hide(axis='index')
    pd.set_option('colheader_justify', 'center')
    html = df.to_html()
    options = {'quality': 80}
    imgkit.from_string(html, name_file + ".png", options=options)


def df2html(dataframe):
    df = dataframe
    df = df.style.set_table_styles([dict(selector='th', props=[('text-align', 'center'),('background-color', '#40466e'), ('color', 'white')])])
    df.set_properties(**{'text-align': 'center'}).hide(axis='index')
    pd.set_option('colheader_justify', 'center')
    html = df.to_html()
    return html


class teamsChat:
    def __init__(self, chat_ID):
        self.chat_ID = chat_ID
        self.funcResult = getAuth()
        self.headers = {
                    'Accept': 'application/json',
                   'Authorization': 'Bearer '+self.funcResult['access_token'],
                   'Content-Type': 'application/json'
                    }

    def send(self, message):
        chatRoom = f"/chats/{self.chat_ID}/messages"
        url = BETA+chatRoom

        if message == 2:
            payload = json.dumps(message)
            res = requests.post(url, headers=self.headers, data=payload)

        elif message != "":
            payload = json.dumps({
              "body": {
                "content": f"{message}"
              }
            })
            res = requests.post(url, headers=self.headers, data=payload)
            print(res.text)

    def sendImage(self, dataframe):
        df = dataframe
        df2img(df, 'dataframe')
        img = "dataframe.png"
        with open(img, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read())
        xyz = b64_string.decode('utf-8')

        chatRoom = f"/chats/{self.chat_ID}/messages"
        url = BETA+chatRoom
        payload = json.dumps({
            "body": {
                "contentType": "html",
                "content": "<div><div>\n<div><span><img height=\"297\" src=\"../hostedContents/1/$value\" width=\"297\" style=\"vertical-align:bottom; width:297px; height:297px\"></span>\n\n</div>\n\n\n</div>\n</div>"
            },
            "hostedContents": [
                {
                    "@microsoft.graph.temporaryId": "1",
                    "contentBytes": f"{xyz}",
                    "contentType": "image/png"
                }
            ]
        })
        res = requests.post(url, headers=self.headers, data=payload)
        print(res.text)

    def sendTable(self, dataframe):
        html = df2html(dataframe)
        chatRoom = f"/chats/{self.chat_ID}/messages"
        url = BETA+chatRoom
        payload = json.dumps({
            "body": {
                "contentType": "html",
                "content": html
            }
        })
        res = requests.post(url, headers=self.headers, data=payload)
        print(res.text)

    def receive(self, top):
        funcResult = getAuth()
        url = ENDPOINT + f'/chats/{self.chat_ID}/messages?$top={top}'
        result = requests.get(url, headers=self.headers).json()
        # result = json.loads(result.text)
        sxJSON = json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False)
        print(sxJSON)

    def findChats(self):
        url = ENDPOINT + '/me/chats'
        result = requests.get(url, headers=self.headers).json()
        # result = json.loads(result.text)
        sxJSON = json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False)
        print(sxJSON)

