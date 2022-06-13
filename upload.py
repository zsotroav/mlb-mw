import dotenv
import os
import requests

if os.path.exists('.env'):
    dotenv.load_dotenv()

S = requests.Session()
URL = "https://miraculousladybug.fandom.com/api.php"
FILE_PATH = 'pikagoh.png'

# Step 1: Retrieve a login token
PARAMS_1 = {
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS_1)
DATA = R.json()

LOGIN_TOKEN = DATA["query"]["tokens"]["logintoken"]

# Step 2: Send a post request to login. Use of main account for login is not
# supported. Obtain credentials via Special:BotPasswords
# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
PARAMS_2 = {
    "action": "login",
    "lgname": os.getenv("mwname"),
    "lgpassword": os.getenv("mwpasswd"),
    "format": "json",
    "lgtoken": LOGIN_TOKEN
}

R = S.post(URL, data=PARAMS_2)
print(R.json())
# Step 3: Obtain a CSRF token
PARAMS_3 = {
    "action": "query",
    "meta":"tokens",
    "format":"json"
}

R = S.get(url=URL, params=PARAMS_3)
DATA = R.json()

CSRF_TOKEN = DATA["query"]["tokens"]["csrftoken"]

directory = '126'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        print(f)
        # Step 4: Post request to upload a file directly
        PARAMS_FILE = {
            "action": "upload",
            "filename": filename,
            "format": "json",
            "token": CSRF_TOKEN,
            "ignorewarnings": 1
        }

        FILE = {'file':(filename, open(f, 'rb'), 'multipart/form-data')}

        R = S.post(URL, files=FILE, data=PARAMS_FILE)
        print(R.json())
