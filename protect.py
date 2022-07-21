from auth import auth, URL, S


PARAMS_4 = {
    "title": "User:Zsotroav/Sandbox",
    "protections": "edit=sysop|move=sysop",
    "expiry": "infinite",
    "token": auth(),
    "action": "protect",
    "format": "json",
    "reason": "BOT: testing"
}
R = S.post(URL, data=PARAMS_4)
print(R.text)