import threading
from auth import auth, S, URL

reason = "Unused file (Automatic)"

file1 = open('deletelist.txt', 'r')
Lines = file1.readlines()
TOKEN = auth()

runs = (int)(len(Lines)/4)


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
            print(R.json())
            print(PARAMS)


threading.Thread(target=delt, args=(1, )).start()
threading.Thread(target=delt, args=(2, )).start()
threading.Thread(target=delt, args=(3, )).start()
threading.Thread(target=delt, args=(4, )).start()

if (len(Lines)%4 != 0):
    for x in range(runs*4, len(Lines)):
        image = Lines[x].replace("\n", "")
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
                "reason": f'{reason} - T0',
            }

            R = S.post(URL, data=PARAMS)
            print(R.json())
            print(PARAMS)
