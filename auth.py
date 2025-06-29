import os
import dotenv
import requests
from datetime import datetime

S = requests.Session()

if os.path.exists('.env'):
    dotenv.load_dotenv()
os.environ["mw-csrf-exp"] = "0"


URL = os.getenv("URL")

def auth():
    if int(os.environ["mw-csrf-exp"]) < int(datetime.timestamp(datetime.now())):
        csrf = get_CSRF()
        os.environ["mw-csrf"] = csrf
        os.environ["mw-csrf-exp"] = str(int(datetime.timestamp(datetime.now())+2000))
        return os.environ["mw-csrf"]
    else:
        return os.environ["mw-csrf"]


def get_CSRF():
    # Step 1: Retrieve a login token
    PARAMS_1 = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_1)
    DATA = R.json()

    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

    # Step 2: Send a post request to login. Use of main account for login
    # is not supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname &
    # lgpassword
    PARAMS_2 = {
        "action": "login",
        "lgname": os.getenv("mwname"),
        "lgpassword": os.getenv("mwpasswd"),
        "format": "json",
        "lgtoken": LOGIN_TOKEN
    }

    R = S.post(URL, data=PARAMS_2)

    # Step 3: While logged in, retrieve a CSRF token
    PARAMS_3 = {
        "action": "query",
        "meta": "tokens",
        "type": "csrf",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_3)
    DATA = R.json()

    return DATA["query"]["tokens"]["csrftoken"]
