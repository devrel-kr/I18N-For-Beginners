from email import message
import requests, uuid, json

# Add your subscription key and endpoint
subscription_key = ""
endpoint = "https://api.cognitive.microsofttranslator.com"

# Add your location, also known as region. The default is global.
# This is required if using a Cognitive Services resource.
location = "koreacentral"

path = '/translate'
constructed_url = endpoint + path

with open('halo.txt', 'rt', encoding='UTF-8') as lyric:
    data = lyric.read()

params = {
    'api-version': '3.0',
    'from': 'en',
    'to': ['ko'],
    'text' : data
}


headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}



# You can pass more than one object in body.
body = [{
    'text': data
}]

request = requests.post(constructed_url, params=params, headers=headers, json=body )
f = open('output_A.txt', 'w', encoding='UTF-8')

if request.ok:
    # print(type(request.text), request.text)
    response = request.json()[0]['translations'][0]['text']

    # print(response)
    f.write(response)
    # print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

