from auth import auth, S, URL

TOKEN = auth()

SEARCH = "XY"
LIMIT = 47

RED_PARA = {
    "action": "query",
    "format": "json",
    "prop": "",
    "list": "querypage",
    "redirects": 1,
    "qppage": "Wantedpages",
    "qplimit": LIMIT
}

RED = S.post(URL, RED_PARA).json()

for i in range(0, len(RED["query"]["querypage"]["results"])):
    page = RED["query"]["querypage"]["results"][i]
    title = page["title"]
    if not title.startswith(SEARCH):
        continue

    LOG_PARA = {
        "action": "query",
        "format": "json",
        "list": "logevents",
        "leprop": "ids|title|details",
        "letype": "move",
        "letitle": title,
        "lelimit": "1"
    }
    LOG = S.post(URL, LOG_PARA).json()

    if len(LOG["query"]["logevents"]) != 1:
        continue

    MOVED_TO = LOG["query"]["logevents"][0]["params"]["target_title"]

    BACK_PARA = {
        "action": "query",
        "format": "json",
        "list": "backlinks",
        "redirects": 1,
        "bltitle": title,
        "bllimit": "500"
    }

    BACK = S.post(URL, BACK_PARA).json()["query"]["backlinks"]

    for j in range(0, 5): # len(BACK)):

        print(title + " - " + BACK[j]["title"])
        title_back = BACK[j]["title"]
        FIX = S.post(URL, {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": title_back,
            "formatversion": "2",
            "rvprop": "content",
            "rvslots": "main"
        })

        FIX_CONT = FIX.json()["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]

        FIX_CONT = FIX_CONT.replace("[[" + title + "]]", "[[" + MOVED_TO + "]]")
        FIX_CONT = FIX_CONT.replace("[[" + title + "|", "[[" + MOVED_TO + "|")

        EDIT_PARA = {
            "action": "edit",
            "title": title_back,
            "token": auth(),
            "format": "json",
            "summary": "Fixing redlinks caused by improper page moves (automatic; small testrun).",
            "text": FIX_CONT
        }

        S.post(URL, EDIT_PARA)
