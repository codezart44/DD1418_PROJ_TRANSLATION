import requests


url = "https://libretranslate.com/translate"

data = {
    "q": "Hello, world!",  # Text to be translated
    "source": "en",         # Source language (English)
    "target": "es",         # Target language (Spanish)
    "format": "text"        # Format of the text
}

response = requests.post(url, data=data)
if response.status_code == 200:
    translation = response.json()['translatedText']
    print(translation)
else:
    print("Error:", response.status_code)
    print(response.content)