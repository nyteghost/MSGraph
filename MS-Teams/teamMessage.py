import requests
import json


url = "https://<company>.webhook.office.com/webhookb2/" \
        "089d231b-35ef-417e-9400-9aba2e4016e2@60924edf-0a5e-4596-99cb-ebcf9d2ddb51/" \
        "IncomingWebhook/9086e2528b6a4ef7862f0f7e7eab008d/" \
        "542cb2d2-c180-43ed-bd24-3e2cf905ac74"


payload = {
    "text": "@email hello"
            "@email hello"
            "@email hello"
}
headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
