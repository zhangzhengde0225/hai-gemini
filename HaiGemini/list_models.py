

import os
import requests

def list_models(proxy=None):
    api_key = os.environ.get('GOOGLE_API_KEY', None)
    assert api_key is not None, "The api_key must be specified, or set the GOOGLE_API_KEY environment variable."
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    if proxy:
        proxies = {"http": proxy, "https": proxy}
    else:
        proxies = None
    
    response = requests.get(url, proxies=proxies)
    print(f'response.text: {response.text}')
    return response.json()


if __name__ == '__main__':
    proxy = 'http://localhost:8118'
    models = list_models(proxy=proxy)

    for m in models["models"]:
        # print(m)
        print("name: ", m["name"])