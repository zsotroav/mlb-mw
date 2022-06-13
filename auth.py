import os
import dotenv
import requests

URL = "https://miraculousladybug.fandom.com/api.php"
S = requests.Session()

def auth():
    if os.path.exists('.env'):
        dotenv.load_dotenv()

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
