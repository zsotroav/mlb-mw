import os
import dotenv
import requests
import datetime


if os.path.exists('.env'):
    dotenv.load_dotenv()

def send(title: str, message: str, color: int):
    PAR = {
    "content": "",
    "embeds": [
        {
        "title": title,
        "description": message,
        "color": color,
        "author": {
            "name": "Miraculous MediaWiki API"
        }
        }
    ],
    "attachments": []
    }
    
    R=requests.post(url=os.getenv('log_webhook'), json=PAR)
    print(R.text)
