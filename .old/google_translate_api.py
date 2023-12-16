
from google.cloud import translate_v2

import requests

response = requests.post(
    url="https://translation.googleapis.com/language/translate/v2",
    json={
        "q": ["Hello world", "My name is Jeff"],
        "target": "de"
        }
    )


print(response.content) 