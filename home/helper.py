import json
import os

import django
import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()


def sms_send(mobile, text):
    payload = json.dumps(
        {
            "messages":
                [
                    {
                        "recipient": mobile,
                        "message-id": "abc000000001",

                        "sms": {

                            "originator": "3700",
                            "content": {
                                "text": text
                            }
                        }
                    }
                ]
        }
    )
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url=settings.SMS_URL, data=payload, headers=headers,
                                auth=HTTPBasicAuth(settings.SMS_LOGIN, settings.SMS_PASSWORD))

    return response
