import os
import threading
from auth import auth, S, URL

TOKEN = auth()
directory = 'up'
files = os.listdir(directory)

THREADS = 1
runs = int(len(files)/THREADS)


def upload(threadn:int):
    for x in range(0, runs):
        filename = files[x*THREADS+threadn-1]
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            print(f)

            PARAMS_FILE = {
                "action": "upload",
                "filename": filename,
                "format": "json",
                "token": TOKEN,
                "ignorewarnings": 1
            }

            FILE = {'file': (filename, open(f, 'rb'), 'multipart/form-data')}

            S.post(URL, files=FILE, data=PARAMS_FILE)

            PARAMS = {
                "bot": True,
                "action": "edit",
                "title": "File:" + filename,
                "token": auth(),
                "format": "json",
                "summary": "Adding categories and license",
                "text": "{{Fairuse}}\n\n[[Category:Credits]]\n[[Category:Crew]]\n[[Category:Cast]]"
            }
            R = S.post(URL, data=PARAMS)


for x in range(1, THREADS+1):
    threading.Thread(target=upload, args=(x,)).start()
