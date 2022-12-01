import requests
import json
import os
import sys


BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
WEBLATE_URL = "http://azuresdkweblate.eastus.cloudapp.azure.com/api/%s"


def read_translated_percent(project, component, language):
    url = WEBLATE_URL % "translations/%s/%s/%s/" %(project, component, language)
        
    headers = {
        'Authorization': BEARER_TOKEN, 
        'Content-Type': 'application/json'
    }
    
    response = requests.request("GET", url, headers=headers)

    result = json.loads(response.text)
    return result["translated_percent"]


def push_repository_from_weblate(project, component, language):
    url =  WEBLATE_URL % "translations/%s/%s/%s/repository/" %(project, component, language)
    
    headers = {
        'Authorization': BEARER_TOKEN, 
        'Content-Type': 'application/json'
    }
    
    response = requests.request("GET", url, headers=headers)

    result = json.loads(response.text)

    if result["needs_commit"]:
        print("commit")

    payload = json.dumps({ "operation": "push" })
    headers = {
        'Authorization': BEARER_TOKEN, 
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


def main(project, component, language):
    if  read_translated_percent(project, component, language) >= 50:
        push_repository_from_weblate(project, component, language)

        
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
