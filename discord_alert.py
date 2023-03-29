#!/usr/bin/env python3

import requests

def raise_alert(reason):
    url = "YourWebhookURL" #webhook url

    data = {
        "content" : "Attention! A new alert has been raised!",
        "username" : "COMMITS ALERT"
    }

    data["embeds"] = [
        {
            "description" : "An alert has been raised for 3 times due to elevated {} levels.".format(reason),
            "title" : "Alert for {}".format(reason),
        }
    ]

    result = requests.post(url, json = data)

