import threading
from auth import auth, S, URL

reason = "Unused misnamed file"

file1 = open('deletelist.txt', 'r')
Lines = file1.readlines()
TOKEN = auth()

THREADS = 4
runs = int(len(Lines)/THREADS)


def delt(threadn:int):
    for x in range(0, runs):
        image = Lines[x*4+threadn-1].replace("\n", "")
        PARAMS = {
        "action": "query",
        "format": "json",
        "list": "imageusage",
        "iutitle": image,
        "iulimit": "3"
        }

        R = S.post(URL, data=PARAMS)
        if len(R.json()["query"]["imageusage"]) == 0:
            PARAMS = {
                "action": "delete",
                "title": image,
                "format": "json",
                "token": TOKEN,
                "reason": f'{reason} - T{threadn}',
            }

            R = S.post(URL, data=PARAMS)
        else:
            print(f"[WARN] USED IMAGE: {image}")


for x in range(1, THREADS+1):
    threading.Thread(target=delt, args=(x,)).start()
