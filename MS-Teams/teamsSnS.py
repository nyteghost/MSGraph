import json
import logging
import os

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

HOOK_URL = os.environ['HookUrl']

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))

    alarm_name = message['AlarmName']
    old_state = message['OldStateValue']
    new_state = message['NewStateValue']
    reason = message['NewStateReason']

    data = {
        "colour": "64a837",
        "title": "**%s** is resolved" % alarm_name,
        "text": "**%s** has changed from %s to %s - %s" % (alarm_name, old_state, new_state, reason)
    }

    if new_state.lower() == 'alarm':
        data = {
            "colour": "d63333",
            "title": "Red Alert - There is an issue %s" % alarm_name,
            "text": "**%s** has changed from %s to %s - %s" % (alarm_name, old_state, new_state, reason)
        }

    message = {
        "@context": "https://schema.org/extensions",
        "@type": "MessageCard",
        "themeColor": data["colour"],
        "title": data["title"],
        "text": data["text"]
    }

    req = Request(HOOK_URL, json.dumps(message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted")
        return {"status": "200 OK"}
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)