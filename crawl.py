import json
import threading
import logging
import logger
from auth import auth, S, URL

auth()

THREADS = 7


def t(threadn: int):
    f = open(f"tres/{threadn}.txt", "a")
    for x in range(0, l):
        work = raw[x*THREADS+threadn-1]["title"]

        page_res = S.post(URL, {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": work,
            "formatversion": "2",
            "rvprop": "content",
            "rvslots": "main"
        })

        page = page_res.json()["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]

        if "<font" in page:
            f.write(work + "\n")
            logging.warning(f"@ T{threadn} - {work} --- FOUND <font> HTML TAG")
    f.close()


PARA = {
    "action": "query",
    "format": "json",
    "list": "allpages",
    "apnamespace": "10",
    "aplimit": "3000"
}

R = S.post(URL, data=PARA)
json = R.json()
# print(json)
raw = json["query"]["allpages"]
l = int(len(raw)/THREADS)

for x in range(1, THREADS+1):
    threading.Thread(target=t, args=(x,)).start()



