from auth import auth, URL, S

page = S.post(URL, {
    "action": "query",
    "format": "json",
    "prop": "revisions",
    "titles": "User:Zsotroav/Sandbox/API",
    "formatversion": "2",
    "rvprop": "content",
    "rvslots": "main"
})

page_cont = page.json()["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]
print(page_cont)
newc = page_cont.replace("<span name=\"test\">✘</span>",
                         "<span style=\"font-weight: bold; color: #ff0000;\" name=\"test\">✘</span>")

print(newc)

PARAMS = {
    "action": "edit",
    "title": "User:Zsotroav/Sandbox/API",
    "token": auth(),
    "format": "json",
    "summary": "Testing bot, now hopefully in the actual sandbox.",
    "text": newc
}
R = S.post(URL, data=PARAMS)
print(R.text)
