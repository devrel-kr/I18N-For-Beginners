import requests, uuid
import pickle
import os

class Translate:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            cls._init = True
            self.cache = {}
            if os.path.exists('data/translate_data.pickle'):
                with open('data/translate_data.pickle', 'rb') as f:
                    self.cache = pickle.load(f)

    def set_api_key(self, api_key):
        # Add your subscription key and endpoint
        subscription_key = api_key
        endpoint = "https://api.cognitive.microsofttranslator.com"
        location = "koreacentral"

        path = '/translate'
        self.constructed_url = endpoint + path

        self.headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        
    def save_translate_cache(self):
        with open("data/translate_data.pickle", "wb") as f:
            pickle.dump(self.cache, f)

    def translate(self, text, lang_from, lang_to):
        if text in self.cache:
            return self.cache[text]
        body = [{
            'text': text
        }]

        params = {
            'api-version': '3.0',
            'from': lang_from,
            'to': [lang_to],
            'text' : text
        }

        request = requests.post(self.constructed_url, params=params, headers=self.headers, json=body)

        if request.ok:
            response = request.json()[0]['translations'][0]['text']
            self.cache[text] = response
            return response
        return None