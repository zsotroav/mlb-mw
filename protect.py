import requests
from auth import auth, URL, S


# Step 4: Send a post request to change edit protection level of a page
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