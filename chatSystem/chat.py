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
from pretty_html_table import build_table

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
    df = df.style.set_table_styles([dict(selector='th', props=[('text-align', 'center'), ('background-color', '#40466e'), ('color', 'white')])])
    df.set_properties(**{'text-align': 'center'}).hide(axis='index')
    pd.set_option('colheader_justify', 'center')
    html = df.to_html()
    return html


class teamsChat:
    print('teamsChat')

    def __init__(self, chat_ID):
        if chat_ID == "portal_posse":
            self.chat_ID = os.getenv('portal_posse')
        elif chat_ID == "mainDataChat":
            self.chat_ID = os.getenv('mainDataChat')
        elif chat_ID == "code_collab":
            self.chat_ID = os.getenv('code_collab')
        elif chat_ID == "ccmChat":
            self.chat_ID = os.getenv('ccmChat')
        self.funcResult = getAuth()
        self.headers = {
                    'Accept': 'application/json',
                   'Authorization': 'Bearer '+self.funcResult['access_token'],
                   'Content-Type': 'application/json'
                    }

    def send(self, message):
        chatRoom = f"/chats/{self.chat_ID}/messages"
        url = BETA+chatRoom
        payload = json.dumps({
              "body": {
                "contentType": "html",
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

    def sendTable(self, title, font_size, dataframe):
        font = f'<font size="{font_size}"><center>{title}</center></font>'
        table = build_table(dataframe, 'green_dark', font_size='14px', width='auth', odd_bg_color="black")
        chatRoom = f"/chats/{self.chat_ID}/messages"
        url = BETA+chatRoom
        payload = json.dumps({
            "body": {
                "contentType": "html",
                "content": font+table
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
        for data in result['value']:
            print(data['topic'])
            print(data['id'])
            print()


if __name__ == '__main__':
    failed_reason = ["This is a test", "This is a test2", "This is a test3"]
    print('Running as Main')
    teamchat = teamsChat('portal_posse')
    df = pd.DataFrame(np.random.randn(10, 5), columns=list('ABCDE'))
    teamchat.sendTable(5, "MP Completion", df)

